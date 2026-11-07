from prometheus_client import Gauge

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
current_redfish_temperature_celsius = Gauge(
    'current_redfish_temperature_celsius', 
    'Метрика, которая показывает температуру.',
    ["sensor"]
)
current_redfish_fans_rpm = Gauge(
    'current_redfish_fans_rpm', 
    'Метрика, которая показывает RPM (частота вращений) вентиляторов.',
    ["fan"]
)
current_redfish_power_health = Gauge(
    'current_redfish_power_health', 
    'Метрика, которая показывает состояние блоков питания.',
    ["psu"]
)