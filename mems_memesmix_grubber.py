import datetime
import json
import logging
from random import shuffle
import psycopg2
from urllib.parse import urlparse

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


#
# def main():
#     mem_info_dict = dict()
#     memes_list = list()
#     ua = UserAgent()
#
#     headers = {
#         "user-agent": ua.chrome
#     }
#
#     domen = "http://memesmix.net"
#     print(headers["user-agent"])
#     for x in range(1, 34295):
#         uri = "/images/popular/alltime"
#         # print(uri + " " + str(datetime.datetime.now()))
#         try:
#             res = requests.get(domen + uri, headers=headers)
#             # print(res.text)
#             if res.status_code == 200:
#                 print(res.status_code)
#                 logging.info(f'Рабатаю со страницей - {x}')
#                 soup = BeautifulSoup(res.text, "lxml")
#                 divs = soup.find_all("div", id="grid-image")
#                 # print(divs)
#                 for div in divs:
#                     name = div.find("div", class_="char-name").find("a")
#                     mem_info_dict["name"] = name.text if name else None
#                     mem_info_dict["img"] = div.find("img").get("src")
#                     buffer = mem_info_dict.copy()
#                     memes_list.append(buffer)
#                     mem_info_dict.clear()
#                 print(memes_list)
#         except Exception as e:
#             print(e)
#             logging.error(f"Проблеммы с requests на странице с мемами - {e}")
#     try:
#         with open("memesmix_memes.json", "w", encoding="utf-8") as f:
#             json.dump(memes_list, f, indent=4, ensure_ascii=False)
#         logging.info(f"В итоговом файле {len(memes_list)} записей")
#     except Exception as ee:
#         logging.error(f"Проблеммы с записью в файл - {ee}")

def make_list() -> list:
    memesmix_list = list()
    bugaga_list = list()
    total_list = list()

    with open("memesmix_memes.json", "r", encoding="utf-8") as file:
        memesmix_list = json.load(file)

    with open("bugaga_memes.json", "r", encoding="utf-8") as file:
        bugaga_list = json.load(file)

    total_list = [*memesmix_list, *bugaga_list]
    # total_list = [*bugaga_list]
    shuffle(total_list)
    print(len(memesmix_list))
    print(len(bugaga_list))
    print(len(total_list))
    return total_list



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
                domen_name = urlparse(memes_list[x]["img"]).netloc
                values_tuple = (memes_list[x]["img"],
                                memes_list[x]["name"],
                                0, 0, domen_name, datetime.datetime.utcnow())

                insert_query = """ INSERT INTO memes (url, title, like_count, dislike_count, source_site, add_time)
                                VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (url) DO NOTHING"""
                cursor.execute(insert_query, values_tuple)



            #

            query = """select url, titl-e from memes LIMIT 20"""
            cursor.execute(query)
            record = cursor.fetchall()
            print(record[0][0])
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="memes_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

    db_connect(make_list())
