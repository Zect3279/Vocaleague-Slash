from bot import Zect
import setting

bot = Zect()

BOT_TOKEN = setting.BOT

extensions = [
    "cogs.admin",
    "cogs.check",
    "slash.vq",
    "slash.point",
    "slash.rank",
]
for extension in extensions:
    bot.load_extension(extension)

bot.run(BOT_TOKEN)
