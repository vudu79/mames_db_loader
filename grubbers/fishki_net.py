import json
from logs import get_logger
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup

from database import db_connect


def fishkinet_pars(uri_part: str):
    logger = get_logger(__name__)
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
                            db_connect(img_url, "https://fishki.net")

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
