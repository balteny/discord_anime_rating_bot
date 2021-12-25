import os
import discord
import requests
from dotenv import load_dotenv
import json


load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')

mal_url = 'myanimelist.net'

anisearch_url = 'anisearch.de'

mal_api_url = 'https://api.jikan.moe/v3'

def load_users():
    with open('users.json') as file:
        d = json.load(file)
        print(d["users"])
        return d["users"]

def get_mal_page(user_id, page):
    r = requests.get(mal_api_url + '/user/' + str(user_id) + '/animelist/completed/' + str(page))
    return r.json()["anime"]


def check_anime_included(anime_id, animes):
    return any(int(anime["mal_id"]) == int(anime_id) for anime in animes)


def get_score(animes, anime_id):
    for anime in animes:
        if int(anime["mal_id"]) == int(anime_id):
            return anime["score"]


def check_data(animes, anime_id, user_id, current_page):
    if check_anime_included(anime_id, animes):
        print("Found anime for " + user_id)
        return get_score(animes, anime_id)

    if len(animes) == 300:
        # die API liefert max 300 Einträge pro Seite zurück
        print("Getting data from page: " + str(current_page + 1))
        return check_data(get_mal_page(user_id, current_page + 1), anime_id, user_id, current_page + 1)

    print("Did not found Anime: " + anime_id + " for user: " + user_id)
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
                    score = check_data(get_mal_page(user["user_id"], 1), anime_id, user["user_id"], 1)
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
            # get users.json content
            # write new entry to content 
            # save file 
            # send message if user was sucessfully added
        if message.content.startswith('!deleteUser'):
            print("delete user")
            # delete auf username oder auf user_id?
            # get users.json content
            # find entry
            # delete entry 
            # write new content to file
            # send message if sucessfully deleted



if __name__ == '__main__':
    client = CustomClient()
    client.run(BOT_TOKEN)
