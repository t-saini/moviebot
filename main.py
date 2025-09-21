from bot_actions import bot
import discord
import utility


def main():
    setup = utility.run_ini()
    DISCORD_TOKEN = setup['token']['value']
    bot.run(DISCORD_TOKEN)


main()
