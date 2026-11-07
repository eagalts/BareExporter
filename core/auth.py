import os 

BASIC_AUTH = {
    'REDFISH_BASE_URL': os.environ.get("REDFISH_BASE_URL"),
    'REDFISH_USER': os.environ.get("REDFISH_USER"),
    'REDFISH_PASSWORD': os.environ.get("REDFISH_PASSWORD")
}