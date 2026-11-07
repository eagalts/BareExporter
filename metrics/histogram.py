from prometheus_client import Histogram
from parameters.redfish import REDFISH_TTA_BUCKETS

redfish_poll_duration_seconds = Histogram(
    'redfish_poll_duration_seconds', 
    'Метрика, которая показывает, за какое время ответил Redfish на запрос.',
    buckets=REDFISH_TTA_BUCKETS
)