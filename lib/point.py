import discord
from discord.ext import commands
from discord_slash import SlashContext

class Point():
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.system = bot.system



    async def point(self, ctx, user: discord.User = None):
        target_user = user if user else ctx.author
        user_data = await self.db.get_user(target_user)
        if user_data is None:
            txt = "まだ登録されていません"
            return txt
        txt = f"{user_data.name} の所持ポイント\n{user_data.point} Point"
        return txt



    # async def ranking(self, ctx: SlashContext) -> None:
    #     users_ranking = await self.db.get_user_rankings()
    #     ranking_message = "```\n"
    #
    #     for user_ranking in users_ranking:
    #         user = self.bot.get_user(user_ranking[0])
    #         user_data = user_ranking[0]
    #
    #         ranking_message += f"{user_ranking[1]}位: {user_data.name}, Point: {user_data.point}\n"
    #
    #     if not discord.utils.find(lambda u: u[0].id == ctx.author.id, users_ranking):
    #         if rank := await self.db.get_user_ranking(ctx.author.id):
    #             user_data = await self.bot.db.get_user(ctx.author)
    #             ranking_message += f"\n{rank}位: {user_data.name}, Point: {user_data.point}"
    #
    #     txt = ranking_message + "```"
    #     return txt
