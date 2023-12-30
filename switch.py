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


data = [
    ('172.40.30.1', 'DGS3000', 3, 2, 2, 1, 33),
    ('172.40.31.1', 'DGS3000', 3, 5, 3, 1, 34),
    ('172.40.32.1', 'DGS3000', 3, 6, 4, 1, 35),
    ('172.40.33.1', 'DGS3000', 3, 9, 3, 1, 36),
    ('172.40.34.1', 'DGS3000', 3, 7, 3, 1, 34),
    ('172.40.35.1', 'DGS3000', 3, 8, 3, 1, 34),
    ('172.40.35.2', 'DGS3000', 3, 8, 3, 1, 34)
]

cursor.executemany(
    '''
    INSERT INTO switch (ip, model, port_count, house_id, provider_id, uplink_port, node_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''',
    data,
)
connection.commit()

# Закрытие курсора
cursor.close()

# Отключение от базы данных
connection.close()