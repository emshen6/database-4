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


# Выполнение запроса на объединение таблиц
cursor.execute(
    """
    SELECT
        district.id,
        district.town,
        district.district,
        house.id,
        house.street,
        house.number,
        address.id,
        address.porch,
        address.floor,
        address.flat
    FROM district
    INNER JOIN house ON district.id = house.district_id
    INNER JOIN address ON house.id = address.house_id
    """
)

# Получение результатов запроса
results = cursor.fetchall()

# Закрытие курсора
cursor.close()

# Отключение от базы данных
connection.close()


header = ["district_id", "town", "district", "house_id", "street", "number", "address_id", "porch", "floor", "flat"]

data = pd.DataFrame(results, columns=header)
print(data)
