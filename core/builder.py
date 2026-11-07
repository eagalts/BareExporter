import time
from metrics import histogram as histogrames
from metrics import gauge as gauges

def builder(
    time_to_answer,
    value,
    labels = None,
    gauge = None,
    histogram = None,
):
    if (value is not None):
        # определить current_redfish_status
        if (gauge is not None):
            gauge.set(value)
        histogrames.metrics_redfish_time_to_answer_seconds.observe(time_to_answer)
        gauges.redfish_last_poll_timestamp_seconds.set(time.time())
    else:
        if (gauge is not None):
            gauge.set(0.0)
    gauges.current_redfish_tta.set(time_to_answer)