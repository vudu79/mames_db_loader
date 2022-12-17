import json
from logs import get_logger
import re

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup

from database import db_connect


def demotos_pars(uri_part: str):
    logger = get_logger(__name__)
    mem_info_dict = dict()
    memes_list = list()
    ua = UserAgent()

    headers = {
        "user-agent": ua.chrome
    }

    domen = "https://demotos.ru"
    print(headers["user-agent"])
    for x in range(1, 484):
    # for x in range(1, 2):
        uri_string = f"/{uri_part}/page/{x}" if x > 1 else f"/{uri_part}"
        url_string = domen + uri_string
        try:
            res = requests.get(url_string, headers=headers)
            if res.status_code == 200:
                print(res.status_code)
                logger.info(f'Рабатаю со страницей - {x}')
                print(f'Рабатаю со страницей - {x}')
                soup = BeautifulSoup(res.text, "lxml")
                main_divs = soup.find_all("div", class_=re.compile("views-row views-row-\d\d?.*"))

                for div in main_divs:
                    # print(div)
                    try:
                        img_url0 = div.find("div", class_="field-items")
                        img_url = img_url0.find("img").get("src") if img_url0 else None
                        name0 = div.find("span", class_="views-field views-field-title")
                        name = name0.find("span", class_="field-content").text if name0 else None
                        if img_url:
                            mem_info_dict["name"] = name
                            mem_info_dict["img"] = img_url
                            buffer = mem_info_dict.copy()
                            memes_list.append(buffer)
                            mem_info_dict.clear()
                            db_connect(img_url, "https://demotos.ru")
                    except Exception as eeee:
                        print(f"Проблеммы с отдельным изображением - {eeee}")
                        logger.error(f"Проблеммы с отдельным изображением - {eeee}")
                    finally:
                        continue

        except Exception as e:
            print(e)
            logger.error(f"Проблеммы с requests на странице с мамами № {x} - {e}")

    try:
        with open("../json_files/demotos_memes.json", "w", encoding="utf-8") as f:
            json.dump(memes_list, f, indent=4, ensure_ascii=False)
        logger.info(f"В итоговом файле {len(memes_list)} записей")
    except Exception as ee:
        logger.error(f"Проблеммы с записью в файл - {ee}")

    return "Завершен парсинг сайта https://demotos.ru"

# if __name__ == "__main__":
#     # logger.basicConfig(level=logger.INFO, filename="../logs/memesmix_log.log", filemode="w",
#     # format="%(asctime)s %(levelname)s %(message)s")
#
#     logger.basicConfig(level=logger.INFO, filename="../logs/demotos_log.log", filemode="w",
#                         format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
#
#     demotos_pars("")
