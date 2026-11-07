import time
from metrics import histogram as histogrames
from metrics import gauge as gauges

def builder(
    time_to_answer,
    value,
    gauge = None,
):
    if (value is not None):
        # определить redfish_up
        if (gauge is not None):
            gauge.set(value)
        histogrames.redfish_poll_duration_seconds.observe(time_to_answer)
        gauges.redfish_last_success_timestamp_seconds.set(time.time())
    else:
        if (gauge is not None):
            gauge.set(0.0)
    gauges.redfish_last_poll_duration_seconds.set(time_to_answer)