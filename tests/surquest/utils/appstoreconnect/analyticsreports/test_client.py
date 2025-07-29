import os
import json
import unittest
from surquest.utils.appstoreconnect.credentials import Credentials
from surquest.utils.appstoreconnect.analyticsreports.client import Client
from surquest.utils.appstoreconnect.analyticsreports.enums.category import Category
from surquest.utils.appstoreconnect.analyticsreports.enums.granularity import Granularity
from pathlib import Path


ISSUER_ID = "69a6de80-fd44-47e3-e053-5b8c7c11a4d1"
KEY_ID = "5WDUV3USAU"
PRIVATE_KEY_PATH = Path.cwd() / "credentials" / "key.p8"
PRIVATE_KEY = PRIVATE_KEY_PATH.read_text()
APP_ID = "6451202232"
CATEGORY = Category.APP_USAGE
REPORT_NAME = "App Store Installation and Deletion Detailed"
GRANULARITY = Granularity.DAILY
DATE = "2025-07-27"

class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client(credentials=Credentials(
                issuer_id=ISSUER_ID, # 36-character issuer ID
                key_id=KEY_ID, # 10-character key ID from App Store Connect
                private_key=PRIVATE_KEY
            ))
        cls.test_app_id = APP_ID

    # def test_read_report_requests(self):

    #     response = self.client.read_report_requests(self.test_app_id)
        
    #     assert isinstance(response, dict), \
    #         f"Response instance is {response.__class__.__name__}"
        
    #     assert "data" in response, \
    #         f"No key `data` in the response"

    # def test_read_report_for_specific_request(self):
        
        
    #     response = self.client.read_report_for_specific_request(
    #         self.test_request_id
    #     )

    #     assert isinstance(response, dict)
    #     assert "data" in response

    # def test_read_list_of_instances_of_report(self):
    #     response = self.client.read_list_of_instances_of_report(self.test_report_id)
    #     assert isinstance(response, dict)
    #     assert "data" in response

    # def test_read_segments_for_report(self):
    #     response = self.client.read_segments_for_report(self.test_instance_id)
    #     assert isinstance(response, dict)
    #     assert "data" in response

    # def test_download_report_to_dicts(self):
    #     data = self.client.download_report_to_dicts(self.test_report_url)
    #     assert isinstance(data, list)
    #     if data:
    #         assert isinstance(data[0], dict)
    #         assert all(isinstance(k, str) for k in data[0].keys())

    # def test_download_report_to_dicts_without_normalize(self):
    #     data = self.client.download_report_to_dicts(self.test_report_url, normalize=False)
    #     assert isinstance(data, list)
    #     if data:
    #         assert isinstance(data[0], dict)
