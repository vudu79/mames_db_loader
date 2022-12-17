import json
import logging
import os

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from database.db import db_connect, db_insert


def fishkinet_pars(uri_part: str):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # настройка обработчика и форматировщика для logger2
    handler = logging.FileHandler(filename=os.path.join(os.path.abspath(os.curdir), "logs", 'fishki.log'), mode='w')
    formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    # добавление форматировщика к обработчику
    handler.setFormatter(formatter)
    # добавление обработчика к логгеру
    logger.addHandler(handler)

    mem_info_dict = dict()
    memes_list = list()
    ua = UserAgent()

    headers = {
        "user-agent": ua.chrome
    }

    domen = "https://fishki.net"
    print(headers["user-agent"])
    for x in range(1, 206):
        uri_string = f"/{uri_part}/{x}"

        url_string = domen + uri_string
        print(url_string)
        try:
            res = requests.get(url_string, headers=headers)
            if res.status_code == 200:
                print(res.status_code)
                logger.info(f'Рабатаю со страницей - {x}')
                print(f'Рабатаю со страницей - {x}')
                soup = BeautifulSoup(res.text, "lxml")
                img_divs = soup.find_all("div", class_="slide__item")

                for img_div in img_divs:
                    try:
                        img_url = img_div.find("img").get("src")
                        print(img_url)
                        if img_url:
                            mem_info_dict["name"] = None
                            mem_info_dict["img"] = img_url
                            buffer = mem_info_dict.copy()
                            memes_list.append(buffer)
                            mem_info_dict.clear()
                            db_insert(img_url, "https://fishki.net")

                    except Exception as eeee:
                        print(f"Проблеммы с отдельным изображением - {eeee}")
                        logger.error(f"Проблеммы с отдельным изображением - {eeee}")
                    finally:
                        continue

        except Exception as e:
            print(e)
            logger.error(f"Проблеммы с requests на странице с мемами - {e}")

    try:
        with open("../json_files/fishkinet_memes.json", "w", encoding="utf-8") as f:
            json.dump(memes_list, f, indent=4, ensure_ascii=False)
        logger.info(f"В итоговом файле {len(memes_list)} записей")
    except Exception as ee:
        logger.error(f"Проблеммы с записью в файл - {ee}")

    return "Завершен парсинг сайта https://fishki.net"



# if __name__ == "__main__":
#     # logger.basicConfig(level=logger.INFO, filename="../logs/memesmix_log.log", filemode="w",
#     # format="%(asctime)s %(levelname)s %(message)s")
#
#     logger.basicConfig(level=logger.INFO, filename="../logs/fishkinet_log.log", filemode="w",
#                         format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
#
#     fishkinet_pars("kartinka-dnja")
