import logging
import os
import time
from datetime import datetime
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from database.db import db_insert


def pinterest_pars(question: str):

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # настройка обработчика и форматировщика для logger2
    handler = logging.FileHandler(filename=os.path.join(os.path.abspath(os.pardir), "logs", 'pinterest.log'), mode='w')
    formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    # добавление форматировщика к обработчику
    handler.setFormatter(formatter)
    # добавление обработчика к логгеру
    logger.addHandler(handler)

    ua = UserAgent(verify_ssl=False,
                   fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={ua.chrome}')
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # driver = webdriver.Chrome(executable_path="/home/andrey/python/gif_bot/cron_tasks/chromedriver", options=options)
    driver = webdriver.Chrome(executable_path="chromedriver", options=options)
    url = 'https://ru.pinterest.com/'

    try:
        driver.get(url)
        time.sleep(10)
        button_enter = driver.find_element(By.XPATH,
                                           '//*[@id="fullpage-wrapper"]/div[1]/div/div/div[1]/div/div[2]/div[2]/button')

        button_enter.click()
        time.sleep(5)
        email = driver.find_element(By.ID, 'email')
        email.clear()
        email.send_keys('vudu-1979@yandex.ru')
        time.sleep(5)
        password = driver.find_element(By.ID, 'password')
        password.clear()
        password.send_keys('SpkSpkSpk1979')
        time.sleep(5)
        login_button = driver.find_element(By.XPATH,
                                           '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div/div/div[4]/form/div[7]/button')
        login_button.click()
        time.sleep(10)
        search_input = driver.find_element(By.TAG_NAME, 'input')
        search_input.clear()
        search_input.send_keys(question)
        search_input.send_keys(Keys.ENTER)
        time.sleep(5)

        url_list = list()
        start = datetime.now()
        file_size = 0.0
        page = 0
        while file_size < 200:
            driver.get(url=url)
            html = driver.find_element(By.TAG_NAME, "html")
            time.sleep(10)
            html.send_keys(Keys.PAGE_DOWN)
            time.sleep(10)

            page += 1
            img_divs = driver.find_elements(By.XPATH, "//*[@class='hCL kVc L4E MIw']")
            count = 0

            for img_div in img_divs:
                try:
                    img_url = img_div.get_attribute("src")
                    url_list.append(img_url)
                    count += 1

                    try:
                        db_insert(img_url, "https://ru.pinterest.com")

                        with open("pinterest.txt", "a", encoding="utf-8") as file:
                            file.write(f'{img_url}\n')
                        file_stats = os.stat("../json_files/pinterest.txt")
                        # file_size = file_stats.st_size / 1024:.2f
                        file_size = file_stats.st_size / (1024 * 1024)
                        print(f"размер файла {file_size}")

                    except Exception as exep:
                        logger.error(f'Ошибка при записи в файл - {exep}')
                        print(exep)

                except Exception as ex:
                    logger.error(f'Ошибка в цикле по сбору ссылок - {ex}')
                    print(ex)
                finally:
                    continue
            total_time = datetime.now() - start
            print(f'Итерация {page}. Загрузилось {count}, общее количество ссылок {len(url_list)}. Время {total_time}')
            logger.info(
                f'Итерация {page}. Загрузилось {count}, общее количество {len(url_list)} ссылок. Время {total_time}')
            # print(url_list)
            html.send_keys(Keys.F5)
            time.sleep(10)



    except Exception as eee:
        print(eee)
        logger.error(f'Ошибка в работе селениум - {eee}')
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="../logs/memes_log.log", filemode="w",
                        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    pinterest_pars("смешные мемы на все случаи жизни")
