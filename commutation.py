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
    (1, 33, 71, "8-core"),
    (2, 34, 73, "8-core"),
    (3, 35, 77, "8-core"),
    (6, 36, 80, "8-core"),
    (4, 37, 82, "8-core"),
    (5, 39, 89, "8-core")
]

cursor.executemany(
    """
    INSERT INTO commutation (abonent_id, switch_id, port_id, cable_type) VALUES (%s, %s, %s, %s)
    """,
    data
)

cursor.execute(
    """
    SELECT * FROM billing;
    """
)

results = cursor.fetchall()
print(results)

connection.commit()
# Закрытие курсора
cursor.close()

# Отключение от базы данных
connection.close()
