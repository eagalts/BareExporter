import os
import time
import urllib3
import requests
from prometheus_client import start_http_server, Gauge

# Отключаем предупреждения о небезопасных запросах
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================================

REDFISH_AUTH = {
    'REDFISH_BASE_URL': os.environ.get("REDFISH_BASE_URL"),
    'REDFISH_USER': os.environ.get("REDFISH_USER"),
    'REDFISH_PASSWORD': os.environ.get("REDFISH_PASSWORD")
}

# ==========================================================

## Проверка, что у нас присутствуют все необходимые параметры

for param, value in REDFISH_AUTH.items():
    if value is None:
        raise SystemExit(f"[ERROR] {param} not defined.")

if not REDFISH_AUTH['REDFISH_BASE_URL'].startswith(('http://', 'https://')):
    raise SystemExit(f"[ERROR] URL must be contains 'http://' or 'https://'.")

# ==========================================================

redfish_first_request = REDFISH_AUTH["REDFISH_BASE_URL"] + "/redfish/v1/"

# ==========================================================

# Запуск HTTP-сервера на порту 9436
start_http_server(9436)

# ==========================================================

# определить current_redfish_status
current_redfish_status = Gauge('current_redfish_status', 'Метрика, которая показывает, доступен ли Redfish (1) или нет (0).')

while True:
    try:   
        # запрос
        redfish_main = requests.get(
            redfish_first_request, 
            auth=(REDFISH_AUTH['REDFISH_USER'], REDFISH_AUTH['REDFISH_PASSWORD']), 
            verify=False,
            timeout=15,
        )
        # проверка доступности redfish (проверяет только базовую доступность)
        if 'RedfishVersion' in redfish_main.text: current_redfish_status.set(1.0)
        else: current_redfish_status.set(0.0)
    except requests.RequestException as e:
        current_redfish_status.set(0.0)
        print(f"[WARN] {REDFISH_AUTH['REDFISH_BASE_URL']} inaccessible over the network <{e}>")
    finally:
        time.sleep(5)
    
