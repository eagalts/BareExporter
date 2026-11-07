import time
import urllib3

from systemd import daemon
from prometheus_client import start_http_server

from runners.psu import psu as psu
from runners.thermal import thermal as thermal
from runners.disk import disk as disk
from runners.sel import sel as sel

from core.builder import builder
from core.auth import BASIC_AUTH
from metrics import gauge as gauges
from agent.runner import runner as run_command
from parameters.param import PARAM_PORT, POLL_INTERVAL, VERIFY_SSL

# ===========================================================

# Отключаем предупреждения о небезопасных запросах
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===========================================================

RUNNERS = [
    thermal,    # Температура + скорость вращения вентиляторов
    psu,        # Power Supply (энергопотребление)
    disk,       # Состояние дисков, контроллера
    sel,        # System Event Log
]

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
        verify_ssl=VERIFY_SSL
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
        gauge = gauges.redfish_up,
    )

    for job in RUNNERS:
        try:
            job()
        except (KeyError, TypeError, ValueError) as e:
            print(f"[WARN] Task '{job.__name__}' failed: {e!r}", flush = True)
        
    daemon.notify("WATCHDOG=1")
    time.sleep(POLL_INTERVAL)