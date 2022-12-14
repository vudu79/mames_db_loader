import psycopg2
from urllib.parse import urlparse
import datetime


def db_connect(memes_list: list):
    # f'host=127.0.0.1 port=5432 dbname=bot_db user=andrey password=SpkSpkSpk1979 connect_timeout=60'

    connection = psycopg2.connect(user="andrey",
                                  password="SpkSpkSpk1979",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="bot_db",
                                  connect_timeout=60)
    with connection:
        with connection.cursor() as cursor:
            create_table_query = '''CREATE TABLE IF NOT EXISTS memes
                                    (url TEXT PRIMARY KEY NOT NULL,
                                    title TEXT,
                                    like_count BIGINT,
                                    dislike_count BIGINT,
                                    source_site TEXT,
                                    add_time timestamp); '''
            # Execute a command: this creates a new table
            cursor.execute(create_table_query)

            for x in range(0, len(memes_list)):
            # for x in range(0, 300):
                domen_name = urlparse(memes_list[x]["img"]).scheme + "://" + urlparse(memes_list[x]["img"]).netloc
                values_tuple = (memes_list[x]["img"],
                                memes_list[x]["name"],
                                0, 0, domen_name, datetime.datetime.utcnow())

                insert_query = """ INSERT INTO memes (url, title, like_count, dislike_count, source_site, add_time)
                                VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (url) DO NOTHING"""
                cursor.execute(insert_query, values_tuple)

            #

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
