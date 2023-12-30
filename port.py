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


# Создать курсор
cursor = connection.cursor()

data = [
        (33, 1, None, 1, 'up', 1000, 'Port 1', 'Link up'),
        (33, 2, None, 2, 'down', 0, 'Port 2', 'Link down'),
        (33, 3, 1, 2, 'up', 1000, 'Port 3', 'Link up'),

        (34, 1, None, 1, 'up', 1000, 'Port 1', 'Link up'),
        (34, 2, 4, 2, 'up', 1000, 'Port 2', 'Link up'),
        (34, 3, None, 2, 'down', 0, 'Port 3', 'Link down'),

        (35, 1, None, 1, 'up', 100, 'Port 1', 'Link up'),
        (35, 2, None, 2, 'up', 100, 'Port 2', 'Link up'),
        (35, 3, 5, 2, 'up', 1000, 'Port 3', 'Link up'),

        (36, 1, None, 1, 'up', 1000, 'Port 1', 'Link up'),
        (36, 2, None, 3, 'up', 0, 'Port 2', 'Link down'),
        (36, 3, 8, 3, 'up', 10, 'Port 3', 'Link up'),

        (37, 1, None, 1, 'up', 1000, 'Port 1', 'Link up'),
        (37, 2, 6, 3, 'up', 0, 'Port 2', 'Link down'),
        (37, 3, None, 3, 'up', 100, 'Port 3', 'Link up'),

        (38, 1, None, 1, 'up', 1000, 'Port 1', 'Link up'),
        (38, 2, None, 3, 'up', 1000, 'Port 2', 'Link up'),
        (38, 3, None, 3, 'down', 0, 'Port 3', 'Link down'),

        (39, 1, None, 1, 'up', 1000, 'Port 1', 'Link up'),
        (39, 2, None, 3, 'up', 1000, 'Port 2', 'Link up'),
        (39, 3, 7, 3, 'up', 1000, 'Port 3', 'Link up')
    ]

cursor.executemany(
        'INSERT INTO port (switch_id, port_number, address_id, vlan_id, port_status, connection_speed, description, connection_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
        data
    )

# Зафиксировать изменения в базе данных
connection.commit()

# Закрыть соединение с базой данных
connection.close()