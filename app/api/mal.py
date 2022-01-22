import requests
from typing import List, Optional
import json
from pydantic import BaseModel


class List_status(BaseModel):
    status: str
    score: int
    num_episodes_watched: int
    is_rewatching: bool
    updated_at: str

    def __getitem__(self, key):
        return getattr(self,key)


class Thumbnails(BaseModel):
    large: str
    medium: str

    def __getitem__(self, key):
        return getattr(self,key)

class Node(BaseModel):
    id: int
    title: str
    main_picture: Thumbnails

    def __getitem__(self, key):
        return getattr(self,key)

class Anime(BaseModel):
    node: Node
    list_status: List_status

    def __getitem__(self, key):
        return getattr(self,key)

class Paging(BaseModel):
    next: Optional[str]
    prev: Optional[str]

    def __getitem__(self, key):
        return getattr(self,key)

class Mal_response(BaseModel):
    data: List[Anime]
    paging: Paging

    def __getitem__(self, key):
        return getattr(self,key)


class AnimeInfo(BaseModel):
    id: int
    title: str
    main_picture: Thumbnails


mal_api_url = 'https://api.myanimelist.net/v2'


def get_mal_token():
    with open('./config/config.json') as file:
        d = json.load(file)
        print('loaded following token {}'.format(d["mal_token"]))
        return d["mal_token"]


mal_client_id = get_mal_token()


def get_mal_page(user_id: str) -> Mal_response:
    url = f"{mal_api_url}/users/{user_id}/animelist?fields=list_status&status=completed&limit=300"
    header = {'X-MAL-CLIENT-ID': mal_client_id}
    r = requests.get(url, headers=header)
    return Mal_response(data=r.json()["data"], paging=r.json()["paging"])


def get_more_mal_page(url: str) -> Mal_response:
    header = {'X-MAL-CLIENT-ID': mal_client_id}
    r = requests.get(url, headers=header)
    return Mal_response(data=r.json()["data"], paging=r.json()["paging"])


def get_anime_info(anime_id: str) -> AnimeInfo:
    header = {'X-MAL-CLIENT-ID': mal_client_id}
    url = f"{mal_api_url}/anime/{anime_id}?fields=main_picture,title"
    r = requests.get(url, headers=header)
    return AnimeInfo(id=r.json()["id"], title=r.json()["title"], main_picture=r.json()["main_picture"])