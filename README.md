
# 📊 AppStoreConnect Analytics Reports Python Package

**Simplified access to Apple App StoreConnect Analytics Reports via API**

[Apple API Docs →](https://developer.apple.com/documentation/appstoreconnectapi/downloading-analytics-reports)

---

## ✨ Overview

This Python package provides a convenient interface to **download Analytics Reports** from the [App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi). It handles authentication using JWT, manages requests, and retrieves analytics data for app usage, sales, crashes, and more.

---

## 🚀 Features

* **JWT Authentication** using private key and issuer ID
* **Download Analytics Reports** for a given app and date
* Support for report types: `ONGOING`, `ONE_TIME_SNAPSHOT`
* Full fetch of history including APP Customer Reviews 
* Unit-tested core components

---

## 📦 Installation

```bash
pip install surquest-utils-appstoreconnect-analyticsreports
```

> Or clone this repo:

```bash
git clone git@github.com:surquest/python-appstoreconnect-analyticsreports.git
cd src/surquest/utils
pip install --no-cache-dir -r requirements.txt
```
---

## 🔧 Setup

To use this package, you will need:

* Apple App Store Connect API **Issuer ID**
* Your **Key ID**
* A `.p8` **private key** downloaded from App Store Connect

Set your credentials in a `.env` file or pass them directly to the client.

```env
ISSUER_ID=your_issuer_id
KEY_ID=your_key_id
PRIVATE_KEY=-----BEGIN PRIVATE KEY-----???-----END PRIVATE KEY-----
```

---

## 🧑‍💻 Usage Example

```python

import os
from surquest.utils.appstoreconnect.credentials import Credentials
from surquest.utils.appstoreconnect.analyticsreports.client import Client
from surquest.utils.appstoreconnect.analyticsreports.handler import Handler
from surquest.utils.appstoreconnect.analyticsreports.enums.category import Category
from surquest.utils.appstoreconnect.analyticsreports.enums.granularity import Granularity
from surquest.utils.appstoreconnect.analyticsreports.enums.report_name import ReportName

APP_ID = "123456789"
REPORT_NAME = ReportName.APP_SESSIONS_STANDARD
ACCESS_TYPE = "ONGOING"
GRANULARITY = Granularity.DAILY
CSV_PATH = "./your/path/to/export/data.csv"

credentials = Credentials(
    issuer_id=os.getenv('ISSUER_ID'),
    key_id=os.getenv('KEY_ID'),
    private_key_path=os.getenv('PRIVATE_KEY'),
)

client = Client(credentials=credentials)

# Example: Download analytics data
data = client.get_data(
    app_id = APP_ID,
    report_name = REPORT_NAME,
    access_type = "ONE_TIME_SNAPSHOT"
)

Handler.list_of_dicts_to_csv(data, CSV_PATH)
```
---

## 📚 Supported Report Parameters

| Parameter        | Description                                             |
| ---------------- | ------------------------------------------------------- |
| `report_name`    | Enum specified in `ReportName` `surquest.utils.appstoreconnect.analyticsreports.enums.report_name.ReportName` |
| `granularity`    | Enum specified in `surquest.utils.appstoreconnect.analyticsreports.enums.granularity.Granularity` |
| `dates`          | Set of dates in `YYYY-MM-DD` format |

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 📁 Project Structure

```
src/
└── surquest/
    └── utils/
        └── appstoreconnect/
            ├── __init__.py
            ├── credentials.py
            ├── requirements.txt
            └── analyticsreports/
                ├── __init__.py
                ├── client.py
                ├── errors.py
                ├── handler.py
                └── enums/
                    ├── __init__.py
                    ├── category.py
                    ├── granularity.py
                    └── report_name.py
tests/
└── surquest/
    └── utils/
        └── appstoreconnect/
            └── analyticsreports/
                └── test_client.py
README.md
pyproject.toml
LICENSE
.gitignore
```

---

## 🛡️ Disclaimer

This project is not affiliated with Apple Inc. Use responsibly and according to Apple’s [Terms of Use](https://developer.apple.com/terms/).

---

## 📄 License

MIT License

---

## 🙋‍♀️ Contact / Contribute

PRs welcome! For bugs or feature requests, open an [issue](https://github.com/your-org/appstoreconnect-analytics/issues).