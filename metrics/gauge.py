from prometheus_client import Gauge

redfish_up = Gauge(
    'redfish_up', 
    'Метрика, которая показывает, доступен ли Redfish (1) или нет (0).'
)
redfish_last_poll_duration_seconds = Gauge(
    'redfish_last_poll_duration_seconds', 
    'Метрика, которая показывает, за какое время ответил Redfish на запрос.'
)
redfish_last_success_timestamp_seconds = Gauge(
    'redfish_last_success_timestamp_seconds', 
    'Метрика, которая показывает, когда пришел последний ответ от Redfish.'
)
redfish_temperature_celsius = Gauge(
    'redfish_temperature_celsius', 
    'Метрика, которая показывает температуру.',
    ["sensor"]
)
redfish_fan_speed_rpm = Gauge(
    'redfish_fan_speed_rpm', 
    'Метрика, которая показывает RPM (частота вращений) вентиляторов.',
    ["fan"]
)
redfish_power_health = Gauge(
    'redfish_power_health', 
    'Метрика, которая показывает состояние блоков питания.',
    ["psu"]
)
redfish_drive_health = Gauge(
    'redfish_drive_health', 
    'Метрика, которая показывает здоровье дисков.',
    ["drive"]
)
redfish_drive_failure_predict = Gauge(
    'redfish_drive_failure_predict', 
    'Метрика, которая показывает прогноз отказа дисков.',
    ["drive"]
)

redfish_sel_entries = Gauge(
    'redfish_sel_entries', 
    'Метрика, которая показывает число записей в SEL по серьёзности.',
    ["severity"]
)