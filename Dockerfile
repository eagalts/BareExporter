# === BUILD ===
FROM python:3.11 AS builder
# Добавляем метки для метаданных
LABEL maintainer="eagalts"
LABEL description="Prometheus exporter for Dell iDRAC 7 hardware metrics over Redfish"
# Создаем рабочий каталог в образе
WORKDIR /app
# Докачиваем недостающие пакеты libsystemd-dev и pkg-config
# для компиляции systemd-python, ибо в образе их нет
RUN apt-get update && apt-get install -y --no-install-recommends libsystemd-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*
# Копируем файл с зависимостями в рабочий каталог образа
COPY requirements.txt /app/requirements.txt
# Устанавливаем зависимости
RUN pip install --no-cache-dir --user -r requirements.txt

# === APP ===
# Устанавливаем базовый образ python 3.11 (slim)
FROM python:3.11-slim
# Добавляем переменные окружения
ENV PARAM_PORT=9436
ENV PARAM_FLUSH=True
ENV POLL_INTERVAL=60
ENV VERIFY_SSL=False
# Добавляем метки для метаданных
LABEL maintainer="eagalts"
LABEL description="Prometheus exporter for Dell iDRAC 7 hardware metrics over Redfish"
# Создаем рабочий каталог в образе
WORKDIR /app
# Копируем результат билда в рабочую директорию
COPY --from=builder /root/.local /root/.local
# Указываем PATH в переменные окружения
ENV PATH=/root/.local/bin:$PATH
# Копируем весь код в рабочую директорию
COPY . /app
# Объявляем порт
EXPOSE 9436
# Запускаем код
CMD ["python", "exporter.py"]