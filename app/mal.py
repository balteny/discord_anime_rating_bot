import requests
from typing import List
import json


class List_status:
    def __init__(self, status: str, score: int, num_episodes_watched: int, is_rewatching: bool, updated_at: str):
        self.status = status
        self.score = score
        self.num_episodes_watched = num_episodes_watched
        self.is_rewatching = is_rewatching
        self.updated_at = updated_at


class Node:
    def __init__(self, id: int, title: str, main_picture):
        self.id = id
        self.title = title
        self.main_picture = main_picture


class Anime:
    def __init__(self, node: Node, list_status: List_status):
        self.node = node
        self.list_status = list_status


class Paging:
    def __init__(self, next: str, prev: str):
        self.next = next
        self.prev = prev


class Mal_response:
    def __init__(self, data: List[Anime], paging: Paging):
        self.data = data
        self.paging = paging


mal_api_url = 'https://api.myanimelist.net/v2'


def get_mal_token():
    with open('./config/config.json') as file:
        d = json.load(file)
        print('loaded following token {}'.format(d["mal_token"]))
        return d["mal_token"]


mal_client_id = get_mal_token()


def get_mal_page(user_id) -> Mal_response:
    url = "{}/users/{}/animelist?fields=list_status&status=completed&limit=300".format(mal_api_url, user_id)
    header = {'X-MAL-CLIENT-ID': mal_client_id}
    r = requests.get(url, headers=header)
    return Mal_response(r.json()["data"], r.json()["paging"])


def get_more_mal_page(url) -> Mal_response:
    header = {'X-MAL-CLIENT-ID': mal_client_id}
    r = requests.get(url, headers=header)
    return Mal_response(r.json()["data"], r.json()["paging"])
