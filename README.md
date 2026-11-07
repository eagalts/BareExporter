# BareExporter

Prometheus-экспортёр для BMC по Redfish 

## Как работает

```
Prometheus ──GET /metrics──► exporter.py :9436
                                  │  (HTTP-сервер в фоновом потоке)
                                  │
                       цикл опроса в главном потоке
                                  │  GET /redfish/v1/ раз в N секунд
                                  ▼
                               iDRAC
```

- `/metrics` отдаёт последние значения из памяти, поэтому скрейп быстрый даже при медленном iDRAC.
- Опрос идёт по своему расписанию, независимо от скрейпов: два Prometheus не удваивают нагрузку на BMC.
- Ошибка опроса не роняет процесс: метрика доступности становится `0`, причина пишется в лог.

## Метрики

| Метрика | Тип | Labels | Описание |
|---|---|---|---|
| `current_redfish_status` | gauge | — | `1`, если `/redfish/v1/` ответил и в ответе есть `RedfishVersion`, иначе `0` |
| `metrics_redfish_time_to_answer_seconds` | histogram | — | длительность ответа от redfish в секундах |
| `current_redfish_tta` | gauge | — | метрика, которая показывает, за какое время ответил Redfish на запрос в секундах |
| `redfish_last_poll_timestamp_seconds` | gauge | — | метрика, которая показывает, когда пришел последний ответ от Redfish |
| `current_redfish_temperature_celsius` | gauge | `sensor` | метрика, которая показывает температуру в градусах Цельсия |
| `current_redfish_fans_rpm` | gauge | `fan` | метрика, которая показывает RPM (частота вращений) вентиляторов |
| `current_redfish_power_health` | gauge | `psu` | `1`, если `psu`-метрика (электропитание) в норме (OK), иначе `0` (Warning/Error/Critical) |

## Требования

- Python 3
- `prometheus_client`, `requests`

На Debian, если pip не достаёт до PyPI:

```bash
sudo apt install python3-prometheus-client python3-requests
```

Иначе:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install prometheus_client requests
```

## Настройка

Через переменные окружения. Все обязательны, значений по умолчанию нет.

| Переменная | Пример | Описание |
|---|---|---|
| `REDFISH_BASE_URL` | `https://10.0.40.10` | Адрес BMC со схемой `http://` или `https://` |
| `REDFISH_USER` | `root` | Пользователь Redfish |
| `REDFISH_PASSWORD` | — | Пароль |

Если переменная не задана или URL без схемы, экспортёр сразу завершается с `[ERROR]`.

## Запуск

```bash
REDFISH_BASE_URL=https://<bmc> REDFISH_USER=root REDFISH_PASSWORD='...' python3 exporter.py
```

Проверка:

```bash
curl -s localhost:9436/metrics | grep redfish
```

## Известные ограничения

- Проверка TLS отключена (`verify=False`): у iDRAC самоподписанный сертификат.
- Интервал опроса (5 с), порт (9436) и таймаут запроса (15 с) пока заданы в коде.
- Только чтение: экспортёр делает исключительно `GET`.