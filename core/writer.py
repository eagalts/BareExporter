def writer(values: list, search_item, label_name: str = None, metric_gauge: Gauge = None):
    if metric_gauge is not None:
        for item in values:
            if item[search_item] is not None:
                if label_name is not None:
                    metric_gauge.labels(**{label_name: item["Name"]}).set(item[search_item])
                else:
                    metric_gauge.set(item[search_item])