import unittest
from pathlib import Path
from surquest.utils.appstoreconnect.credentials import Credentials
from surquest.utils.appstoreconnect.analyticsreports.client import Client
from surquest.utils.appstoreconnect.analyticsreports.enums.granularity import (
    Granularity,
)
from surquest.utils.appstoreconnect.analyticsreports.enums.report_name import ReportName


ISSUER_ID = "69a6de80-fd44-47e3-e053-5b8c7c11a4d1"
KEY_ID = "5WDUV3USAU"
PRIVATE_KEY_PATH = Path.cwd() / "credentials" / "key.p8"
PRIVATE_KEY = PRIVATE_KEY_PATH.read_text()
APP_ID = "950949627"
REPORT_NAME = ReportName.APP_STORE_INSTALLATION_AND_DELETION_STANDARD
GRANULARITY = Granularity.DAILY
DATE = "2025-07-27"


class TestClientIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client(
            credentials=Credentials(
                issuer_id=ISSUER_ID, key_id=KEY_ID, private_key=PRIVATE_KEY
            )
        )
        cls.test_app_id = APP_ID

    def test_read_report_requests(self):
        response = self.client.read_report_requests(self.test_app_id)
        assert isinstance(response, list), f"Expected list, got {type(response)}"
        if response:
            assert (
                "id" in response[0]
            ), "Each report request should contain an 'id' field"

    def test_read_report_for_specific_request(self):

        report_requests = self.client.read_report_requests(self.test_app_id)
        assert isinstance(
            report_requests, list
        ), f"Expected list, got {type(report_requests)}"
        assert report_requests, "No report requests found"

        request_id = report_requests[0]["id"]
        report_response = self.client.read_report_for_specific_request(request_id)
        assert isinstance(
            report_response, list
        ), f"Expected list, got {type(report_response)}"
        if report_response:
            assert (
                "id" in report_response[0]
            ), "Report item should contain an 'id' field"

    def test_read_list_of_instances_of_report(self):
        report_requests = self.client.read_report_requests(self.test_app_id)
        assert report_requests, "No report requests found"

        request_id = report_requests[0]["id"]
        report_response = self.client.read_report_for_specific_request(request_id)
        assert report_response, "No reports found for the given request"

        report_id = report_response[0]["id"]
        instances = self.client.read_list_of_instances_of_report(report_id)
        assert isinstance(instances, list), f"Expected list, got {type(instances)}"
        if instances:
            assert "id" in instances[0], "Instance item should contain an 'id' field"

    def test_download_report_to_dicts_with_invalid_url(self):
        data = self.client.download_report_to_dicts("https://invalid-url.com/report.gz")
        assert data is None, "Expected None for invalid URL"

    def test_list_report_dates(self):

        dates = self.client.list_report_dates(
            app_id=self.test_app_id,
            report_name=REPORT_NAME,
            granularity=GRANULARITY,
        )

        assert isinstance(dates, list), f"Expected list, got {type(dates)}"
        if dates:
            assert isinstance(
                dates[0], str
            ), f"Expected string in dates list, got {type(dates[0])}"


    def test_get_data_pipeline(self):
        data = self.client.get_data(
            app_id=self.test_app_id,
            report_name=REPORT_NAME,
            granularity=GRANULARITY,
            dates={DATE},
        )
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        if data:
            assert isinstance(
                data[0], dict
            ), f"Expected dict in data rows, got {type(data[0])}"

    def test__get_request(self):

        response = self.client._get_request("https://httpstat.us/400")
        assert None == response
        
    def test_fetch_customer_reviews(self):
        reviews = self.client.fetch_customer_reviews(
            app_id=self.test_app_id,
            max_iterations=2,  # Limit for test efficiency
        )

        assert isinstance(reviews, list), f"Expected list, got {type(reviews)}"
        if reviews:
            first = reviews[0]
            assert isinstance(first, dict), f"Expected dict, got {type(first)}"
            assert "id" in first, "Each review should contain an 'id' field"