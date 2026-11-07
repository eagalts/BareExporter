import json

from core.writer import writer
from core.auth import BASIC_AUTH
from metrics import gauge as gauges
from agent.runner import runner as run_command
from parameters.param import VERIFY_SSL

def thermal():
    redfish_sensors = run_command(
        BASIC_AUTH["REDFISH_BASE_URL"] + "/redfish/v1/Chassis/System.Embedded.1/Thermal", 
        auth_creds=(BASIC_AUTH['REDFISH_USER'], BASIC_AUTH['REDFISH_PASSWORD']), 
        verify_ssl=VERIFY_SSL
    )
    
    if (redfish_sensors[0] is not None):
        values = json.loads(redfish_sensors[0])

        writer(
            values = values["Temperatures"],
            search_item = "ReadingCelsius",
            label_name = "sensor",
            metric_gauge = gauges.redfish_temperature_celsius,
        )

        writer(
            values = values["Fans"],
            search_item = "Reading",
            label_name = "fan",
            metric_gauge = gauges.redfish_fan_speed_rpm,
        )