from typing import List
from api.mal import get_more_mal_page, Mal_response, Anime
import json


def get_anime_id(message):
    return message[30:message.find('/', 30)]


def check_anime_included(anime_id: int, animes: List[Anime]):
    return any(int(anime["node"]["id"]) == int(anime_id) for anime in animes)


def get_score(animes: List[Anime], anime_id: int):
    for anime in animes:
        if int(anime["node"]["id"]) == int(anime_id):
            return int(anime["list_status"]["score"])


def check_data(mal_response: Mal_response, anime_id: int, user_id: str):
    animes: List[Anime] = mal_response.data
    if check_anime_included(anime_id, animes):
        print("Found anime for " + user_id)
        return get_score(animes, anime_id)

    if len(animes) == 300:
        # die API liefert max 300 Einträge pro Seite zurück
        print("Getting data from page: " + mal_response.paging["next"])
        return check_data(get_more_mal_page(mal_response.paging["next"]), anime_id, user_id)

    print("Did not found Anime: " + str(anime_id) + " for user: " + user_id)
    return -1


def get_ds_token():
    with open('./config/config.json') as file:
        d = json.load(file)
        return d["discord_token"]


def get_db_path():
    with open('./config/config.json') as file:
        d = json.load(file)
        return d["db_path"]