import pika

connection_params = pika.ConnectionParameters(
    host='rabbitmq',  # Замените на адрес вашего RabbitMQ сервера
    port=5672,          # Порт по умолчанию для RabbitMQ
    virtual_host='/',   # Виртуальный хост (обычно '/')
    credentials=pika.PlainCredentials(
        username="rmuser",  # Имя пользователя по умолчанию
        password="rmpassword"   # Пароль по умолчанию
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)