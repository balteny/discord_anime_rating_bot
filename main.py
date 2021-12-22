import discord
import requests

BOT_TOKEN = 'OTIyNDU2OTE4NTkxNjk2OTQ2.YcBu8w.kaID8YSBWcaUL1YuGv94D_RfNC4'

mal_url = 'myanimelist.net'

anisearch_url = 'anisearch.de'

mal_api_url = 'https://api.jikan.moe/v3'

users = [
    {
        "user_id": "nellow25",
        "username": "Moritz"
    },
    {
        "user_id": "m4rcLs",
        "username": "Marcel"
    },
    {
        "user_id": "hansklumberte",
        "username": "Christopher"
    }
]


def get_initial_mal_anime_list(user_id):
    r = requests.get(mal_api_url + '/user/' + user_id + '/animelist/completed')
    return r.json()["anime"]


def get_more_mal_pages(user_id, page):
    r = requests.get(mal_api_url + '/user/' + str(user_id) + '/animelist/completed/' + str(page))
    return r.json()["anime"]


def check_data(animes, anime_id, user_id, current_page):
    if any(int(anime["mal_id"]) == int(anime_id) for anime in animes):
        print("Found anime for " + user_id)
        for anime in animes:
            if int(anime["mal_id"]) == int(anime_id):
                return anime["score"]
                break
    if len(animes) >= 300:
        print(user_id + " has more than 300 entries")
        print("Getting data from page: " + current_page + 1)
        data = get_more_mal_pages(user_id, current_page + 1)
        return check_data(data, anime_id, user_id, current_page + 1)

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
                data = get_initial_mal_anime_list(user["user_id"])
                score = check_data(data, anime_id, user["user_id"], 1)
                if score == -1:
                    await message.channel.send(user["username"] + ' hat diesen Anime noch nicht bewertet.')
                else:
                    await message.channel.send(user["username"] + ': ' + str(score))


client = CustomClient()
client.run(BOT_TOKEN)
