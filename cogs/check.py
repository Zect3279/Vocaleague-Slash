import discord
from discord.ext import commands

class Check(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.db = bot.db
        self.system = bot.system



    @commands.Cog.listener()
    async def on_message(self, message):

        self.na = message.author
        chan = message.channel.id
        # DEBUG: print(0)
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


def setup(bot):
    bot.add_cog(Check(bot))
