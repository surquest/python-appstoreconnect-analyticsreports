import json
from src.surquest.utils.appstoreconnect.credentials import Credentials
from src.surquest.utils.appstoreconnect.analyticsreports.client import Client
from src.surquest.utils.appstoreconnect.analyticsreports.handler import Handler
from src.surquest.utils.appstoreconnect.analyticsreports.enums.category import Category
from src.surquest.utils.appstoreconnect.analyticsreports.enums.granularity import Granularity
from src.surquest.utils.appstoreconnect.analyticsreports.enums.report_name import ReportName
from pathlib import Path

key_path = Path.cwd() / "credentials" / "key.p8"
CATEGORY = Category.FRAMEWORK_USAGE
REPORT_NAME = ReportName.APP_STORE_INSTALLATION_AND_DELETION_DETAILED
GRANULARITY = Granularity.DAILY
DATE = "2025-07-27"
APP_ID = "950949627"

KEY_ID = '5WDUV3USAU' # 10-character key ID from App Store Connect
ISSUER_ID = '69a6de80-fd44-47e3-e053-5b8c7c11a4d1'  # 36-character issuer ID
PRIVATE_KEY = key_path.read_text()

credentials = Credentials(
    issuer_id=ISSUER_ID, # 36-character issuer ID
    key_id=KEY_ID, # 10-character key ID from App Store Connect
    private_key=PRIVATE_KEY
)
client = Client(credentials=credentials)
# token = credentials.generate_token()
#1A Read Report Requests
# report_requests = client.read_report_requests(app_id=APP_ID)
# data = client.get_data(
#     app_id = APP_ID,
#     report_name = REPORT_NAME,
#     category = CATEGORY,
#     granularity = GRANULARITY,
#     # dates = {'2025-07-25', '2025-07-26'}
# )

data = client.list_reports(
    app_id = APP_ID
)

# Extract Report types
print(json.dumps(Handler.extract_attribute_values(data), indent=4))

dates = client.list_report_dates(
    report_name = REPORT_NAME,
    app_id = APP_ID,
    granularity = GRANULARITY
)

print(f"/{dates}/")
print(json.dumps(list(dates), indent=4))
