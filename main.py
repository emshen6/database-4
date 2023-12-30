import psycopg2
from sshtunnel import SSHTunnelForwarder
import io

import hashlib
import string
import random
from datetime import datetime

from make_diagnostics import make_diagnostics
from make_request import make_request
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



def add_address(cursor, town, district, street, house_number, porch, floor, flat):
    query = '''SELECT id FROM district WHERE town=%s AND district=%s;'''
    cursor.execute(query, (town, district))
    id = cursor.fetchone()

    if not(id):
        query = '''INSERT INTO district (town, district) VALUES (%s, %s) RETURNING id;'''
        cursor.execute(query, (town, district))
        district_id = cursor.fetchone()[0]
    else:
        district_id = id[0]

    query = '''SELECT id FROM house WHERE district_id=%s AND street=%s AND number=%s;'''
    cursor.execute(query, (district_id, street, house_number))
    id = cursor.fetchone()

    if not(id):
        query = '''INSERT INTO house (district_id, street, number) VALUES (%s, %s, %s) RETURNING id;'''
        cursor.execute(query, (district_id, street, house_number))
        house_id = cursor.fetchone()[0]
    else:
        house_id = id[0]

    query = '''SELECT id FROM address WHERE house_id=%s AND flat=%s;'''
    cursor.execute(query, (house_id, flat))
    id = cursor.fetchone()

    if not(id):
        query = '''INSERT INTO address (house_id, porch, floor, flat) VALUES (%s, %s, %s, %s) RETURNING id;'''
        cursor.execute(query, (house_id, porch, floor, flat))
        return cursor.fetchone()[0]
    else:
        return id[0]
    
def get_address(cursor, town, district, street, house_number, porch, floor, flat):
    query = '''SELECT id FROM district WHERE town=%s AND district=%s;'''
    cursor.execute(query, (town, district))
    id = cursor.fetchone()

    if not(id):
        return None
    else:
        district_id = id[0]

    query = '''SELECT id FROM house WHERE district_id=%s AND street=%s AND number=%s;'''
    cursor.execute(query, (district_id, street, house_number))
    id = cursor.fetchone()

    if not(id):
        return None
    else:
        house_id = id[0]

    query = '''SELECT id FROM address WHERE house_id=%s AND flat=%s;'''
    cursor.execute(query, (house_id, flat))
    id = cursor.fetchone()

    if not(id):
        return None
    else:
        return int(id[0])
    

def add_abonent(cursor, login, account_number, name, surname, phone_number, email, status, address_id, note):
    print('Choose provider id (1 - Ростелеком, 2 - Етелеком, 3 - Тиера, 4 - Скайнет):')
    provider_id = int(input())
    query = '''INSERT INTO abonent (login, account_number, name, surname, phone_number, email, status, address_id, note, provider_id) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;'''
    cursor.execute(query, (login, account_number, name, surname, phone_number, email, status, address_id, note, provider_id))

def add_switch(cursor, ip, model, port_count, house_id, provider_id, uplink_port):
    query = '''INSERT INTO switch(ip, model, port_count, house_id, provider_id, uplink_port) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;'''
    cursor.execute(query, (ip, model, port_count, house_id, provider_id, uplink_port))
    return cursor.fetchone()[0]



if __name__ == '__main__':
    server.start()

    conn = psycopg2.connect(user=REMOTE_USERNAME, database='studs', password='IUkanShc6DhfHo7x', host='localhost', port=10022)

    cursor = conn.cursor()
    name ="Дмитрий"
    surname = "Борисов"

    cursor.execute("""SELECT id FROM abonent WHERE (name=%s and surname=%s)""", (name, surname))

    abonent_id= cursor.fetchone()[0]


    diagnostics_id = make_diagnostics(cursor, conn, abonent_id, 1)
    cursor.execute(
    """
    SELECT * FROM connection_diagnostics WHERE id = %s
    """, (diagnostics_id, ))
    print(cursor.fetchone())
    print()

    text = " 172.40.34.1:5 Линка нет, ошибок нет, потерь нет, по диагностике кабеля разрыв во второй паре"

    request_id = make_request(cursor, conn, name, surname, 1, "Нет доступа к сети", text)


    conn.commit()
    cursor.close()
    conn.close()