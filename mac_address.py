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

    (71, '18-67-B0-51-5B-D2'),
    (73, '18-67-B0-51-5B-D3'),
    (77, '18-67-B0-51-5B-D4'),
    (80, '18-67-B0-51-5B-D5'),
    (82, '18-67-B0-51-5B-D6'),
    (89, '18-67-B0-51-5B-D7'),
]

cursor.executemany(
    """
    INSERT INTO mac_address (port_id, mac_address) VALUES (%s, %s)
    """,
    data
)

cursor.execute(
    """
    SELECT * FROM mac_address;
    """
)

results = cursor.fetchall()
print(results)
connection.commit()

# Закрытие курсора
cursor.close()

# Отключение от базы данных
connection.close()
