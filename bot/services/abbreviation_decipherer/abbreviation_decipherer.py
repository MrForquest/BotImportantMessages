import random
import re

import pymorphy2
import requests
from bs4 import BeautifulSoup

from database import database

ABBR_BASE_URL = "https://xn----7sbbfsshef0aedydgg4lyb.xn--p1ai"

morph_analyzer = pymorphy2.MorphAnalyzer()


def get_deciphers_from_abbr_page(page):
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find(id="cards-list-0")
    # поскольку на странице не сразу таблица, а только ссылка на неё, то сначала добываем url таблицы
    deciphers_raw_url = re.search(r"fetch\('\S*'\)", str(table)).group(0)[7:-2]
    deciphers_url = ABBR_BASE_URL + deciphers_raw_url
    page = requests.get(deciphers_url)
    # парсим таблицу
    soup = BeautifulSoup(page.text, "html.parser")
    p_deciphers = soup.findAll(class_="mx-2")
    deciphers = list()

    for dph in p_deciphers:
        norm_text = " ".join(dph.text.split())
        deciphers.append(norm_text)

    return deciphers


def get_deciphers(abbr):
    base_url = "https://xn----7sbbfsshef0aedydgg4lyb.xn--p1ai"
    url = f"{base_url}/a/{abbr}"
    main_abbr_page = requests.get(url)

    if main_abbr_page.status_code == 200:
        deciphers = get_deciphers_from_abbr_page(main_abbr_page)
        return 1, abbr, deciphers
    elif main_abbr_page.status_code == 404:
        search_url = f"{base_url}/s?q={abbr}"
        search_page = requests.get(search_url)
        soup = BeautifulSoup(search_page.text, "html.parser")
        groups = soup.find_all(class_="list-group")
        if len(groups) == 0:
            # если вообще ничего не нашли, то возвращаем пустой список
            return -1, None, list()

        imprecise_matches = groups[1].find_all(class_="list-group-item")
        # берём ссылку на случайную подходящую аббревиатуру
        imprecise_abbr_href = random.choice(imprecise_matches)["href"]
        imprecise_abbr_url = ABBR_BASE_URL + imprecise_abbr_href
        imprecise_abbr_page = requests.get(imprecise_abbr_url)
        deciphers = get_deciphers_from_abbr_page(imprecise_abbr_page)
        new_abbr = imprecise_abbr_href.split("/")[-1]
        return 0, new_abbr, deciphers
    else:
        assert ValueError(f"abbr: {abbr}\n code: {main_abbr_page.status_code}")
    # print(imprecise_matches[0]["href"])
    # return deciphers


def get_random_word_by_ps(ps, start_with=""):
    cursor = database.get_cursor()
    if ps == "ADJF":
        word = cursor.execute(
            f"""
            SELECT word FROM curse_words 
            WHERE (word LIKE '{start_with}%') AND (part_speech IN ('ADJF', 'PRTF'))
            ORDER BY RANDOM()
            LIMIT 1
            """
        ).fetchone()
    else:
        word = cursor.execute(
            f"""
            SELECT word FROM curse_words 
            WHERE (word LIKE '{start_with}%') AND (part_speech='{ps}')
            ORDER BY RANDOM()
            LIMIT 1
            """
        ).fetchone()
    cursor.close()
    if word:
        return word[0]
    else:
        return None


def adjf_noun_of_noun(abbr):
    try:
        noun1 = morph_analyzer.parse(
            get_random_word_by_ps("NOUN", start_with=abbr[1]),
        )[0]
        adjf1 = morph_analyzer.parse(
            get_random_word_by_ps("ADJF", start_with=abbr[0]),
        )[0]
        noun2 = morph_analyzer.parse(
            get_random_word_by_ps("NOUN", start_with=abbr[2]),
        )[0]
        gender1 = noun1.tag.gender
        res = "{0} {1} им. {2}".format(
            adjf1.inflect({"nomn", "sing", gender1}).word,
            noun1.inflect({"nomn", "sing"}).word,
            noun2.inflect({"gent"}).word.capitalize(),
        )
        return res
    except AttributeError:
        return None


def n_adjf_of_noun(abbr):
    try:
        abbr = abbr.lower()
        noun1 = morph_analyzer.parse(
            get_random_word_by_ps("NOUN", start_with=abbr[-1]),
        )[0]
        gender1 = noun1.tag.gender
        words = list()
        for i in range(len(abbr) - 1):
            ad = morph_analyzer.parse(
                get_random_word_by_ps("ADJF", start_with=abbr[i])
            )[0]
            words.append(ad.inflect({"nomn", gender1}).word)
        res = " ".join([w.capitalize() for w in words]) + " " + noun1.word.capitalize()
        return res
    except AttributeError:
        return None
