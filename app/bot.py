from discord.ext import commands
import discord
from mal import get_mal_page, get_more_mal_page, Mal_response, Anime
from typing import List
import json


mal_url = 'myanimelist.net'

anisearch_url = 'anisearch.de'


def get_ds_token():
    with open('./config/config.json') as file:
        d = json.load(file)
        return d["discord_token"]


def load_users():
    with open('./config/users.json') as file:
        d = json.load(file)
        print('loaded following users {}'.format(d["users"]))
        return d["users"]


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


class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('!rate'):
            if mal_url in message.content:
                # https://myanimelist.net/anime/<mal_id>/<anime_name>
                # id ab stelle 30 der url
                anime_id = message.content[36:message.content.find('/', 36)]
                print("Anime id: " + anime_id)
                for user in load_users():
                    score = check_data(get_mal_page(user["user_id"]), int(anime_id), user["user_id"])
                    if score == -1:
                        await message.channel.send(user["username"] + ' hat diesen Anime noch nicht bewertet.')
                    else:
                        await message.channel.send(user["username"] + ': ' + str(score))
                return
            if 'help' in message.content:
                await message.channel.send('Dieser Bot holt sich die jeweiligen Bewertungen von einem Anime heran, welchen man auf MyAnimeList bewertet hat.\nDafür einfach "!rate https://myanimelist.net/anime/<mal_id>/<anime_name>" schreiben.')
        if message.content.startswith('!addUser'):
            print("add user")
            # wie muss message aussehen?
            # maybe mal check?
            # via db (slqlight) adden
            # send message if user was sucessfully added
        if message.content.startswith('!deleteUser'):
            print("delete user")
            # delete auf username oder auf user_id?
            # via db deleten
            # send message if sucessfully deleted


client = CustomClient()

def runClient():
    client.run(get_ds_token())