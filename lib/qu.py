# vq/vq.py

import discord
from discord.ext import commands

import json
import random
import asyncio



# vq.cmdから渡された引数を格納したリストの取得
# argvs = sys.argv


class Vocaleague(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.qu = bot.qu
        self.system = bot.system

        self.mem: Optional[str]= None  # メンバー ID（正解判定用）
        self.na: Optional[str] = None  # メンバー Name（正解判定用）


        # if argvs[2] != "all":
        #     self.ids = argvs[2]  # 参加者ID
        #     self.names = argvs[4]

    async def msg(self,txt):
        test = discord.Embed(title=self.pr,colour=0x1e90ff)
        test.add_field(name=txt, value="ボカリーグ", inline=True)
        # test.set_author(name="ボカリーグ", icon_url=discord.File("V.jpg"))
        self.ed = await self.chan.send(embed=test)

    async def think(self,time):
        for i in range(time):
            n = time - i
            txt = "\n思考時間 " + "■" * n
            await self.edit(txt)
            await asyncio.sleep(0.9)

    async def edit(self,txt):
        test = discord.Embed(title=self.pr,colour=0x1e90ff)
        test.add_field(name=txt, value="ボカリーグ", inline=True)
        # test.set_author(name="ボカリーグ", icon_url=discord.File("V.jpg"))
        await self.ed.edit(embed=test)


    async def start(self, ctx):

        many = 1
        time = 10
        chan = ctx.channel.id


        for i in range(many):
            self.chan = ctx.channel
            self.system.winners[str(chan)] = []

            await asyncio.sleep(1)

            numA = str(random.randint(1, 230))
            numB = int(random.randint(0,2))

            que = self.qu[numA]["Q"]

            self.pr = que[numB]
            self.system.answers[str(chan)] = self.qu[numA]["A"]

            print(self.system.answers[str(chan)])

            await self.msg("\n思考時間開始")
            await asyncio.sleep(0.5)
            await self.think(time)


            await self.edit("\n解答開始")
            self.system.on.append(str(chan))
            await asyncio.sleep(5)

            self.system.on.remove(str(chan))

            test = discord.Embed(title="回答終了\n解答：{}".format(self.system.answers[str(chan)]),colour=0x1e90ff)
            await self.chan.send(embed=test)

            win = self.system.winners[str(chan)]
            await asyncio.sleep(0.5)

            if len(win) == 0:
                await self.chan.send('正解者はいませんでした。')
            else:
                txt = "正解者は、\n```"
                for p in win:
                    txt += f"\n{p.name} さん"
                await self.chan.send(f"{txt}\n```\nの{len(win)}人です！")





















#
