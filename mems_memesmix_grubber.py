import json
import logging
from random import shuffle
from database.db import db_connect


def make_list() -> list:
    # memesmix_list = list()
    bugaga_list = list()
    # pinterest_list = list()
    fishki_list = list()
    demotos_list = list()
    zaebovnet_list = list()
    anekdot_list = list()

    total_list = list()
    pint_dict = {
        "name": "",
        "img": ""
    }

    with open("json_files/anekdot_memes.txt", "r", encoding="utf-8") as file:
        pinterest = file.readlines()
    for x in pinterest:
        # pint_dict["img"] = x.strip()
        # pint_dict["name"] = ""
        anekdot_list.append(x)
        # pint_dict.clear()

    # with open("json_files/memesmix_memes.json", "r", encoding="utf-8") as file:
    #     memesmix_list = json.load(file)

    with open("json_files/bugaga_memes.json", "r", encoding="utf-8") as file:
        bugaga_list = json.load(file)

    with open("json_files/demotos_memes.json", "r", encoding="utf-8") as file:
        demotos_list = json.load(file)

    with open("json_files/fishkinet_memes.json", "r", encoding="utf-8") as file:
        fishki_list = json.load(file)
    with open("json_files/zaebovnet_memes.json", "r", encoding="utf-8") as file:
        zaebovnet_list = json.load(file)

    total_list = [*bugaga_list, *demotos_list, *fishki_list, *zaebovnet_list]
    shuffle(total_list)
    # print(len(pinterest_list))
    # print(len(memesmix_list))
    # print(len(bugaga_list))
    # print(len(fishki_list))
    # print(len(demotos_list))
    # print(len(zaebovnet_list))

    an = set()
    an.update(anekdot_list)
    print(len(anekdot_list))
    print(len(an))
    # print(len(total_list))
    #
    # with open("json_files/result_memes.json", "w", encoding="utf-8") as file:
    #     json.dump(total_list, file, ensure_ascii=False, indent=4)

    return total_list


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="logs/memes_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

    make_list()
    # db_connect(make_list())
