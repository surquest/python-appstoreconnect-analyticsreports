import requests
from typing import Dict, Any, Optional, List
from ..credentials import Credentials
import csv
import gzip
import io


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

    def _get_headers(self) -> Dict[str, str]:
        """Generates the authorization headers for API requests."""
        token = self.credentials.generate_token()
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
        try:
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raises HTTPError for 4xx or 5xx status codes
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
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
        try:
            # Use a simplified header for downloading the file from the presigned URL
            headers = {"Accept-Encoding": "gzip"}
            response = self.session.get(report_url, headers=headers, stream=True)
            response.raise_for_status()
            
            # Decompress the gzipped content in memory
            gzipped_content = response.content
            decompressed_content = gzip.decompress(gzipped_content)
            
            # Decode bytes to string and use io.StringIO to treat it like a file
            csv_file_string = decompressed_content.decode('utf-8')
            csv_file = io.StringIO(csv_file_string)
            
            # Use csv.DictReader to parse the data into a list of dictionaries
            reader = csv.DictReader(csv_file, delimiter='\t')

            # Normalize keys: lowercase and replace spaces with underscores
            if normalize is True:
                data = [
                    {key.lower().replace(' ', '_'): value for key, value in row.items()}
                    for row in reader
                ]
            else:
                data = list(reader)

            return data

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error downloading report: {e.response.status_code} - {e.response.text}")
        except gzip.BadGzipFile:
            print("Error: The downloaded file is not a valid GZIP file.")
        except Exception as e:
            print(f"An error occurred while processing the report file: {e}")
        
        return None
