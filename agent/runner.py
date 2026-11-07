import time
import requests

from core.auth import BASIC_AUTH
from parameters.param import PARAM_FLUSH
from parameters.redfish import REDFISH_TIMEOUT_REQUEST

def runner(redfish_request, auth_creds, verify_ssl):
    answer = None
    start = time.monotonic()

    try:
        redfish_answer = requests.get(
            redfish_request, 
            auth=auth_creds, 
            verify=verify_ssl,
            timeout=REDFISH_TIMEOUT_REQUEST,
        )
        redfish_answer.raise_for_status()
        answer = redfish_answer.text
    except requests.RequestException as e:
        print(f"[WARN] {BASIC_AUTH['REDFISH_BASE_URL']} <{e}>", flush = PARAM_FLUSH)
    finally:
        end = time.monotonic()

    return (answer, float(end - start))