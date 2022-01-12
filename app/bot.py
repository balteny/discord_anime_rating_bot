from discord.ext import commands
from mal import get_mal_page, get_more_mal_page, Mal_response, Anime
from typing import List
import json


mal_url = 'myanimelist.net'

anisearch_url = 'anisearch.de'


bot = commands.Bot(command_prefix="!")


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


@bot.command(name='rate', help='Rate an anime from myanimelist.net')
async def anime_rating(ctx):
    print(ctx.message.content)
    if ctx.author == bot.user:
        return

    if ctx.message.content.startswith('!rate'):
        if mal_url in ctx.message.content:
            # https://myanimelist.net/anime/<mal_id>/<anime_name>
            # id ab stelle 30 der url
            anime_id = ctx.message.content[36:ctx.message.content.find('/', 36)]
            print("Anime id: " + anime_id)
            for user in load_users():
                score = check_data(get_mal_page(user["user_id"]), int(anime_id), user["user_id"])
                if score == -1:
                    await ctx.channel.send(user["username"] + ' hat diesen Anime noch nicht bewertet.')
                else:
                    await ctx.channel.send(user["username"] + ': ' + str(score))
            return


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')


def runBot():
    bot.run(get_ds_token())
