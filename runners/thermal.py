import json

from core.writer import writer
from core.auth import BASIC_AUTH
from metrics import gauge as gauges
from agent.runner import runner as run_command
from parameters.param import VERIFY_SSL

def parse_thermal(values):
    thermal_values = []
    fan_values = []

    for sensor in values["Temperatures"]:
        thermal_values.append({"Name": sensor["Name"], "Value": sensor["ReadingCelsius"]})

    for sensor in values["Fans"]:
            fan_values.append({"Name": sensor["Name"], "Value": sensor["Reading"]})

    return thermal_values, fan_values

def thermal():
    redfish_sensors = run_command(
        BASIC_AUTH["REDFISH_BASE_URL"] + "/redfish/v1/Chassis/System.Embedded.1/Thermal", 
        auth_creds=(BASIC_AUTH['REDFISH_USER'], BASIC_AUTH['REDFISH_PASSWORD']), 
        verify_ssl=VERIFY_SSL
    )
    
    if (redfish_sensors[0] is not None):
        values = json.loads(redfish_sensors[0])
        thermal_values, fan_values = parse_thermal(values)

        writer(
            values = thermal_values,
            search_item = "Value",
            label_name = "sensor",
            metric_gauge = gauges.redfish_temperature_celsius,
        )

        writer(
            values = fan_values,
            search_item = "Value",
            label_name = "fan",
            metric_gauge = gauges.redfish_fan_speed_rpm,
        )