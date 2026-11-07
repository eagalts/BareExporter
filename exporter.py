import json
import time
import urllib3

from systemd import daemon
from prometheus_client import start_http_server

from core.writer import writer
from core.builder import builder
from core.auth import BASIC_AUTH
from metrics import gauge as gauges
from agent.runner import runner as run_command
from parameters.param import PARAM_PORT, POLL_INTERVAL

# ===========================================================

# Отключаем предупреждения о небезопасных запросах
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===========================================================

## Проверка, что у нас присутствуют все необходимые параметры

for param, value in BASIC_AUTH.items():
    if value is None:
        raise SystemExit(f"[ERROR] {param} not defined.")

if not BASIC_AUTH['REDFISH_BASE_URL'].startswith(('http://', 'https://')):
    raise SystemExit(f"[ERROR] URL must be contains 'http://' or 'https://'.")

# ==========================================================

redfish_first_request = BASIC_AUTH["REDFISH_BASE_URL"] + "/redfish/v1/"

# Запуск HTTP-сервера 
start_http_server(PARAM_PORT)

# ==========================================================

daemon.notify("READY=1")

while True:
    # запрос
    redfish_main = run_command(
        redfish_first_request, 
        auth_creds=(BASIC_AUTH['REDFISH_USER'], BASIC_AUTH['REDFISH_PASSWORD']), 
        verify_ssl=False
    )

    if redfish_main[0] is None:
        status = None
    elif 'RedfishVersion' in redfish_main[0]:
        status = 1.0
    else:
        status = 0.0
    
    builder(
        redfish_main[1],
        status,
        gauge = gauges.current_redfish_status,
    )

    # sensors + fans

    redfish_sensors = run_command(
        BASIC_AUTH["REDFISH_BASE_URL"] + "/redfish/v1/Chassis/System.Embedded.1/Thermal", 
        auth_creds=(BASIC_AUTH['REDFISH_USER'], BASIC_AUTH['REDFISH_PASSWORD']), 
        verify_ssl=False
    )
    
    if (redfish_sensors[0] is not None):
        values = json.loads(redfish_sensors[0])

        writer(
            values = values["Temperatures"],
            search_item = "ReadingCelsius",
            label_name = "sensor",
            metric_gauge = gauges.current_redfish_temperature_celsius,
        )

        writer(
            values = values["Fans"],
            search_item = "Reading",
            label_name = "fan",
            metric_gauge = gauges.current_redfish_fans_rpm,
        )

    daemon.notify("WATCHDOG=1")
    time.sleep(POLL_INTERVAL)
    
