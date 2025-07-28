import requests
import time


class Client:
    
    BASE_URL = "https://api.appstoreconnect.apple.com/v1"

    def __init__(self, credentials):
        """
        Initializes the client with a Credentials object that provides a JWT token.
        """
        self.credentials = credentials

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.credentials.generate_token()}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def request_reports(self, app_id: str, access_type: str = "ONGOING") -> dict:
        """
        POST /v1/analyticsReportRequests

        Initiates a request to generate a report.
        """
        url = f"{self.BASE_URL}/analyticsReportRequests"
        response = requests.post(url, 
        headers=self._get_headers(), 
        json={
            "data": {
                "type": "analyticsReportRequests",
                "attributes": {
                    "accessType": access_type
                },
                "relationships":{
                    "app":{
                        "data": {
                            "id": app_id,
                            "type": "apps"
                        }
                    }
                }
            }
        }
        )
        response.raise_for_status()
        return response.json()

    def read_report_requests(self, app_id: str) -> dict:
        """
        GET /v1/apps/{id}/analyticsReportRequests
        DOC: https://developer.apple.com/documentation/appstoreconnectapi/get-v1-analyticsreportrequests-_id_-reports

        Reads report requests for the given app.
        """
        url = f"{self.BASE_URL}/apps/{app_id}/analyticsReportRequests"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def read_reports_for_specific_request(self, id: str, filters: dict = None) -> dict:
        """
        GET /v1/analyticsReportRequests/{id}/reports

        Returns report metadata for a specific report request.
        """
        url = f"{self.BASE_URL}/analyticsReportRequests/{id}/reports"

        response = requests.get(url, headers=self._get_headers(), params=filters)
        response.raise_for_status()
        return response.json()

    def list_instances_of_report(self, report_id: str) -> dict:
        """
        GET /v1/analyticsReports/{id}/instances

        Returns all instances of a report.
        """
        url = f"{self.BASE_URL}/analyticsReports/{report_id}/instances"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def read_segments_for_report(self, instance_id: str) -> dict:
        """
        GET /v1/analyticsReportInstances/{id}/segments

        Returns all segments for a report instance.
        """
        url = f"{self.BASE_URL}/analyticsReportInstances/{instance_id}/segments"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
