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
| `redfish_up` | gauge | — | `1`, если `/redfish/v1/` ответил и в ответе есть `RedfishVersion`, иначе `0` |
| `redfish_poll_duration_seconds` | histogram | — | длительность ответа от redfish в секундах |
| `redfish_last_poll_duration_seconds` | gauge | — | метрика, которая показывает, за какое время ответил Redfish на запрос в секундах |
| `redfish_last_success_timestamp_seconds` | gauge | — | метрика, которая показывает, когда пришел последний ответ от Redfish |
| `redfish_temperature_celsius` | gauge | `sensor` | метрика, которая показывает температуру в градусах Цельсия |
| `redfish_fan_speed_rpm` | gauge | `fan` | метрика, которая показывает RPM (частота вращений) вентиляторов |
| `redfish_power_health` | gauge | `psu` | `1`, если `psu`-метрика (электропитание) в норме (OK), иначе `0` (Warning/Error/Critical) |
| `redfish_drive_health` | gauge | `drive` | `1`, если `health`-метрика (состояние диска) в норме (OK), иначе `0` (Warning/Error/Critical) |
| `redfish_drive_failure_predict` | gauge | `drive` | `0`, если диск в норме (OK), иначе `1` (диск скоро умрет - требуется внимание к нему) |
| `redfish_sel_entries` | gauge | `severity` | количество записей в SEL по серьёзности |

## Требования

- Python 3
- `prometheus_client`
- `requests`
- `python3-systemd`

На Debian, если pip не достаёт до PyPI:

```bash
sudo apt install python3-prometheus-client python3-requests python3-systemd
```

Иначе:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install prometheus_client requests systemd-python
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

- Проверка TLS отключена (задается параметром `VERIFY_SSL`, по умолчанию `False`): у iDRAC самоподписанный сертификат.
- Интервал опроса (60 с - `POLL_INTERVAL`), порт (9436) и таймаут запроса (15 с) пока заданы в коде.
- Только чтение: экспортёр делает исключительно `GET`.