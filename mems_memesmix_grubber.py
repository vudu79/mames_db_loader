import json
import logging
from random import shuffle
from database.db import db_connect


def make_list() -> list:
    memesmix_list = list()
    bugaga_list = list()
    total_list = list()
    pinterest_list = list()

    pint_dict = {
        "name": "",
        "img": ""
    }

    with open("json_files/result.txt", "r", encoding="utf-8") as file:
        pinterest = file.readlines()
    for x in pinterest:
        pint_dict["img"] = x.strip()
        pint_dict["name"] = ""
        pinterest_list.append(pint_dict.copy())
        pint_dict.clear()

    with open("json_files/memesmix_memes.json", "r", encoding="utf-8") as file:
        memesmix_list = json.load(file)

    with open("json_files/bugaga_memes.json", "r", encoding="utf-8") as file:
        bugaga_list = json.load(file)

    total_list = [*memesmix_list, *bugaga_list, *pinterest_list]
    # total_list = [*bugaga_list]
    shuffle(total_list)
    print(len(pinterest_list))
    print(len(memesmix_list))
    print(len(bugaga_list))
    print(len(total_list))

    with open("json_files/result_memes.json", "w", encoding="utf-8") as file:
        json.dump(total_list, file, ensure_ascii=False, indent=4)

    return total_list




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="logs/memes_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

    db_connect(make_list())
