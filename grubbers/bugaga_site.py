import json
import logging

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup

from database import db_connect


# сайт https://bugaga.ru
def bugag_pars(uri: str):
    mem_info_dict = dict()
    memes_list = list()
    ua = UserAgent()

    headers = {
        "user-agent": ua.chrome
    }

    domen = "https://bugaga.ru"
    # print(headers["user-agent"])
    for x in range(1, 29):
        uri_string = f"/{uri}/page/{x}"
        # print(uri + " " + str(datetime.datetime.now()))
        try:
            res = requests.get(domen + uri_string, headers=headers)
            if res.status_code == 200:
                logging.info(f'Рабатаю со страницей - {x}')
                soup = BeautifulSoup(res.text, "lxml")

                divs = soup.find_all("div", class_="w_news")
                for div in divs:
                    try:
                        pack_url = div.find("a", class_="ui-button dalee").get("href")

                        res = requests.get(pack_url, headers=headers)
                        if res.status_code == 200:
                            print(res.status_code)
                            print(f'Рабатаю с ссылкой - {pack_url}')
                            logging.info(f'Рабатаю с ссылкой - {pack_url}')
                            soup = BeautifulSoup(res.text, "lxml")
                            urls = soup.find("div", class_="w_cntn").find_all("a", class_="highslide")
                            paginate = soup.find("div", class_="navigation")
                            print(paginate)
                            print(len(urls))
                            if len(urls) > 0:
                                for a in urls:
                                    img_url = domen + a.find("img").get("src")
                                    mem_info_dict["name"] = ""
                                    mem_info_dict["img"] = img_url
                                    buffer = mem_info_dict.copy()
                                    memes_list.append(buffer)
                                    mem_info_dict.clear()
                                if paginate:
                                    paginate_urls = paginate.find_all("a")
                                    for pag_url in paginate_urls:
                                        res = requests.get(pag_url.get("href"), headers=headers)
                                        if res.status_code == 200:
                                            print(res.status_code)
                                            print(f'Рабатаю с ссылкой - {pack_url}')
                                            logging.info(f'Рабатаю с ссылкой - {pack_url}')
                                            soup = BeautifulSoup(res.text, "lxml")
                                            urls = soup.find("div", class_="w_cntn").find_all("a", class_="highslide")
                                            print(len(urls))
                                            if len(urls) > 0:
                                                for a in urls:
                                                    img_url = domen + a.find("img").get("src")
                                                    mem_info_dict["name"] = ""
                                                    mem_info_dict["img"] = img_url
                                                    buffer = mem_info_dict.copy()
                                                    memes_list.append(buffer)
                                                    mem_info_dict.clear()
                                                    db_connect(img_url, "https://bugaga.ru")

                    except Exception as e:
                        logging.error("проблемма с запросом на страницу мемов")

        except Exception as e:
            print(e)
            logging.error(f"Проблеммы с requests на странице со сборниками мемов - {e}")

    try:
        with open("bugaga_memes.json", "w", encoding="utf-8") as f:
            json.dump(memes_list, f, indent=4, ensure_ascii=False)
        logging.info(f'записал в файл {len(memes_list)} записей')
    except Exception as ee:
        logging.error(f"Проблеммы с записью в файл - {ee}")


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, filename="../logs/memes_buguga_log.log", filemode="w",
    #                     format="%(asctime)s %(levelname)s %(message)s")
    logging.basicConfig(level=logging.INFO, filename="../logs/memes_buguga_log.log", filemode="w",
                        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    # bugag_pars("/tags/%D0%BC%D0%B5%D0%BC%D1%8B")
    bugag_pars("jokes")
