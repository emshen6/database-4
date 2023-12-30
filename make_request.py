import psycopg2
from sshtunnel import SSHTunnelForwarder
from datetime import datetime

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

def make_request(cursor, connection, abonent_name, abonent_surname, author_id, type, text):
    cursor.execute(
        """SELECT id FROM abonent WHERE (name = %s AND surname = %s)""", (abonent_name, abonent_surname)
    )

    abonent_id = cursor.fetchone()[0]

    create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Не выполнена"

    cursor.execute(
        """INSERT INTO request (abonent_id, author_id, create_date, status, type, text) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
        (abonent_id, author_id, create_date, status, type, text)
    )
    id = cursor.fetchone()[0]
    connection.commit()
    return id

def change_request_status(cursor, connection, author_id, request_id, new_status):
    cursor.execute("""UPDATE request SET status = %s WHERE id = %s""", (new_status, request_id))
    change_request_status_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""UPDATE request SET status_change_date = %s WHERE id = %s""", (change_request_status_date, request_id))
    connection.commit()


def add_comment(cursor, connection, author_id, request_id, text):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """INSERT INTO comment (request_id, date, text, employee_id) VALUES (%s, %s, %s, %s)""",
        (request_id, date, text, author_id)
    )
    connection.commit()

def close_request(cursor, request_id):
    cursor.execute("""UPDATE request SET status = %s WHERE id = %s""", ("Выполнена", request_id))
    connection.commit()

cursor.close()
connection.close()