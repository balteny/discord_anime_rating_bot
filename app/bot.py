from discord.ext import commands
from discord.ext.commands import context
from discord import Embed, Color
from mal import get_mal_page, get_more_mal_page, get_anime_info, Mal_response, Anime
from typing import List
import json
from pydantic import BaseModel


mal_url = 'myanimelist.net'

anisearch_url = 'anisearch.de'


bot = commands.Bot(command_prefix="!")


class UserScore(BaseModel):
    name: str
    score: int

    def __getitem__(self, key):
        return getattr(self,key)


class User(BaseModel):
    user_id: str
    username: str

    def __getitem__(self, key):
        return getattr(self,key)


class Users(BaseModel):
    users: List[User]

    def __getitem__(self, key):
        return getattr(self,key)


def get_ds_token():
    with open('./config/config.json') as file:
        d = json.load(file)
        return d["discord_token"]


def load_users() -> Users:
    with open('./config/users.json') as file:
        d = json.load(file)
        print(f'loaded following users {Users(users = d["users"])}')
        return Users(users = d["users"])


def get_anime_id(message):
    return message[36:message.find('/', 36)]


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


def build_embed(anime_url: str, anime_title, thumbnail_url, user_scores: List[UserScore]):
    embed=Embed(title=f"Anime Rating: {anime_title}", url=anime_url, color=Color.blue())
    embed.set_thumbnail(url=thumbnail_url)

    for entry in user_scores:
        if entry.score == -1:
            embed.add_field(name=f"{entry.name} - Score: -", value="\u200B", inline=False)
            continue

        embed.add_field(name=f"{entry.name} - Score: {entry.score}", value="\u200B" ,inline=False)

    return embed


@bot.command(name='rate', help='Rate an anime from myanimelist.net')
async def anime_rating(ctx: context):
    if ctx.author == bot.user:
        return

    user_scores = list()
    if mal_url in ctx.message.content:
        # https://myanimelist.net/anime/<mal_id>/<anime_name>
        # id ab stelle 30 der url
        anime_id = get_anime_id(ctx.message.content)
        print("Anime id: " + anime_id)
        anime = get_anime_info(anime_id)
        url = ctx.message.content[6:]

        for user in load_users().users:
            score = check_data(get_mal_page(user.user_id), int(anime_id), user.user_id)
            user_scores.append(UserScore(name=user.username, score=score))

        embed = build_embed(url, anime.title, anime.main_picture.large, user_scores)
        await ctx.channel.send(embed=embed)
        print("Anime rating sent")

    return


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')


def runBot():
    bot.run(get_ds_token())
