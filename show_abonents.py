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


connection = psycopg2.connect(user=REMOTE_USERNAME, database='studs', password='IUkanShc6DhfHo7x', host='localhost', port=10022)


cursor = connection.cursor()


def show_abonents(cursor):
    cursor.execute(
        """
        SELECT
            abonent.id,
            abonent.login,
            abonent.name,
            abonent.surname,
            abonent.address_id,
            abonent.provider_id,
            house.id,
            district.id
        FROM abonent
        INNER JOIN address ON abonent.address_id = address.id
        INNER JOIN house ON address.house_id = house.id
        INNER JOIN district ON house.district_id = district.id
        """
    )

    results = cursor.fetchall()
    cursor.close()
    connection.close()
    header = ["abonent_id", "login", "name", "surname", "address_id", "provider_id", "house_id", "district_id"]

    data = pd.DataFrame(results, columns=header)
    print(data)
