import requests
import warnings
from typing import Dict, Any, Optional, List
import csv
import gzip
import io
import logging

from ..credentials import Credentials
from .handler import Handler
from .enums.category import Category
from .enums.granularity import Granularity

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


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
        logger.info("Initialized Client with provided credentials")

    def _get_headers(self) -> Dict[str, str]:
        """Generates the authorization headers for API requests."""
        token = self.credentials.generate_token()
        logger.debug("Generated authorization token")
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def _get_request(self, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Performs a GET request to a specified URL.

        Args:
            url (str): The full URL for the API endpoint.
            params (Optional[Dict[str, Any]]): A dictionary of query parameters.

        Returns:
            Optional[Dict[str, Any]]: The JSON response as a dictionary, or None if an error occurs.
        """
        headers = self._get_headers()
        logger.debug(f"GET {url} | Params: {params}")
        try:
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raises HTTPError for 4xx or 5xx status codes
            logger.debug(f"Response Status: {response.status_code}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Error: {e}")
        return None

    def read_report_requests(self, app_id: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Reads the list of analytics report requests for a specific app.
        API Docs: https://developer.apple.com/documentation/appstoreconnectapi/get-v1-apps-_id_-analyticsreportrequests

        Args:
            app_id (str): The identifier of the app.
            params (Optional[Dict[str, Any]]): Optional query parameters.

        Returns:
            Optional[Dict[str, Any]]: API response dictionary.
        """
        url = f"{self.BASE_URL}/apps/{app_id}/analyticsReportRequests"
        logger.info(f"Fetching report requests for app_id: {app_id}")
        return self._get_request(url, params)

    def read_report_for_specific_request(self, request_id: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Reads the report for a specific analytics report request.
        API Docs: https://developer.apple.com/documentation/appstoreconnectapi/get-v1-analyticsreportrequests-_id_-reports

        Args:
            request_id (str): The identifier of the report request.
            params (Optional[Dict[str, Any]]): Optional query parameters.

        Returns:
            Optional[Dict[str, Any]]: API response dictionary.
        """
        url = f"{self.BASE_URL}/analyticsReportRequests/{request_id}/reports"
        logger.info(f"Fetching reports for report request id: {request_id}")
        return self._get_request(url, params)

    def read_list_of_instances_of_report(self, report_id: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Reads the list of instances for a specific report.
        API Docs: https://developer.apple.com/documentation/appstoreconnectapi/get-v1-analyticsreports-_id_-instances

        Args:
            report_id (str): The identifier of the report.
            params (Optional[Dict[str, Any]]): Optional query parameters.

        Returns:
            Optional[Dict[str, Any]]: API response dictionary.
        """
        url = f"{self.BASE_URL}/analyticsReports/{report_id}/instances"
        logger.info(f"Fetching instances for report id: {report_id} with params: {params}")
        return self._get_request(url, params)

    def read_segments_for_report(self, instance_id: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Reads the segments for a specific report instance (e.g., by domain or territory).
        API Docs: https://developer.apple.com/documentation/appstoreconnectapi/get-v1-analyticsreportinstances-_id_-segments

        Args:
            instance_id (str): The identifier of the report instance.
            params (Optional[Dict[str, Any]]): Optional query parameters.

        Returns:
            Optional[Dict[str, Any]]: API response dictionary.
        """
        url = f"{self.BASE_URL}/analyticsReportInstances/{instance_id}/segments"
        logger.info(f"Fetching segments for instance id: {instance_id}")
        return self._get_request(url, params)

    def download_report_to_dicts(self, report_url: str, normalize: bool = True) -> Optional[List[Dict[str, str]]]:
        """
        Downloads a gzipped CSV report from a URL and loads it into a list of dictionaries.

        This method uses only native Python libraries. The URL for the report is 
        typically found in the 'url' attribute of a report instance or segment object.

        Args:
            report_url (str): The presigned URL to the .csv.gz report file.
            normalize (bool): Convert the keys of the dictionaries to lowercases with underscores instead of spaces

        Returns:
            Optional[List[Dict[str, str]]]: A list of dictionaries, where each dictionary
                                            represents a row of the report. Returns None on error.
        """
        logger.info(f"Downloading report from URL: {report_url}")
        try:
            headers = {"Accept-Encoding": "gzip"}
            response = self.session.get(report_url, headers=headers, stream=True)
            response.raise_for_status()

            decompressed_content = gzip.decompress(response.content)
            csv_file_string = decompressed_content.decode('utf-8')
            csv_file = io.StringIO(csv_file_string)
            reader = csv.DictReader(csv_file, delimiter='\t')

            if normalize:
                data = [
                    {key.lower().replace(' ', '_'): value for key, value in row.items()}
                    for row in reader
                ]
            else:
                data = list(reader)

            logger.debug(f"Downloaded {len(data)} rows.")
            return data

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error downloading report: {e.response.status_code} - {e.response.text}")
        except gzip.BadGzipFile:
            logger.error("Error: The downloaded file is not a valid GZIP file.")
        except Exception:
            logger.exception("An error occurred while processing the report file.")
        return None

    def get_data(
        self,
        app_id: str,
        report_name: str,
        category: Category,
        granularity: Granularity,
        dates: set = set()
    ) -> list:
        """
        Retrieves data from the App Store Connect Analytics Report API.

        This is the main entry point for downloading analytics data. It performs the following steps:
        1. Fetches report request IDs for the specified app.
        2. Retrieves report IDs based on the given category and report name.
        3. Obtains report instance IDs according to the specified granularity and optional dates.
        4. Fetches URLs for all report segments.
        5. Downloads and combines all segments into a single list of dictionaries.

        Args:
            app_id (str): The App Store Connect application ID.
            report_name (str): Name of the analytics report to retrieve.
            category (Category): Report category (e.g., SALES, USAGE).
            granularity (Granularity): Data granularity (e.g., DAILY, WEEKLY).
            dates (set, optional): Set of dates to filter the report instances. Defaults to empty set.

        Returns:
            list: Combined report data as a list of dictionaries.
        """
        logger.info("Starting get_data process")
        logger.debug(f"Parameters: app_id={app_id}, report_name={report_name}, category={category}, granularity={granularity}, dates={dates}")

        data: list = []
        report_request_ids: list = []
        report_ids: list = []
        instance_ids: list = []
        urls: list = []

        # Step 1: Fetch report requests IDs
        report_requests = self.read_report_requests(app_id=app_id)
        report_request_ids.extend(Handler.extract_ids(report_requests))
        logger.debug(f"Found report request IDs: {report_request_ids}")

        if not report_request_ids:
            logger.error(f"No report requests found for app: {app_id}")
            raise Exception(f"No report requests found for app: {app_id}")

        # Step 2: Get report list for the request
        for report_request_id in report_request_ids:
            reports = self.read_report_for_specific_request(
                request_id=report_request_id,
                params={
                    "filter[category]": category.value,
                    "filter[name]": report_name
                }
            )
            reports_ids = Handler.extract_ids(reports)
            if not reports_ids:
                logger.warning(f"No reports found for app: {app_id} and report request id: {report_request_id}")
                continue
            else:
                report_ids.extend(reports_ids)
        logger.debug(f"Collected report IDs: {report_ids}")

        if not report_ids:
            logger.error(f"No reports found for app: {app_id}")
            raise Exception(f"No reports found for app: {app_id}")

        # Step 3A: Get dates if not defined
        if not dates:
            logger.info("Dates not provided; fetching available dates.")
            for report_id in report_ids:
                instances = self.read_list_of_instances_of_report(
                    report_id=report_id,
                    params={
                        "filter[granularity]": granularity.value
                    }
                )
                available_dates = Handler.extract_attribute_values(
                    payload=instances,
                    attribute='processingDate'
                )
                if available_dates:
                    dates.update(available_dates)
            dates = set(sorted(dates))
            logger.info(f"Updated dates set: {dates}")

        # Step 3B: Get report instances
        for report_id in report_ids:
            for date in dates:
                logger.debug(f"Processing report_id={report_id} and date={date}")
                instances = self.read_list_of_instances_of_report(
                    report_id=report_id,
                    params={
                        "filter[granularity]": granularity.value,
                        "filter[processingDate]": date
                    }
                )
                available_instance_ids = Handler.extract_ids(payload=instances)
                if available_instance_ids:
                    instance_ids.extend(available_instance_ids)
                else:
                    logger.warn(f"No instances found for report_id={report_id} and date={date}")

        logger.debug(f"Collected instance IDs: {instance_ids}")

        # Step 4: Get report segments
        for instance_id in instance_ids:
            segments = self.read_segments_for_report(instance_id=instance_id)
            available_urls = Handler.extract_attribute_values(payload=segments, attribute='url')
            if available_urls:
                urls.extend(available_urls)
            else:
                logger.debug(f"No segments found for instance_id={instance_id}")

        logger.debug(f"Collected segment URLs: {urls}")

        # Step 5: Download and combine all segments
        for url in urls:
            segment_data = self.download_report_to_dicts(report_url=url)
            if segment_data:
                data.extend(segment_data)

        logger.info(f"Total records collected: {len(data)}")
        return data
