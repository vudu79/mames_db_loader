import json
import logging

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


def memesmix_pars(uri_part: str):
    mem_info_dict = dict()
    memes_list = list()
    ua = UserAgent()

    headers = {
        "user-agent": ua.chrome
    }

    domen = "http://memesmix.net"
    print(headers["user-agent"])
    for x in range(1, 34295):
        uri_string = f"/{uri_part}/{x}"
        url_string = domen + uri_string
        # print(uri + " " + str(datetime.datetime.now()))
        try:
            res = requests.get(url_string, headers=headers)
            # print(res.text)
            if res.status_code == 200:
                print(res.status_code)
                logging.info(f'Рабатаю со страницей - {x}')
                soup = BeautifulSoup(res.text, "lxml")
                divs = soup.find_all("div", id="grid-image")
                # print(divs)
                for div in divs:
                    name = div.find("div", class_="char-name").find("a")
                    mem_info_dict["name"] = name.text if name else None
                    mem_info_dict["img"] = div.find("img").get("src")
                    buffer = mem_info_dict.copy()
                    memes_list.append(buffer)
                    mem_info_dict.clear()

        except Exception as e:
            print(e)
            logging.error(f"Проблеммы с requests на странице с мемами - {e}")
    try:
        with open("memes.json", "w", encoding="utf-8") as f:
            json.dump(memes_list, f, indent=4, ensure_ascii=False)
        logging.info(f"В итоговом файле {len(memes_list)} записей")
    except Exception as ee:
        logging.error(f"Проблеммы с записью в файл - {ee}")


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, filename="../logs/memesmix_log.log", filemode="w",
    # format="%(asctime)s %(levelname)s %(message)s")

    logging.basicConfig(level=logging.INFO, filename="../logs/memesmix_log.log", filemode="w",
                        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    memesmix_pars("images/popular/alltime")
