from prometheus_client import Gauge

def writer(values: list, search_item, label_name: str = None, metric_gauge: Gauge = None, health_to_num: bool = False):
    for item in values:
        if item[search_item] is not None:
            if health_to_num:
                value = 1 if item[search_item] == "OK" else 0
            else:
                value = item[search_item]

            if metric_gauge is not None:
                _add_to_gauge(
                    value=value,
                    label_name=label_name,
                    label_value=item["Name"],
                    metric_gauge=metric_gauge
                )

def _add_to_gauge(value: float, label_name: str = None, label_value: str = None, metric_gauge: Gauge = None):
    if label_name is not None and label_value is not None:
            metric_gauge.labels(**{label_name: label_value}).set(value)
    else:
        metric_gauge.set(value)