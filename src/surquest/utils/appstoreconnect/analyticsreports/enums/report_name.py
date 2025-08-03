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

    def __new__(cls, value: str, category: Category) -> "ReportType":
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