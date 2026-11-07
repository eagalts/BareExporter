import json

from core.writer import writer
from core.auth import BASIC_AUTH
from metrics import gauge as gauges
from agent.runner import runner as run_command
from parameters.param import VERIFY_SSL

def disk():
    redfish_drives = run_command(
        BASIC_AUTH["REDFISH_BASE_URL"] + "/redfish/v1/Systems/System.Embedded.1/Storage/RAID.Integrated.1-1", 
        auth_creds=(BASIC_AUTH['REDFISH_USER'], BASIC_AUTH['REDFISH_PASSWORD']), 
        verify_ssl=VERIFY_SSL
    )
    
    if (redfish_drives[0] is not None):
        values = json.loads(redfish_drives[0])

        drive_values = []

        for item in values["Drives"]:
            path = item["@odata.id"]
            current_drive = run_command(
                BASIC_AUTH["REDFISH_BASE_URL"] + path, 
                auth_creds=(BASIC_AUTH['REDFISH_USER'], BASIC_AUTH['REDFISH_PASSWORD']), 
                verify_ssl=VERIFY_SSL
            )

            if current_drive[0] is not None:
                drive = json.loads(current_drive[0])
                drive_values.append({"Name": drive["Name"], "Health": drive["Status"]["Health"], "FailurePredicted": drive["FailurePredicted"]})

        writer(
            values = drive_values,
            search_item = "Health",
            label_name = "drive",
            metric_gauge = gauges.redfish_drive_health,
            health_to_num=True,
        )

        writer(
            values = drive_values,
            search_item = "FailurePredicted",
            label_name = "drive",
            metric_gauge = gauges.redfish_drive_failure_predict,
        )