import os
import time
import urllib3
import requests
from prometheus_client import start_http_server, Gauge, Histogram

# Отключаем предупреждения о небезопасных запросах
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================================

PARAM_PORT = 9436
PARAM_FLUSH = True

# ==========================================================

REDFISH_TIMEOUT_REQUEST = 15
REDFISH_TTA_BUCKETS = [1,3,4,5,6,7,8,9,10,12,15]
POLL_INTERVAL = 60

# ==========================================================

def run_command(redfish_request, auth_creds, verify_ssl):
    answer = None
    start = time.monotonic()

    try:
        redfish_answer = requests.get(
            redfish_request, 
            auth=auth_creds, 
            verify=verify_ssl,
            timeout=REDFISH_TIMEOUT_REQUEST,
        )
        answer = redfish_answer.text
    except requests.RequestException as e:
        print(f"[WARN] {REDFISH_AUTH['REDFISH_BASE_URL']} <{e}>", flush = PARAM_FLUSH)
    finally:
        end = time.monotonic()

    return (answer, float(end - start))

def builder(
    time_to_answer,
    redfish_answer
):
    if (redfish_answer is not None):
        # определить current_redfish_status
        current_redfish_status.set(1.0 if 'RedfishVersion' in redfish_answer else 0.0)
        metrics_redfish_time_to_answer_seconds.observe(time_to_answer)
        redfish_last_poll_timestamp_seconds.set(time.time())
    else:
        current_redfish_status.set(0.0)
    current_redfish_tta.set(time_to_answer)
    

# ==========================================================

REDFISH_AUTH = {
    'REDFISH_BASE_URL': os.environ.get("REDFISH_BASE_URL"),
    'REDFISH_USER': os.environ.get("REDFISH_USER"),
    'REDFISH_PASSWORD': os.environ.get("REDFISH_PASSWORD")
}

# ===========================================================

current_redfish_status = Gauge(
    'current_redfish_status', 
    'Метрика, которая показывает, доступен ли Redfish (1) или нет (0).'
)
current_redfish_tta = Gauge(
    'current_redfish_tta', 
    'Метрика, которая показывает, за какое время ответил Redfish на запрос.'
)
redfish_last_poll_timestamp_seconds = Gauge(
    'redfish_last_poll_timestamp_seconds', 
    'Метрика, которая показывает, когда пришел последний ответ от Redfish.'
)
metrics_redfish_time_to_answer_seconds = Histogram(
    'metrics_redfish_time_to_answer_seconds', 
    'Метрика, которая показывает, за какое время ответил Redfish на запрос.',
    buckets=REDFISH_TTA_BUCKETS
)


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

# Запуск HTTP-сервера 
start_http_server(PARAM_PORT)

# ==========================================================

while True:
    # запрос
    redfish_main = run_command(
        redfish_first_request, 
        auth_creds=(REDFISH_AUTH['REDFISH_USER'], REDFISH_AUTH['REDFISH_PASSWORD']), 
        verify_ssl=False
    )

    builder(
        redfish_main[1],
        redfish_main[0]
    )
    
    time.sleep(POLL_INTERVAL)
    
