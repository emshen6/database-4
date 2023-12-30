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

# Выполнение запроса на добавление узлов
data = [
    ('OLT5300', 4, 2),
    ('Arista6300', 7, 3),
    ('Arista7300', 8, 4),
    ('Arista8300', 9, 3),
]
cursor.executemany(
    """
    INSERT INTO node (model, district_id, provider_id)
    VALUES (%s, %s, %s);
    """,
    data,
)

cursor.execute(
    """
    SELECT * FROM node;
    """
)

# Закрытие курсора
cursor.close()

# Отключение от базы данных
connection.close()