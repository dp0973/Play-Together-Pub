from bot import PlayTogether


def load(bot: PlayTogether):
    cogs = ["error", "general", "ready", "room"]

    for cog in cogs:
        bot.load_extension(f"cogs.{cog}")
        
    bot.load_extension("jishaku")