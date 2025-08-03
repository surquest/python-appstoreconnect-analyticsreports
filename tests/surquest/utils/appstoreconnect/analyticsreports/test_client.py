import unittest
from pathlib import Path
from surquest.utils.appstoreconnect.credentials import Credentials
from surquest.utils.appstoreconnect.analyticsreports.client import Client
from surquest.utils.appstoreconnect.analyticsreports.enums.category import Category
from surquest.utils.appstoreconnect.analyticsreports.enums.granularity import Granularity

ISSUER_ID = "69a6de80-fd44-47e3-e053-5b8c7c11a4d1"
KEY_ID = "5WDUV3USAU"
PRIVATE_KEY_PATH = Path.cwd() / "credentials" / "key.p8"
PRIVATE_KEY = PRIVATE_KEY_PATH.read_text()
APP_ID = "6451202232"
CATEGORY = Category.APP_USAGE
REPORT_NAME = "App Store Installation and Deletion Detailed"
GRANULARITY = Granularity.DAILY
DATE = "2025-07-27"

class TestClientIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client(credentials=Credentials(
            issuer_id=ISSUER_ID,
            key_id=KEY_ID,
            private_key=PRIVATE_KEY
        ))
        cls.test_app_id = APP_ID

    def test_read_report_requests(self):
        response = self.client.read_report_requests(self.test_app_id)
        assert isinstance(response, dict), f"Expected dict, got {type(response)}"
        assert "data" in response, "Response does not contain 'data' key"

    def test_read_report_for_specific_request(self):
        response = self.client.read_report_requests(self.test_app_id)
        request_ids = [item["id"] for item in response.get("data", [])]
        assert request_ids, "No report requests found"

        report_id = request_ids[0]
        report_response = self.client.read_report_for_specific_request(report_id)
        assert isinstance(report_response, dict)
        assert "data" in report_response

    def test_read_list_of_instances_of_report(self):
        report_requests = self.client.read_report_requests(self.test_app_id)
        request_ids = [item["id"] for item in report_requests.get("data", [])]
        assert request_ids, "No report requests found"

        report_response = self.client.read_report_for_specific_request(request_ids[0])
        report_ids = [item["id"] for item in report_response.get("data", [])]
        assert report_ids, "No reports found for request"

        instances = self.client.read_list_of_instances_of_report(report_ids[0])
        assert isinstance(instances, dict)
        assert "data" in instances

    def test_download_report_to_dicts_with_invalid_url(self):
        data = self.client.download_report_to_dicts("https://invalid-url.com/report.gz")
        assert data is None, "Expected None for invalid URL"

    def test_get_data_pipeline(self):
        data = self.client.get_data(
            app_id=self.test_app_id,
            report_name=REPORT_NAME,
            category=CATEGORY,
            granularity=GRANULARITY,
            dates={DATE}
        )
        assert isinstance(data, list)
        if data:
            assert isinstance(data[0], dict)

