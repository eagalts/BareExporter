import json

from core.writer import writer
from core.auth import BASIC_AUTH
from metrics import gauge as gauges
from agent.runner import runner as run_command
from parameters.param import VERIFY_SSL

def parse_psu(values):
    power_values = []
    for item in values["PowerSupplies"]:
        power_values.append({"Name": item["Name"], "State": item["Status"]["Health"]})
    return power_values

def psu():
    redfish_power = run_command(
        BASIC_AUTH["REDFISH_BASE_URL"] + "/redfish/v1/Chassis/System.Embedded.1/Power", 
        auth_creds=(BASIC_AUTH['REDFISH_USER'], BASIC_AUTH['REDFISH_PASSWORD']), 
        verify_ssl=VERIFY_SSL
    )

    if (redfish_power[0] is not None):
        values = json.loads(redfish_power[0])
        power_values = parse_psu(values=values)
        writer(
                values = power_values,
                search_item = "State",
                label_name = "psu",
                metric_gauge = gauges.redfish_power_health,
                health_to_num = True,
            )