import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, cog_ext, SlashContext
from discord_slash.utils import manage_commands

import asyncio

from lib.point import Point

class SlashRank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.qu = bot.qu
        self.system = bot.system
        self.bot.slash.get_cog_commands(self) # コマンドを取得する
        # asyncio.create_task(self.bot.slash.sync_all_commands()) # 同期してコマンドがDiscordに出るようにする

    # コマンドの定義はcog_ext.cog_slashデコレータを使う
    @cog_ext.cog_slash(
    name='ranking',
    description='Vocaleagueのポイントランキングを表示',
    guild_ids=[720566804094648330,808283612105408533,726233332655849514]
    )
    async def slash_say(self, ctx: SlashContext):


        # if ctx.author != self.bot.get_user(653785595075887104):
        #     await ctx.send("あなたには使用する権限がありません。 \nYou don't have the privilege to use this.")
        #     return

        await ctx.respond(eat=False) # eat=Falseでログを出す
        txt = await Point(self.bot).ranking(ctx)
        await ctx.send(content=txt, hidden=False) # hidden=Trueで実行した人のみにみえるように


    def cog_unload(self):
      self.bot.slash.remove_cog_commands(self) # コマンド解放


def setup(bot):
    bot.add_cog(SlashRank(bot))
