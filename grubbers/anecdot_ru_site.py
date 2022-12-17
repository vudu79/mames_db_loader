import json
import logging
import os
from logs import get_logger
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from database.db import db_connect


def anecdot_pars(uri_part: str):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # настройка обработчика и форматировщика для logger2
    handler = logging.FileHandler(f"../logs/{__name__}.log", mode='w')
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
    domen = "https://www.anekdot.ru"
    print(headers["user-agent"])
    page = 0
    file_size = 0
    while file_size < 300:
        page += 1
        uri_string = f"/{uri_part}/"

        url_string = domen + uri_string
        print(url_string)
        try:
            res = requests.get(url_string, headers=headers)
            if res.status_code == 200:
                print(res.status_code)
                logger.info(f'Рабатаю со страницей - {page}')
                print(f'Рабатаю со страницей - {page}')
                soup = BeautifulSoup(res.text, "lxml")
                img_divs = soup.find_all("div", class_="topicbox")

                for img_div in img_divs:
                    try:
                        img_url = img_div.find("div", class_="text").find("img").get("src")
                        print(img_url)
                        if img_url not in memes_list:
                            try:
                                db_connect(img_url, "https://www.anekdot.ru")

                                with open("../json_files/anekdot_memes.txt", "a", encoding="utf-8") as f:
                                    f.write(f"{img_url}\n")

                                file_stats = os.stat("../json_files/anekdot_memes.txt")
                                file_size = file_stats.st_size / (1024 * 1024)
                                logger.info(f"В итоговом файле {len(memes_list)} записей")
                                print(f"В итоговом файле {len(memes_list)} записей")

                            except Exception as ee:
                                logger.error(f"Проблеммы с записью в файл - {ee}")


                    except Exception as eeee:
                        print(f"Проблеммы с отдельным изображением - {eeee}")
                        logger.error(f"Проблеммы с отдельным изображением - {eeee}")
                    finally:
                        continue

        except Exception as e:
            print(e)
            logger.error(f"Проблеммы с requests на странице с мемами - {e}")

    return "Завершен парсинг https://www.anekdot.ru"

# if __name__ == "__main__":
#     # logger.basicConfig(level=logger.INFO, filename="../logs/memesmix_log.log", filemode="w",
#     # format="%(asctime)s %(levelname)s %(message)s")
#
#     logger.basicConfig(level=logger.INFO, filename="../logs/anekdot_log.log", filemode="w",
#                         format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

# anecdot_pars("random/mem")
