import json

from core.writer import writer
from core.auth import BASIC_AUTH
from metrics import gauge as gauges
from agent.runner import runner as run_command
from parameters.param import VERIFY_SSL

def sel():
    redfish_sel = run_command(
        BASIC_AUTH["REDFISH_BASE_URL"] + "/redfish/v1/Managers/iDRAC.Embedded.1/Logs/Sel", 
        auth_creds=(BASIC_AUTH['REDFISH_USER'], BASIC_AUTH['REDFISH_PASSWORD']), 
        verify_ssl=VERIFY_SSL
    )
    
    if (redfish_sel[0] is not None):
        values = json.loads(redfish_sel[0])
        counter_of_events = {"Critical": 0, "Warning": 0, "OK": 0}

        for item in values["Members"]:
            counter_of_events[item["Severity"]] = counter_of_events.get(item["Severity"], 0) + 1

        events = []

        for severity, count in counter_of_events.items():
            events.append({"Name": severity, "Count": count})

        writer(
            values = events,
            search_item = "Count",
            label_name = "severity",
            metric_gauge = gauges.current_redfish_sel_entries,
        )