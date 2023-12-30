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

connection = psycopg2.connect(user=REMOTE_USERNAME, database='studs', password='IUkanShc6DhfHo7x', host='localhost', port=10022)

cursor = connection.cursor()

data = [
    (1, '2023-12-18 14:30:00', 71, 71, 71),
    (2, '2004-10-19 10:23:54', 73, 73, 73),
    (3, '2004-10-19 10:23:54', 77, 77, 77),
    (4, '2004-10-19 10:23:54', 80, 80, 80),
    (5, '2004-10-19 10:23:54', 82, 82, 82),
    (6, '2004-10-19 10:23:54', 89, 89, 89)
]

cursor.executemany(
    """
    INSERT INTO arp (id, create_date, port_id, node_id, vlan_id) 
    VALUES (%s, 
    %s,
    %s,
    (SELECT switch.node_id 
    FROM switch 
    INNER JOIN port ON switch.id = port.switch_id
    WHERE port.id = %s),
    (SELECT vlan_id FROM port WHERE id = %s)
    )
    """
    , data)

cursor.execute(
    """
    SELECT * FROM arp
    """)

results = cursor.fetchall()
print(results)

connection.commit()

cursor.close()
connection.close()