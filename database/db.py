import datetime
import psycopg2


def db_connect():
    connection = psycopg2.connect(user="andrey",
                                  password="SpkSpkSpk1979",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="bot_db",
                                  connect_timeout=60)
    return connection


def db_insert(img_url: str, source: str):
    connection = db_connect()
    with connection:
        with connection.cursor() as cursor:
            create_table_query = '''CREATE TABLE IF NOT EXISTS memes
                                    (img_url TEXT PRIMARY KEY NOT NULL,
                                    source VARCHAR,
                                    like_count BIGINT,
                                    dislike_count BIGINT,
                                    add_time timestamp); '''
            # Execute a command: this creates a new table
            cursor.execute(create_table_query)
            values_tuple = (img_url, source, 0, 0, datetime.datetime.utcnow())
            insert_query = """ INSERT INTO memes (img_url,  source, like_count,dislike_count, add_time)
                            VALUES (%s, %s, %s, %s, %s) ON CONFLICT (img_url) DO NOTHING"""
            cursor.execute(insert_query, values_tuple)

            # query = """select url, title from memes LIMIT 20"""
            # cursor.execute(query)
            # record = cursor.fetchall()
            # print(record[0][0])
            # Itemprice = int(record)
            #
            # # find customer's ewallet balance
            # query = """select balance from ewallet where userId = 23"""
            # cursor.execute(query)
            # record = cursor.fetchone()[0]
            # ewalletBalance = int(record)
            # new_EwalletBalance = ewalletBalance
            # new_EwalletBalance -= Itemprice
            #
            # # Withdraw from ewallet now
            # sql_update_query = """Update ewallet set balance = %s where id = 23"""
            # cursor.execute(sql_update_query, (new_EwalletBalance,))
            #
            # # add to company's account
            # query = """select balance from account where accountId = 2236781258763"""
            # cursor.execute(query)
            # record = cursor.fetchone()
            # accountBalance = int(record)
            # new_AccountBalance = accountBalance
            # new_AccountBalance += Itemprice
            #
            # # Credit to  company account now
            # sql_update_query = """Update account set balance = %s where id = 2236781258763"""
            # cursor.execute(sql_update_query, (new_AccountBalance,))
            # print("Transaction completed successfully ")


def db_select_count():
    connection = db_connect()
    with connection:
        with connection.cursor() as cursor:
            query = """select count(*) from mames"""
            cursor.execute(query)
            count = cursor.fetchone()[0]
            return count
