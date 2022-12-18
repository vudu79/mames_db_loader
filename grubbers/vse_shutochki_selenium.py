import logging
import os
import time
from datetime import datetime

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from database.db import db_connect, db_insert


def vse_shutochki_pars(uti: str):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # настройка обработчика и форматировщика для logger2
    handler = logging.FileHandler(filename=os.path.join(os.path.abspath(os.pardir), "logs", 'vse_shutochki.log'), mode='w')
    formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    # добавление форматировщика к обработчику
    handler.setFormatter(formatter)
    # добавление обработчика к логгеру
    logger.addHandler(handler)

    for page in range(1, 2822):
        ua = UserAgent(verify_ssl=False,
                       fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={ua.random}')
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        # driver = webdriver.Chrome(executable_path="/home/andrey/python/selenium_grabber_memes/chromedriver", options=options)
        driver = webdriver.Chrome(executable_path="chromedriver", options=options)
        # for page in range(1, 2):
        url = f'https://vse-shutochki.ru/kartinki-prikolnye/{page}'
        try:
            driver.get(url=url)
            html = driver.find_element(By.TAG_NAME, "html")
            time.sleep(10)
            for y in range(1):
                count = 0
                img_divs = driver.find_elements(By.XPATH, "//*[@class='post noSidePadding']")
                time.sleep(3)
                url_list = list()
                start = datetime.now()
                for img_div in img_divs:
                    try:
                        img_path = img_div.find_element(By.TAG_NAME, "img")
                        img_url = img_path.get_attribute("src")
                        print(img_url)
                        url_list.append(img_url)
                        count += 1
                        try:
                            db_insert(img_url, "https://vse-shutochki.ru")
                        except Exception as exep:
                            logger.error(f'Ошибка при записи в файл - {exep}')
                            print(exep)
                        finally:
                            continue

                    except Exception as ex:
                        logger.error(f'Ошибка в цикле по сбору ссылок - {ex}')
                        print(ex)
                    finally:
                        continue
                total_time = datetime.now() - start
                print(
                    f'Страница {page}. Загрузилось {count}, общее количество ссылок {len(url_list)}. Время {total_time}')
                logger.info(
                    f'Страница {page}. Загрузилось {count}, общее количество {len(url_list)} ссылок. Время {total_time}')

                html.send_keys(Keys.PAGE_DOWN)
                time.sleep(3)

        except Exception as eee:
            print(eee)
            logger.error(f'Ошибка в работе селениум - {eee}')
        finally:
            driver.close()
            driver.quit()
    return "Завершен парсинг сайта https://vse-shutochki.ru"


#
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="../logs/vse_shutochki_log.log", filemode="w",
                        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    vse_shutochki_pars("")
