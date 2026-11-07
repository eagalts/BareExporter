from prometheus_client import Histogram
from parameters.redfish import REDFISH_TTA_BUCKETS

metrics_redfish_time_to_answer_seconds = Histogram(
    'metrics_redfish_time_to_answer_seconds', 
    'Метрика, которая показывает, за какое время ответил Redfish на запрос.',
    buckets=REDFISH_TTA_BUCKETS
)