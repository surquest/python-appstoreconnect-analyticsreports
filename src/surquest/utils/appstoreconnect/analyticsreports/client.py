import requests
import warnings
from typing import Dict, Any, Optional, List, Set
import csv
import gzip
import io

from ..credentials import Credentials
from .handler import Handler
from .enums.category import Category
from .enums.granularity import Granularity
from .enums.report_name import ReportName
from .logger import logger
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class APIClientError(Exception):
    """Custom exception for API client errors."""

    pass


class Client:
    """
    A client for interacting with the Apple AppStore Connect Analytics Report API.
    """

    BASE_URL = "https://api.appstoreconnect.apple.com/v1"

    def __init__(self, credentials: Credentials):
        """
        Initializes the API client.

        Args:
            credentials (Credentials): An instance of a credentials class
                                       that provides a `generate_token` method.
        """
        self.credentials = credentials
        self.session = requests.Session()
        self._configure_retries()
        logger.info("Initialized Client with provided credentials")

    def _configure_retries(self):
        """Configures retries for HTTP requests to handle transient errors."""
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)

    def _get_headers(self) -> Dict[str, str]:
        """Generates the authorization headers for API requests."""
        token = self.credentials.generate_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def _get_request(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Performs a GET request and returns JSON response or None."""
        headers = self._get_headers()
        logger.debug(f"GET {url} | Params: {params}")
        try:
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Error: {e}")
        return None

    def _get_resource(
        self, resource_path: str, params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Builds URL and fetches resource."""
        return self._get_request(f"{self.BASE_URL}/{resource_path}", params)

    def _paginate(
        self, resource_path: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Handles pagination and returns full list of data items."""
        results = []
        url = f"{self.BASE_URL}/{resource_path}"
        while url:
            response = self._get_request(url, params)
            if response and "data" in response:
                results.extend(response["data"])
            url = response.get("links", {}).get("next")
            params = None  # subsequent pages include params in URL
        return results

    # ----------------- Public API Methods -----------------

    def read_report_requests(
        self, app_id: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        return self._paginate(f"apps/{app_id}/analyticsReportRequests", params)

    def read_report_for_specific_request(
        self, request_id: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        return self._paginate(f"analyticsReportRequests/{request_id}/reports", params)

    def read_list_of_instances_of_report(
        self, report_id: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        return self._paginate(f"analyticsReports/{report_id}/instances", params)

    def read_segments_for_report(
        self, instance_id: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        return self._paginate(
            f"analyticsReportInstances/{instance_id}/segments", params
        )

    def download_report_to_dicts(
        self, report_url: str, normalize: bool = True
    ) -> Optional[List[Dict[str, str]]]:
        """Downloads a gzipped CSV report and parses it into a list of dictionaries."""
        try:
            csv_content = self._download_gzipped_csv(report_url)
            data = self._parse_csv_to_dicts(csv_content, normalize)
            out = []
            for item in data:
                # item.update({"url": report_url})
                out.append(item)
            return out
        except Exception:
            logger.exception("Failed to download or parse report")
            return None

    # ----------------- Helper Methods -----------------

    def _download_gzipped_csv(self, url: str) -> str:
        """Downloads gzipped CSV and returns as string."""
        response = self.session.get(
            url, headers={"Accept-Encoding": "gzip"}, stream=True
        )
        response.raise_for_status()
        decompressed_content = gzip.decompress(response.content)
        return decompressed_content.decode("utf-8")

    def _parse_csv_to_dicts(
        self, csv_content: str, normalize: bool
    ) -> List[Dict[str, str]]:
        """Parses CSV content into list of dictionaries."""
        csv_file = io.StringIO(csv_content)
        reader = csv.DictReader(csv_file, delimiter="\t")
        if normalize:
            return [
                {key.lower().replace(" ", "_").replace("-", "_"): value for key, value in row.items()}
                for row in reader
            ]
        return list(reader)

    def list_report_dates(
        self,
        report_name: ReportName,
        app_id: Optional[str] = None,
        report_ids: Optional[List[str]] = None,
        granularity: Granularity = Granularity.DAILY,
    ) -> List[str]:
        if not app_id and not report_ids:
            raise APIClientError("Either 'app_id' or 'report_ids' must be provided.")

        if not report_ids:
            response = self.list_reports(
                app_id=app_id, report_name=report_name, category=report_name.category
            )
            report_ids = Handler.extract_ids(response)

        dates: Set[str] = set()
        for report_id in report_ids:
            instances = self.read_list_of_instances_of_report(
                report_id, params={"filter[granularity]": granularity.value}
            )
            if not instances:
                raise APIClientError(f"No instances found for report: {report_id}")
            available_dates = Handler.extract_attribute_values(
                instances, attribute="processingDate"
            )
            if available_dates:
                dates.update(available_dates)
        return sorted(dates)

    def list_reports(
        self,
        app_id: str,
        category: Optional[Category] = None,
        report_name: Optional[ReportName] = None,
    ) -> List[Dict[str, Any]]:
        query_params = {}
        if category:
            query_params["filter[category]"] = category.value
        if report_name:
            query_params["filter[name]"] = report_name.value

        report_requests = self.read_report_requests(app_id)
        report_ids = Handler.extract_ids(report_requests)
        if not report_ids:
            raise APIClientError(f"No report requests found for app: {app_id}")

        reports = []
        for request_id in report_ids:
            reports.extend(
                self.read_report_for_specific_request(request_id, params=query_params)
            )
        return reports

    def get_data(
        self,
        app_id: str,
        report_name: ReportName,
        granularity: Granularity = Granularity.DAILY,
        dates: Optional[Set[str]] = None,
    ) -> List[Dict[str, str]]:
        dates = dates or set()
        data: List[Dict[str, str]] = []

        report_ids = self._fetch_report_ids(app_id, report_name)
        if not dates:
            dates = set(
                self.list_report_dates(
                    report_name, report_ids=report_ids, granularity=granularity
                )
            )

        instance_ids = self._fetch_instance_ids(report_ids, granularity, dates)
        urls = self._fetch_segment_urls(instance_ids)

        date_slices = dict()
        
        for url in urls: # URLs are sorted older are processed before newer
            segment_data = self.download_report_to_dicts(url)
        
            if segment_data:
                # -------------------------------------------------------------- #
                # Important: This part requires patch
                # - for each dataset we have to analyze set of avaialble dates
                #   and for each date we ahve to add them to report dates 
                #   or overwrite it in report_dates
                # -------------------------------------------------------------- #
                
                available_dates = Handler.get_distinct_values(
                    data=segment_data,
                    key='date'
                )

                for avaialble_date in available_dates:

                    data_slice = Handler.filter_list_of_dicts(
                        data=segment_data,
                        attribute='date',
                        value=avaialble_date,
                        comparator='=='
                    )

                    date_slices[avaialble_date] = data_slice

        for date, data_slice in date_slices.items():
            data.extend(data_slice)
        
        return Handler.deduplicate_data(data)

    def fetch_customer_reviews(
        self,
        app_id: str,
        last_known_customer_review_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        max_iterations: Optional[int] = None,

    ) -> List[Dict[str, Any]]:
        """
        Fetches all customer reviews for a given app_id.

        Args:
            app_id (str): The ID of the app.
            last_known_customer_review_id (Optional[str]): If provided, stops pagination once this review ID is found.
            params (Optional[Dict[str, Any]]): Query parameters for the request (default: sort=-createdDate, limit=200).
            max_iterations (Optional[int]): Max number of pagination requests (for integration testing). Unlimited by default.

        Returns:
            List[Dict[str, Any]]: A list of customer review records.
        """
        results = []
        seen_ids = set()
        found_last_known = False
        iterations = 0

        query_params = {
            "limit": 200,
            "sort": "-createdDate",
        }
        if params:
            query_params.update(params)

        url = f"{self.BASE_URL}/apps/{app_id}/customerReviews"

        while url and not found_last_known:
            if max_iterations is not None and iterations >= max_iterations:
                logger.info(f"Reached max iteration limit: {max_iterations}")
                break

            response = self._get_request(url, query_params)
            if not response:
                break

            data = response.get("data", [])
            for item in data:
                review_id = item.get("id")
                if last_known_customer_review_id and review_id == last_known_customer_review_id:
                    found_last_known = True
                    break
                if review_id not in seen_ids:
                    results.append(item)
                    seen_ids.add(review_id)

            url = response.get("links", {}).get("next")
            query_params = None  # Only pass params on the first request
            iterations += 1

        return results

    # ----------------- Private Steps for get_data -----------------

    def _fetch_report_ids(self, app_id: str, report_name: ReportName) -> List[str]:
        reports = self.list_reports(
            app_id, category=report_name.category, report_name=report_name
        )
        return Handler.extract_ids(reports)

    def _fetch_instance_ids(
        self, report_ids: List[str], granularity: Granularity, dates: Set[str]
    ) -> List[str]:
        instance_ids: List[str] = []
        for report_id in report_ids:
            for date in dates:
                instances = self.read_list_of_instances_of_report(
                    report_id,
                    params={
                        "filter[granularity]": granularity.value,
                        "filter[processingDate]": date,
                    },
                )
                ids = Handler.extract_ids(instances)
                instance_ids.extend(ids)
        return instance_ids

    def _fetch_segment_urls(self, instance_ids: List[str]) -> List[str]:
        urls: List[str] = []
        for instance_id in instance_ids:
            segments = self.read_segments_for_report(instance_id)
            urls.extend(Handler.extract_attribute_values(segments, attribute="url"))
        return sorted(urls)
