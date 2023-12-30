import psycopg2
from sshtunnel import SSHTunnelForwarder
import pandas as pd

PORT = 5432
REMOTE_USERNAME = 's312637'
REMOTE_HOST = 'helios.cs.ifmo.ru'
REMOTE_SSH_PORT = 2222
REMOTE_PASSWORD = 'XVQI.2552'

server = SSHTunnelForwarder((REMOTE_HOST, REMOTE_SSH_PORT),
         ssh_username=REMOTE_USERNAME,
         ssh_password=REMOTE_PASSWORD,
         remote_bind_address=('192.168.10.80', PORT),
         local_bind_address=('localhost', 10022))


server.start()

# Подключиться к базе данных
connection = psycopg2.connect(user=REMOTE_USERNAME, database='studs', password='IUkanShc6DhfHo7x', host='localhost', port=10022)


cursor = connection.cursor()


# Выполнение запроса на объединение таблиц
cursor.execute(
    """
    SELECT *
    FROM switch
    """
)

# Получение результатов запроса
results = cursor.fetchall()

# Закрытие курсора
cursor.close()

# Отключение от базы данных
connection.close()


header = ["id", "ip", "model", "port_count", "house_id", "provider_id", "uplink_port", "node_id"]

data = pd.DataFrame(results, columns=header)
print(data)
