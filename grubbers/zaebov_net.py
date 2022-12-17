import json
import logging
import os

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from database.db import db_connect, db_insert


def zaebovnet_pars(uri_part: str):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # настройка обработчика и форматировщика для logger2
    handler = logging.FileHandler(filename=os.path.join(os.path.abspath(os.curdir), "logs", 'zaebov_net.log'), mode='w')
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

    domen = "https://zaebov.net"
    print(headers["user-agent"])
    for x in range(1, 27):
        uri_string = f"/{uri_part}/page/{x}" if x > 1 else f"/{uri_part}"
        url_string = domen + uri_string
        # print(uri + " " + str(datetime.datetime.now()))
        try:
            res = requests.get(url_string, headers=headers)
            # print(res.text)
            if res.status_code == 200:
                print(res.status_code)
                logger.info(f'Рабатаю со страницей - {x}')
                print(f'Рабатаю со страницей - {x}')
                soup = BeautifulSoup(res.text, "lxml")
                divs = soup.find_all("div", class_="entry-title")
                # print(divs)
                for div in divs:
                    img_page_url = div.find("a").get("href")
                    img_page_name = div.find("a").text
                    try:
                        res = requests.get(img_page_url, headers=headers)
                        # print(res.text)
                        if res.status_code == 200:
                            print(res.status_code)
                            logger.info(f'Рабатаю с набором мемов - {img_page_name}')
                            print(f'Рабатаю с набором мемов - {img_page_name}')
                            soup = BeautifulSoup(res.text, "lxml")
                            div_entry_content = soup.find("div", class_="entry-content")
                            pp = div_entry_content.find_all("p")
                            # print(pp)

                            for page in pp:
                                try:
                                    img_url = page.find("img").get("src")
                                    print(img_url)
                                    if img_url:
                                        db_insert(img_url, "https://zaebov.net")

                                except Exception as eeee:
                                    print(f"Проблеммы с отдельным изображением - {eeee}")
                                    logger.error(f"Проблеммы с отдельным изображением - {eeee}")
                                finally:
                                    continue

                    except Exception as eee:
                        print(f"Проблеммы с requests на странице с мемами - {eee}")
                        logger.error(f"Проблеммы с requests на странице с мемами - {eee}")

        except Exception as e:
            print(e)
            logger.error(f"Проблеммы с requests на странице с наборами - {e}")

    try:
        with open("../json_files/zaebovnet_memes.json", "w", encoding="utf-8") as f:
            json.dump(memes_list, f, indent=4, ensure_ascii=False)
        logger.info(f"В итоговом файле {len(memes_list)} записей")
    except Exception as ee:
        logger.error(f"Проблеммы с записью в файл - {ee}")

    return "Завершен парсинг сайта https://zaebov.net"

# if __name__ == "__main__":
#     # logger.basicConfig(level=logger.INFO, filename="../logs/memesmix_log.log", filemode="w",
#     # format="%(asctime)s %(levelname)s %(message)s")
#
#     logger.basicConfig(level=logger.INFO, filename="../logs/zaebovnet_log.log", filemode="w",
#                         format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
#
#     zaebovnet_pars("foto-prikoli")
