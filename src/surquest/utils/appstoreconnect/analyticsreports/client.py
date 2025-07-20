import requests
from ..credentials import Credentials


class AnalyticsClient:
    """
    Client for downloading App Store Connect Analytics Reports.
    Documentation: https://developer.apple.com/documentation/analytics-reports
    """

    BASE_URL = "https://api.appstoreconnect.apple.com/v1"

    def __init__(self, credentials: Credentials):
        """
        Initializes the AnalyticsClient with given credentials.

        :param credentials: An instance of the Credentials class
        """
        self.credentials = credentials

    def download_report(
        self,
        app_id: str,
        report_type: str,  # e.g., "app-usage", "crashes", "sales"
        report_subtype: str,  # e.g., "DAILY", "WEEKLY"
        frequency: str,  # e.g., "DAILY", "WEEKLY"
        report_date: str  # e.g., "2024-07-01"
    ) -> bytes:
        """
        Download a report from App Store Connect Analytics API.

        :param app_id: The app's Apple ID (as string)
        :param report_type: Report type ("app-usage", "crashes", "sales", etc.)
        :param report_subtype: Subtype of report
        :param frequency: Report frequency (DAILY, WEEKLY, etc.)
        :param report_date: ISO 8601 date string ("YYYY-MM-DD")
        :return: Binary report content (CSV zipped file)
        """
        token = self.credentials.generate_token()

        url = f"{self.BASE_URL}/apps/{app_id}/analyticsReports/{report_type}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/a-gzip",
        }
        params = {
            "filter[reportDate]": report_date,
            "filter[reportSubType]": report_subtype,
            "filter[frequency]": frequency
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.content  # Return raw gzip data
        else:
            raise RuntimeError(
                f"Failed to download report: {response.status_code} {response.text}"
            )
