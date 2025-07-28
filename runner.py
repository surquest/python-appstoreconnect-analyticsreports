import json
from surquest.utils.appstoreconnect.credentials import Credentials
from surquest.utils.appstoreconnect.analyticsreports.client import Client

from pathlib import Path

key_path = Path.cwd() / "credentials" / "key.p8"
private_key = key_path.read_text()

ISSUER_ID = "69a6de80-fd44-47e3-e053-5b8c7c11a4d1"
KEY_ID = "5WDUV3USAU"
APP_ID = "6451202232"

credentials = Credentials(
    issuer_id=ISSUER_ID, # 36-character issuer ID
    key_id=KEY_ID, # 10-character key ID from App Store Connect
    private_key=private_key
)

client = Client(credentials=credentials)

client = Client(credentials)

print("--- token ---")
print(credentials.generate_token())
print("--- --- ---")

# # Step 1: Request a report
# try:
#     report_request = client.request_reports(app_id = APP_ID)
#     request_id = report_request["data"]["id"]
# except Exception as e:
#     print(f"Error requesting report: {e}")
    
#     report_requests = client.read_report_requests(app_id=APP_ID)
#     # print(json.dumps(report_requests, indent=4))
#     request_id = report_requests.get("data")[0].get("id")

# print(f"Request ID: {request_id}")

# # Step 2: Poll for report status
# while True:
#     reports = client.read_reports_for_specific_request(request_id)
#     if reports["data"]:
#         print("Report ready!")
#         print(json.dumps(reports, indent=4))
#         break
#     print("Waiting for report...")
#     time.sleep(10)

# # Step 3: Get report instances
# report_id = reports["data"][0]["id"]
# instances = client.list_instances_of_report(report_id)
# download_url = instances["data"][0]["attributes"]["downloadUrl"]

# # Step 4: Download report
# report_response = requests.get(download_url)
# with open("report.gz", "wb") as f:
#     f.write(report_response.content)
