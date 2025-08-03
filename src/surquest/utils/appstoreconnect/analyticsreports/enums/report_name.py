from enum import Enum
from .category import Category


class ReportName(str, Enum):
    AIRPLAY_DISCOVERY_SESSIONS = ("AirPlay Discovery Sessions", Category.FRAMEWORK_USAGE)
    HOME_SCREEN_WIDGET_ROTATIONS = ("Home Screen Widget Rotations", Category.FRAMEWORK_USAGE)
    FILE_BASED_VIDEO_PLAYBACK_USAGE = ("File-Based Video Playback Usage", Category.FRAMEWORK_USAGE)
    SAFARI_EXTENSIONS_USAGE = ("Safari Extensions Usage", Category.FRAMEWORK_USAGE)
    CRABS_BASED_VIDEO_PLAYBACK_USAGE = ("CRABS-Based Video Playback Usage", Category.FRAMEWORK_USAGE)
    TRANSLATION_REQUEST_USAGE = ("Translation Request Usage", Category.FRAMEWORK_USAGE)
    SAFARI_EXTENSIONS_ENABLEMENT = ("Safari Extensions Enablement", Category.FRAMEWORK_USAGE)
    AUTOMATIC_SPEECH_RECOGNITION_USAGE = ("Automatic Speech Recognition Usage", Category.FRAMEWORK_USAGE)
    KEYBOARD_DICTATION_USAGE = ("Keyboard Dictation Usage", Category.FRAMEWORK_USAGE)
    SPATIAL_AUDIO_USAGE = ("Spatial Audio Usage", Category.FRAMEWORK_USAGE)
    VIDEO_DURATION_INFORMATION = ("Video Duration Information", Category.FRAMEWORK_USAGE)
    DEFAULT_BROWSER_USAGE_RATE = ("Default Browser Usage Rate", Category.FRAMEWORK_USAGE)
    HOME_SCREEN_WIDGETS = ("Home Screen Widgets", Category.FRAMEWORK_USAGE)
    BROWSER_CHOICE_SCREEN_ENGAGEMENT_IOS_VERSIONS_BEFORE_18_2 = (
        "Browser Choice Screen Engagement (iOS versions before 18.2)", Category.FRAMEWORK_USAGE
    )
    HOME_SCREEN_WIDGET_USAGE = ("Home Screen Widget Usage", Category.FRAMEWORK_USAGE)
    VISIONKIT_IMAGE_ANALYSIS = ("VisionKit Image Analysis", Category.FRAMEWORK_USAGE)
    REMINDERS_USAGE = ("Reminders Usage", Category.FRAMEWORK_USAGE)
    PHOTOKIT_IMPORTS = ("PhotoKit Imports", Category.FRAMEWORK_USAGE)
    NETWORKING_CONNECTION_ACTIVITY = ("Networking Connection Activity", Category.PERFORMANCE)
    SPEECH_FRAMEWORK_TRANSCRIPTION_REQUESTS = ("Speech Framework Transcription Requests", Category.FRAMEWORK_USAGE)
    HTTP_LIVE_STREAMING_VIDEO_PLAYBACK_USAGE = ("HTTP Live Streaming Video Playback Usage", Category.FRAMEWORK_USAGE)
    MODE_ACTIVITY_NOTIFICATIONS = ("Mode Activity Notifications", Category.FRAMEWORK_USAGE)
    METAL_COMMAND_QUEUES = ("Metal Command Queues", Category.FRAMEWORK_USAGE)
    LOCK_SCREEN_WIDGET_CONFIGURATION = ("Lock Screen Widget Configuration", Category.FRAMEWORK_USAGE)
    LOCAL_NETWORK_PRIVACY = ("Local Network Privacy", Category.FRAMEWORK_USAGE)
    PHOTOS_LIBRARY_ACCESS = ("Photos Library Access", Category.FRAMEWORK_USAGE)
    GAME_CONTROLLER_SESSIONS = ("Game Controller Sessions", Category.FRAMEWORK_USAGE)
    SPEECH_FRAMEWORK_TRANSCRIPTION_REQUEST_AUDIO_DURATION = (
        "Speech Framework Transcription Request Audio Duration", Category.FRAMEWORK_USAGE
    )
    TEXT_INPUT_ACTIONS = ("Text-Input Actions", Category.FRAMEWORK_USAGE)
    VISIONKIT_SESSIONS = ("VisionKit Sessions", Category.FRAMEWORK_USAGE)
    CAMETALLAYER_PERFORMANCE = ("CAMetalLayer Performance", Category.PERFORMANCE)
    BLUETOOTH_SYSTEM_WAKES = ("Bluetooth System Wakes", Category.PERFORMANCE)
    APP_RUNTIME_USAGE = ("App Runtime Usage", Category.FRAMEWORK_USAGE)
    APP_DOWNLOADS_STANDARD = ("App Downloads Standard", Category.COMMERCE)
    APP_DOWNLOADS_DETAILED = ("App Downloads Detailed", Category.COMMERCE)
    APP_INSTALL_PERFORMANCE = ("App Install Performance", Category.PERFORMANCE)
    APP_STORE_INSTALLATION_AND_DELETION_STANDARD = ("App Store Installation and Deletion Standard", Category.APP_USAGE)
    APP_STORE_INSTALLATION_AND_DELETION_DETAILED = ("App Store Installation and Deletion Detailed", Category.APP_USAGE)
    APP_SESSIONS_STANDARD = ("App Sessions Standard", Category.APP_USAGE)
    APP_SESSIONS_DETAILED = ("App Sessions Detailed", Category.APP_USAGE)
    APP_STORE_PRE_ORDERS_STANDARD = ("App Store Pre-Orders Standard", Category.COMMERCE)
    APP_STORE_PRE_ORDERS_DETAILED = ("App Store Pre-Orders Detailed", Category.COMMERCE)
    APP_STORE_PURCHASES_STANDARD = ("App Store Purchases Standard", Category.COMMERCE)
    APP_STORE_PURCHASES_DETAILED = ("App Store Purchases Detailed", Category.COMMERCE)
    APP_STORE_DISCOVERY_AND_ENGAGEMENT_STANDARD = (
        "App Store Discovery and Engagement Standard", Category.APP_STORE_ENGAGEMENT
    )
    APP_STORE_DISCOVERY_AND_ENGAGEMENT_DETAILED = (
        "App Store Discovery and Engagement Detailed", Category.APP_STORE_ENGAGEMENT
    )
    FLASHLIGHT_USAGE = ("Flashlight Usage", Category.FRAMEWORK_USAGE)
    ARKIT_WORLD_TRACKING = ("ARKit World Tracking", Category.FRAMEWORK_USAGE)
    ARKIT_WORLD_TRACKING_IMAGE_DETECTION = ("ARKit World Tracking Image Detection", Category.FRAMEWORK_USAGE)
    PHOTOGRAMMETRY_OBJECTCAPTURESESSION_API_USAGE = ("Photogrammetry ObjectCaptureSession API Usage", Category.FRAMEWORK_USAGE)
    PHOTOGRAMMETRYSESSION_API_USAGE = ("PhotogrammetrySession API Usage", Category.FRAMEWORK_USAGE)
    HAPTICS_ENGINE_USAGE = ("Haptics Engine Usage", Category.FRAMEWORK_USAGE)
    SHAZAMKIT_USAGE = ("ShazamKit Usage", Category.FRAMEWORK_USAGE)
    APP_ADDED_TO_FOCUS = ("App Added to Focus", Category.FRAMEWORK_USAGE)
    STREAMING_PLAYBACK_PERFORMANCE = ("Streaming Playback Performance", Category.PERFORMANCE)
    STREAMING_DOWNLOADS_PERFORMANCE = ("Streaming Downloads Performance", Category.PERFORMANCE)
    AUDIO_INPUT_MUTING = ("Audio Input Muting", Category.FRAMEWORK_USAGE)
    AIRPLAY_PERFORMANCE = ("AirPlay Performance", Category.PERFORMANCE)
    ROOMPLAN_USAGE = ("RoomPlan Usage", Category.FRAMEWORK_USAGE)
    AUDIO_INPUT_ROUTE_AND_DURATION_AND_CALL_MODE = ("Audio Input Route and Duration and Call Mode", Category.FRAMEWORK_USAGE)
    APP_DISK_SPACE_USAGE = ("App Disk Space Usage", Category.FRAMEWORK_USAGE)
    LOCATION_SESSIONS = ("Location Sessions", Category.FRAMEWORK_USAGE)
    CARPLAY_NAVIGATION = ("CarPlay Navigation", Category.FRAMEWORK_USAGE)
    VIDEO_PIP_DURATION = ("Video PiP Duration", Category.FRAMEWORK_USAGE)
    HTTP_LIVE_STREAMING_PLAYBACK_ERRORS = ("HTTP Live Streaming Playback Errors", Category.PERFORMANCE)
    HTTP_LIVE_STREAMING_PLAYBACK_COUNT = ("HTTP Live Streaming Playback Count", Category.FRAMEWORK_USAGE)
    BLUETOOTH_LE_SCANS = ("Bluetooth LE Scans", Category.FRAMEWORK_USAGE)
    BLUETOOTH_LE_ADVERTISING = ("Bluetooth LE Advertising", Category.FRAMEWORK_USAGE)
    ACCESSORYSETUPKIT_USAGE = ("AccessorySetupKit Usage", Category.FRAMEWORK_USAGE)
    APP_CLIP_USAGE_STANDARD = ("App Clip Usage Standard", Category.APP_USAGE)
    APP_CLIP_USAGE_DETAILED = ("App Clip Usage Detailed", Category.APP_USAGE)
    APP_CRASHES = ("App Crashes", Category.APP_USAGE)
    CUSTOM_LANGUAGE_MODEL_BUILDS_FAILED = ("Custom Language Model Builds Failed", Category.PERFORMANCE)
    CUSTOM_LANGUAGE_MODEL_BUILDS_STARTED = ("Custom Language Model Builds Started", Category.FRAMEWORK_USAGE)
    CUSTOMIZED_TRANSCRIPTION_REQUESTS = ("Customized Transcription Requests", Category.FRAMEWORK_USAGE)
    DOCKKIT_APP_USAGE = ("DockKit App Usage", Category.FRAMEWORK_USAGE)
    LIVE_ACTIVITY_USE = ("Live Activity Use", Category.FRAMEWORK_USAGE)
    MULTIPLE_GAME_CONTROLLERS_USAGE = ("Multiple Game Controllers Usage", Category.FRAMEWORK_USAGE)
    PHOTOS_PICKER = ("Photos Picker", Category.FRAMEWORK_USAGE)
    SHARED_WITH_YOU_CONTENT_ENGAGEMENT = ("Shared With You Content Engagement", Category.FRAMEWORK_USAGE)
    SPOTLIGHT_QUERY_PERFORMANCE = ("Spotlight Query Performance", Category.PERFORMANCE)
    IBEACON_ADD_REGION_USAGE = ("iBeacon Add Region Usage", Category.FRAMEWORK_USAGE)
    IBEACON_STOP_MONITORING_FOR_REGION_USAGE = ("iBeacon Stop Monitoring for Region Usage", Category.FRAMEWORK_USAGE)
    VISIONKIT_LIVE_TEXT_USAGE = ("VisionKit Live Text Usage", Category.FRAMEWORK_USAGE)
    WI_FI_KNOWN_NETWORK_MODIFICATIONS = ("Wi-Fi Known Network Modifications", Category.FRAMEWORK_USAGE)
    ACCESSORYSETUPKIT_ACCESSORY_PICKER_SESSIONS = ("AccessorySetupKit Accessory Picker Sessions", Category.FRAMEWORK_USAGE)
    BLUETOOTH_LE_SESSION = ("Bluetooth LE Session", Category.FRAMEWORK_USAGE)  # added if missing

    def __new__(cls, value: str, category: Category) -> "ReportName":
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj._category = category
        return obj

    @property
    def category(self) -> Category:
        return self._category


# Usage Example
# print(ReportType.APP_DOWNLOADS_STANDARD.value)   # "App Downloads Standard"
# print(ReportType.APP_DOWNLOADS_STANDARD.category)  # Category.COMMERCE