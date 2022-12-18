import json
import logging
from concurrent.futures import ThreadPoolExecutor
from random import shuffle
from grubbers.anecdot_ru_site import anecdot_pars
from grubbers.bugaga_site import bugag_pars
from grubbers.demotos_site import demotos_pars
from grubbers.fishki_net import fishkinet_pars
from grubbers.pinterest_site import pinterest_pars
from grubbers.vse_shutochki_selenium import vse_shutochki_pars
from grubbers.zaebov_net import zaebovnet_pars


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
    # print(len(vse_shutochki_list_))

    print(len(total_list))

    return total_list


def cron_meme_parse():
    parser_dict = [
        # (pinterest_pars, "смешные мемы на все случаи жизни"),
        # (bugag_pars, "jokes"),
        # (demotos_pars, ""),
        # (fishkinet_pars, "kartinka-dnja"),
        (vse_shutochki_pars, ""),
        # (zaebovnet_pars, "foto-prikoli"),
        (anecdot_pars, "random/mem"),
    ]

    with ThreadPoolExecutor(max_workers=3) as executor:
        future_list = []
        for parser in parser_dict:
            future = executor.submit(parser[0], parser[1])
            future_list.append(future)
        for f in future_list:
            print(f.result())


if __name__ == "__main__":
    cron_meme_parse()
