from discord.ext import commands
from discord.ext.commands import context
from database.user import Users
from sqlalchemy import exc


class userCommand(commands.Cog):
    @commands.command(name='addUser', help='add a user to the database, model: !addUser <username> <mal_user_id>')
    async def addUser(self, ctx: context, username: str = None, user_id: str = None):
        if None in (username, user_id):
            await ctx.send("No username or user_id given")
            return
        try:
            Users.add_user(username=username, user_id=user_id)
        except (ValueError, exc.SQLAlchemyError) as e:
            print(e)
            await ctx.channel.send(f"Error while adding user {username} to database")
            return

        await ctx.channel.send(f"User {username} added to the database")

        return



    @commands.command(name='deleteUser', help='delete a user from the database, model: !deleteUser <mal_user_id>')
    async def deleteUser(self, ctx: context, user_id: str = None):
        if user_id is None:
            await ctx.channel.send("No user id given")
            return
        try:
            Users.delete_user(user_id=user_id)
        except (ValueError, exc.SQLAlchemyError) as e:
            print(e)
            await ctx.channel.send(f"Error while deleting user with id {user_id} from database")
            return

        await ctx.channel.send(f"User {user_id} deleted from the database")

        return

    @commands.command(name='getUsers', help='get all users from the database')
    async def getUsers(self, ctx: context):
        try:
            users = Users.get_users()
        except (ValueError, exc.SQLAlchemyError) as e:
            print(e)
            await ctx.channel.send(f"Error while getting all user from database")
            return

        for user in users:
            await ctx.channel.send(f"username: {user.name} - mal_id: {user.mal_username}")

        return
