import json
import logging
from random import shuffle
from database.db import db_connect


def make_list() -> list:
    # memesmix_list = list()
    bugaga_list = list()
    bugaga_list_ = list()
    # pinterest_list = list()
    fishki_list = list()
    fishki_list_ = list()
    demotos_list = list()
    demotos_list_ = list()
    zaebovnet_list = list()
    zaebovnet_list_ = list()
    anekdot_list_ = list()
    vse_shutochki_list_ = list()

    total_list = list()
    pint_dict = {
        "name": "",
        "img": ""
    }

    with open("json_files/anekdot_memes.txt", "r", encoding="utf-8") as file:
        pinterest = file.readlines()
    for x in pinterest:
        anekdot_list_.append(x.strip())

    with open("json_files/vse_shutochki.txt", "r", encoding="utf-8") as file:
        shutochki = file.readlines()
    for x in shutochki:
        vse_shutochki_list_.append(x.strip())

    # with open("json_files/memesmix_memes.json", "r", encoding="utf-8") as file:
    #     memesmix_list = json.load(file)

    with open("json_files/bugaga_memes.json", "r", encoding="utf-8") as file:
        bugaga_list = json.load(file)
    for x in bugaga_list:
        bugaga_list_.append(x["img"])

    with open("json_files/demotos_memes.json", "r", encoding="utf-8") as file:
        demotos_list = json.load(file)
    for x in demotos_list:
        demotos_list_.append(x["img"])

    with open("json_files/fishkinet_memes.json", "r", encoding="utf-8") as file:
        fishki_list = json.load(file)
    for x in demotos_list:
        fishki_list_.append(x["img"])

    with open("json_files/zaebovnet_memes.json", "r", encoding="utf-8") as file:
        zaebovnet_list = json.load(file)
    for x in zaebovnet_list:
        zaebovnet_list_.append(x["img"])

    total_list = [*bugaga_list_, *demotos_list_, *fishki_list_, *zaebovnet_list_, *anekdot_list_, *vse_shutochki_list_]
    shuffle(total_list)
    # print(len(pinterest_list))
    # print(len(memesmix_list))
    # print(len(bugaga_list))
    # print(len(fishki_list))
    # print(len(demotos_list))
    # print(len(zaebovnet_list))
    print(len(vse_shutochki_list_))

    print(len(total_list))

    return total_list


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="logs/memes_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

    # make_list()
    db_connect(make_list())
