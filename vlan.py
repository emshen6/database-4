import psycopg2
from sshtunnel import SSHTunnelForwarder

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

# Заполнить данные в таблицу vlan
data = [
    (1, 'VLAN1'),
    (2, 'VLAN2'),
    (3, 'VLAN3'),
    (4, 'VLAN4'),
    (5, 'VLAN5'),
]
cursor.executemany('INSERT INTO vlan (id, name) VALUES (%s, %s)', data)

# Зафиксировать изменения в базе данных
connection.commit()

# Закрыть соединение с базой данных
connection.close()