from bot.rateCommand import rateCommand
from bot.userCommand import userCommand
from utility.utility import get_ds_token
from discord.ext import commands


client = commands.Bot(command_prefix="!")
client.add_cog(userCommand(client))
client.add_cog(rateCommand(client))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print('------')


if __name__ == '__main__':
    client.run(get_ds_token())