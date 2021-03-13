import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, cog_ext, SlashContext
from discord_slash.utils import manage_commands

import asyncio

from lib.qu import Vocaleague

class SlashVQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.qu = bot.qu
        self.system = bot.system
        self.bot.slash.get_cog_commands(self) # コマンドを取得する
        # asyncio.create_task(self.bot.slash.sync_all_commands()) # 同期してコマンドがDiscordに出るようにする

    # コマンドの定義はcog_ext.cog_slashデコレータを使う
    @cog_ext.cog_slash(
    name='vq',
    description='Vocaleague開始',
    guild_ids=[720566804094648330,808283612105408533,726233332655849514]
    )
    async def slash_say(self, ctx: SlashContext):

        if str(ctx.channel.id) in self.system.on:
            await ctx.send("すでに起動しています")

        # if ctx.author != self.bot.get_user(653785595075887104):
        #     await ctx.send("あなたには使用する権限がありません。 \nYou don't have the privilege to use this.")
        #     return

        await ctx.respond(eat=False) # eat=Falseでログを出す
        # txt = "Vocaleagueを開始します"
        # await ctx.send(content=txt, hidden=False) # hidden=Trueで実行した人のみにみえるように
        await Vocaleague(self.bot).start(ctx)

    def cog_unload(self):
      self.bot.slash.remove_cog_commands(self) # コマンド解放


    @commands.Cog.listener()
    async def on_message(self, message):

        self.na = message.author
        chan = message.channel.id
        # print(0)
        try:
            # print(1)
            if message.author == self.bot:
                # print(2)
                return
            if str(chan) not in self.system.on:
                # print(3)
                return
            if self.na in self.system.winners[str(chan)]:
                # print(4)
                return
            if message.content != self.system.answers[str(chan)]:
                # print(5)
                return

            await self.db.add_point(self.na)
            # print(6)

            self.system.winners[str(chan)].append(self.na)
            print(7)
            await message.add_reaction("⭕")
        except KeyError:
            # print("KeyError had occurred")
            return

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

def setup(bot):
    bot.add_cog(SlashVQ(bot))
