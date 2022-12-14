import logging
import os
from selenium import webdriver
from fake_useragent import UserAgent
import time
from datetime import datetime
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.devtools.v85.indexed_db import Key


def pinterest_pars(question: str):
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
    # driver = webdriver.Chrome(executable_path="/home/andrey/python/selenium_grabber_memes/chromedriver", options=options)
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
        time.sleep(5)
        search_input = driver.find_element(By.TAG_NAME, 'input')
        search_input.clear()
        search_input.send_keys(question)
        search_input.send_keys(Keys.ENTER)
        time.sleep(5)

        driver.get(url=url)
        html = driver.find_element(By.TAG_NAME, "html")
        url_list = list()
        start = datetime.now()
        file_size = 0.0
        page = 0
        while file_size < 200:
            page += 1
            img_divs = driver.find_elements(By.XPATH, "//*[@class='hCL kVc L4E MIw']")
            count = 0

            for img_div in img_divs:
                try:
                    img_url = img_div.get_attribute("src")
                    url_list.append(img_url)
                    count += 1

                    try:
                        with open("result1.txt", "a", encoding="utf-8") as file:
                            file.write(f'{img_url}\n')
                        file_stats = os.stat("result1.txt")
                        # file_size = file_stats.st_size / 1024:.2f
                        file_size = file_stats.st_size / (1024 * 1024)
                        print(f"???????????? ?????????? {file_size}")

                    except Exception as exep:
                        logging.error(f'???????????? ?????? ???????????? ?? ???????? - {exep}')
                        print(exep)

                except Exception as ex:
                    logging.error(f'???????????? ?? ?????????? ???? ?????????? ???????????? - {ex}')
                    print(ex)
                finally:
                    continue
            total_time = datetime.now() - start
            print(f'???????????????? {page}. ?????????????????????? {count}, ?????????? ???????????????????? ???????????? {len(url_list)}. ?????????? {total_time}')
            logging.info(
                f'???????????????? {page}. ?????????????????????? {count}, ?????????? ???????????????????? {len(url_list)} ????????????. ?????????? {total_time}')
            # print(url_list)

            html.send_keys(Keys.PAGE_DOWN)
            time.sleep(3)

    except Exception as eee:
        print(eee)
        logging.error(f'???????????? ?? ???????????? ???????????????? - {eee}')
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="../logs/memes_log.log", filemode="w",
                        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    pinterest_pars("?????????????? ???????? ???? ?????? ???????????? ??????????")
