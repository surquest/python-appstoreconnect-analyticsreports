
# 📊 AppStoreConnect Analytics Reports Python Package

**Simplified access to Apple App StoreConnect Analytics Reports via API**

[Apple API Docs →](https://developer.apple.com/documentation/appstoreconnectapi/downloading-analytics-reports)

---

## ✨ Overview

This Python package provides a convenient interface to **download Analytics Reports** from the [App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi). It handles authentication using JWT, manages requests, and retrieves analytics data for app usage, sales, crashes, and more.

---

## 🚀 Features

* 🔐 **JWT Authentication** using private key and issuer ID
* 📥 **Download Analytics Reports** for a given app and date
* 🧾 Support for report types: `app-usage`, `crashes`, `sales`, etc.
* 🗓️ Date range selection with proper ISO 8601 formatting
* 🧪 Unit-tested core components

---

## 📦 Installation

```bash
pip install surquest-utils-appstoreconnect-analytics-reports
```

> Or clone this repo:

```bash
git clone https://github.com/surquest/python-appstoreconnect-analyticsreports
cd src/surquest/utils
pip install -e .
```

---

## 🔧 Setup

To use this package, you will need:

* Apple App Store Connect API **Issuer ID**
* Your **Key ID**
* A `.p8` **private key file** downloaded from App Store Connect

Set your credentials in a `.env` file or pass them directly to the client.

```env
APPSTORE_ISSUER_ID=your_issuer_id
APPSTORE_KEY_ID=your_key_id
APPSTORE_PRIVATE_KEY_PATH=AuthKey_XXXXXXXXXX.p8
```

---

## 🧑‍💻 Usage Example

```python
from surquest.utils.appstoreconnect.credentials import Credentials
from surquest.utils.appstoreconnect.analyticsreports import Client

credentials = Credentials(
    issuer_id="your_issuer_id",
    key_id="your_key_id",
    private_key_path="AuthKey_XXXXXXXXXX.p8"
)

client = AnalyticsClient(
    credentials=credentials
)

report_data = client.download_report(
    app_id="1234567890",
    report_type="app-usage",
    report_subtype="DAILY",
    frequency="DAILY",
    report_date="2024-07-01"
)
```

---

## 📚 Supported Report Parameters

| Parameter        | Description                                             |
| ---------------- | ------------------------------------------------------- |
| `report_type`    | Type of report (`app-usage`, `crashes`, `sales`)        |
| `report_subtype` | Format/subtype of report (`DAILY`, `WEEKLY`, `MONTHLY`) |
| `frequency`      | Time granularity (`DAILY`, `WEEKLY`, etc.)              |
| `report_date`    | Date in `YYYY-MM-DD` format                             |

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 📁 Project Structure

```
appstoreconnect_analytics/
│
├── client.py            # API client logic
├── auth.py              # JWT generation
├── utils.py             # Helpers for requests, validation
├── __init__.py
└── ...
tests/
└── test_client.py
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