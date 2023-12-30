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

def make_diagnostics(cursor, connection, abonent_id, employee_id):

    cursor.execute("""SELECT switch.id, switch.ip FROM switch INNER JOIN commutation ON commutation.abonent_id = %s WHERE switch.id = commutation.switch_id """, (abonent_id, ))
    
    switch = cursor.fetchall()[0]

    cursor.execute("""SELECT port.id, port.port_number FROM port INNER JOIN commutation ON commutation.abonent_id = %s WHERE port.id = commutation.port_id """, (abonent_id, ))

    port = cursor.fetchall()[0]

    cursor.execute("""SELECT connection_status, connection_speed FROM port WHERE id=%s""", (port[0],))

    link, link_type = cursor.fetchall()[0]

    cursor.execute("""SELECT mac_address FROM mac_address WHERE port_id=%s""", (port[0],))

    mac = cursor.fetchall()[0]

    has_link = False
    if (link == "Link up"):
        has_link = True

    has_mac = False
    if (mac):
        has_mac = True

    errors = 0
    errors_rise = False
    correct_vlan = True
    switch_loss=0

    data = (employee_id, switch[1], port[1], has_link, link_type, has_mac, errors, errors_rise, correct_vlan, switch_loss)

    cursor.execute(
            """INSERT INTO connection_diagnostics (employee_id, switch, port, has_link,link_type, has_mac, errors, errors_rise, correct_vlan, switch_loss) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
            data
        )
    id = cursor.fetchone()[0]
    connection.commit()
    return id

cursor.close()
connection.close()