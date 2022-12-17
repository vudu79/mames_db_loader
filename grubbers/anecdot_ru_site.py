import json
import logging

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


def anecdot_pars(uri_part: str):
    mem_info_dict = dict()
    memes_list = list()
    ua = UserAgent()

    headers = {
        "user-agent": ua.chrome
    }
    domen = "https://www.anekdot.ru"
    print(headers["user-agent"])
    page = 0
    while True:
        page += 1
        uri_string = f"/{uri_part}/"

        url_string = domen + uri_string
        print(url_string)
        try:
            res = requests.get(url_string, headers=headers)
            if res.status_code == 200:
                print(res.status_code)
                logging.info(f'Рабатаю со страницей - {page}')
                print(f'Рабатаю со страницей - {page}')
                soup = BeautifulSoup(res.text, "lxml")
                img_divs = soup.find_all("div", class_="topicbox")

                for img_div in img_divs:
                    try:
                        img_url = img_div.find("div", class_="text").find("img").get("src")
                        print(img_url)
                        if img_url not in memes_list:
                            memes_list.append(img_url)
                            try:
                                with open("../json_files/anekdot_memes.txt", "a", encoding="utf-8") as f:
                                    f.write(f"{img_url}\n")
                                logging.info(f"В итоговом файле {len(memes_list)} записей")
                                print(f"В итоговом файле {len(memes_list)} записей")
                            except Exception as ee:
                                logging.error(f"Проблеммы с записью в файл - {ee}")


                    except Exception as eeee:
                        print(f"Проблеммы с отдельным изображением - {eeee}")
                        logging.error(f"Проблеммы с отдельным изображением - {eeee}")
                    finally:
                        continue

        except Exception as e:
            print(e)
            logging.error(f"Проблеммы с requests на странице с мемами - {e}")



if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, filename="../logs/memesmix_log.log", filemode="w",
    # format="%(asctime)s %(levelname)s %(message)s")

    logging.basicConfig(level=logging.INFO, filename="../logs/anekdot_log.log", filemode="w",
                        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    anecdot_pars("random/mem")
