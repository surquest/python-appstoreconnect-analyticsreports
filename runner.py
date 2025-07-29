import json
from surquest.utils.appstoreconnect.credentials import Credentials
from surquest.utils.appstoreconnect.analyticsreports.client import Client
from surquest.utils.appstoreconnect.analyticsreports.enums.category import Category
from pathlib import Path

key_path = Path.cwd() / "credentials" / "key.p8"
private_key = key_path.read_text()

ISSUER_ID = "69a6de80-fd44-47e3-e053-5b8c7c11a4d1"
KEY_ID = "5WDUV3USAU"
APP_ID = "6451202232"
CATEGORY = Category.APP_USAGE
# REPORT_NAME = "App Crashes Expanded"

credentials = Credentials(
    issuer_id=ISSUER_ID, # 36-character issuer ID
    key_id=KEY_ID, # 10-character key ID from App Store Connect
    private_key=private_key
)

client = Client(credentials=credentials)

client = Client(credentials)

print("--- token ---")
print(credentials.generate_token())
print("-------------")


#1A Read Report Requests
report_requests = client.read_report_requests(app_id=APP_ID)
print(json.dumps(report_requests, indent=2))

#1B Get report ID
report_request_id = report_requests.get("data")[0].get("id")
print(report_request_id)

#2A Read Report
report = client.read_report_for_specific_request(
    request_id=report_request_id,
    params={
        "filter[category]": CATEGORY.value,
        # "filter[name]": REPORT_NAME
    }
)
print(json.dumps(report, indent=2))
report_id = report.get("data")[0].get("id")
print(report_id)

#3A Read Report Instances
instances = client.read_list_of_instances_of_report(report_id=report_id)
print(json.dumps(instances, indent=2))
instance_id = instances.get("data")[0].get("id")
print(instance_id)
#4A Read Report Segments