from api.mal import get_mal_page, get_anime_info
from utility.utility import check_data, get_anime_id
from database.user import Users

from discord.ext import commands
from discord.ext.commands import context
from discord import Embed, Color

from pydantic import BaseModel
from typing import List


mal_url = 'myanimelist.net'

anisearch_url = 'anisearch.de'


class UserScore(BaseModel):
    name: str
    score: int

    def __getitem__(self, key):
        return getattr(self,key)


def build_embed(anime_url: str, anime_title, thumbnail_url, user_scores: List[UserScore]):
    embed=Embed(title=f"Anime Rating: {anime_title}", url=anime_url, color=Color.blue())
    embed.set_thumbnail(url=thumbnail_url)

    for entry in user_scores:
        if entry.score == -1:
            embed.add_field(name=f"{entry.name} - Score: -", value="\u200B", inline=False)
            continue

        embed.add_field(name=f"{entry.name} - Score: {entry.score}", value="\u200B" ,inline=False)

    return embed


class rateCommand(commands.Cog):
    @commands.command(name='rate', help='Rate an anime from myanimelist.net')
    async def anime_rating(self, ctx: context, url: str = None):

        if url is None:
            await ctx.send("No url given")
            return

        user_scores = list()
        if mal_url in url:
            # https://myanimelist.net/anime/<mal_id>/<anime_name>
            # id ab stelle 30 der url
            anime_id = get_anime_id(url)
            print("Anime id: " + anime_id)
            anime = get_anime_info(anime_id)

            for user in Users.get_users():
                score = check_data(get_mal_page(user.mal_username), int(anime_id), user.mal_username)
                user_scores.append(UserScore(name=user.name, score=score))

            embed = build_embed(url, anime.title, anime.main_picture.large, user_scores)
            await ctx.channel.send(embed=embed)
            print("Anime rating sent")

        return
