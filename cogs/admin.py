import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.qu = bot.qu
        self.system = bot.system


    @commands.command()
    async def qu(self,ctx):
        try:
            print(self.system.questions[str(ctx.channel.id)])
        except KeyError:
            print("KeyError had occurred")

    @commands.command()
    async def an(self,ctx):
        try:
            print(self.system.answers[str(ctx.channel.id)])
        except KeyError:
            print("KeyError had occurred")

    @commands.command()
    async def on(self,ctx):
        print(self.system.on)

    @commands.command()
    async def reset(self,ctx):
        await self.db.reset()
        await ctx.send("ポイントを初期化しました")





def setup(bot):
    bot.add_cog(Admin(bot))
