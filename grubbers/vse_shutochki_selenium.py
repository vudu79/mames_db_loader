import logging
import os
from selenium import webdriver
from fake_useragent import UserAgent
import time
from datetime import datetime
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.devtools.v85.indexed_db import Key

from database import db_connect


def vse_shutochki_pars():
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
                            db_connect(img_url, "https://vse-shutochki.ru")
                        except Exception as exep:
                            logging.error(f'Ошибка при записи в файл - {exep}')
                            print(exep)
                        finally:
                            continue

                    except Exception as ex:
                        logging.error(f'Ошибка в цикле по сбору ссылок - {ex}')
                        print(ex)
                    finally:
                        continue
                total_time = datetime.now() - start
                print(
                    f'Страница {page}. Загрузилось {count}, общее количество ссылок {len(url_list)}. Время {total_time}')
                logging.info(
                    f'Страница {page}. Загрузилось {count}, общее количество {len(url_list)} ссылок. Время {total_time}')

                html.send_keys(Keys.PAGE_DOWN)
                time.sleep(3)

        except Exception as eee:
            print(eee)
            logging.error(f'Ошибка в работе селениум - {eee}')
        finally:
            driver.close()
            driver.quit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="../logs/vse_shutochki_log.log", filemode="w",
                        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    vse_shutochki_pars()
