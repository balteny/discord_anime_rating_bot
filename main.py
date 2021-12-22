import os
import discord
import requests
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')

mal_url = 'myanimelist.net'

anisearch_url = 'anisearch.de'

mal_api_url = 'https://api.jikan.moe/v3'


class User:
  def __init__(self, username, user_id):
    self.username = username
    self.user_id = user_id


users = [
    User("Moritz", "nellow25"),
    User("Marcel", "m4rcLs"),
    User("Christopher", "hansklumberte")
]


def get_initial_mal_anime_list(user_id):
    r = requests.get(mal_api_url + '/user/' + user_id + '/animelist/completed')
    return r.json()["anime"]


def get_more_mal_pages(user_id, page):
    r = requests.get(mal_api_url + '/user/' + str(user_id) + '/animelist/completed/' + str(page))
    return r.json()["anime"]


def check_anime_included(anime_id, animes):
    return any(int(anime["mal_id"]) == int(anime_id) for anime in animes)


def check_data(animes, anime_id, user_id, current_page):
    if check_anime_included(anime_id, animes):
        print("Found anime for " + user_id)
        for anime in animes:
            if int(anime["mal_id"]) == int(anime_id):
                return anime["score"]
                break

    if len(animes) == 300:
        # die API liefert max 300 Einträge pro Seite zurück
        print("Getting data from page: " + current_page + 1)

        return check_data(get_more_mal_pages(user_id, current_page + 1), anime_id, user_id, current_page + 1)

    print("Did not found Anime: " + anime_id + " for user: " + user_id)
    return -1


class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == client.user:
            return

        if mal_url in message.content:
            # https://myanimelist.net/anime/<mal_id>/<anime_name>
            # id ab stelle 30
            anime_id = message.content[30:message.content.find('/', 30)]
            print("Anime id: " + anime_id)
            for user in users:
                data = get_initial_mal_anime_list(user.user_id)
                score = check_data(data, anime_id, user.user_id, 1)
                if score == -1:
                    await message.channel.send(user.username + ' hat diesen Anime noch nicht bewertet.')
                else:
                    await message.channel.send(user.username + ': ' + str(score))


if __name__ == '__main__':
    client = CustomClient()
    client.run(BOT_TOKEN)
