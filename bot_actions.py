#bot.py
#https://betterprogramming.pub/coding-a-discord-bot-with-python-64da9d6cade7

import discord
import csv
import utility
import random


# Initialize bot, intents, logger
intents = discord.Intents.default()
intents.members = True

bot = discord.Client(intents=intents)
logger = utility.system_logs()
with open('./movies.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    titles = [row['titles'] for row in reader]
with open('./watched.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    watched = [row['watched'] for row in reader]
    if watched is None:
        watched = []

MOVIES = {'titles': titles, 'watched':watched}

def check_movie(que_string, to_watch):
    if que_string in to_watch:
        return 0

def que_movie(que_string, movie_que=MOVIES):
    movie_que['titles'].append(que_string)
    return movie_que

def list_movie():
    if not MOVIES['titles']:
        return "Whaaaat?! No movies queued up? This is a cinematic crime, punishable by repeated viewings of ‘Manos: The Hands of Fate’! Somebody, please… save us from the crushing void of free time and pick something—anything! Even a documentary about sand!."
    return "\n".join(f"- {title}" for title in MOVIES['titles'])

def watched_movie():
    if not MOVIES['watched']:
        return "Well butter my bolts and reboot my RAM! The watched movie list is emptier than a vending machine after Servo's been through it! Someone toss a reel in the projector before I start narrating my own existential crisis!"
    return "\n".join(f"- {title}" for title in MOVIES['watched'])

def finished_movie(que_string, movie_que=MOVIES):
    movie_titles = movie_que['titles']
    if que_string in movie_titles:
        movie_titles.remove(que_string)
        movie_que['watched'].append(que_string)
        return movie_que
    raise ValueError(f"Movie '{que_string}' not found in the list.")

def del_movie(que_string, movie_que=MOVIES):
    movie_titles = movie_que['titles']
    if que_string in movie_titles:
        movie_titles.remove(que_string)
        return movie_que
    raise ValueError(f"Movie '{que_string}' not found in the list.")

def crow_help_message():
    return (
        "**[Crow T. Robot’s Guide to MovieBot – Because You Clearly Need Help]**\n\n"
        "🎬 *Greetings, you confused carbon-based film enthusiast!* I, Crow T. Robot, have been burdened with the sacred duty of helping you manage your little movie list. Try to keep up.\n\n"
        "🛠️ **COMMANDS FOR THE ATTENTION-DEFICIENT:**\n"
        "👉 `!que:<movie name>` – Add a movie to the list. You can also use `!add` if you like synonyms. I won’t judge. Out loud.\n"
        "👉 `!list` – Prints out your glorious collection of unwatched films. Revel in it. Or despair. Your call.\n"
        "👉 `!watched` – Prints out your glorious collection of watched films. Revel in it. Or despair. Your call.\n"
        "👉 `!remove:<movie name>` – Removes a movie from the list, you fickle beast. `!finished` does the same thing, but makes you feel more accomplished.\n"
        "👉 `!del:<movie name>` – Removes a movie from the list, F-O-R-E-V-E-R.\n"
        "👉 `!random` – Can't decide? Let me decide for you. What could go wrong?\n"
        "👉 `!help` – Displays *this very message*, in case you didn’t get enough sass the first time.\n\n"
        "🎯 *Syntax reminder, earthling:* Use a colon `:` after your command. For example:\n"
        "`!que: my life as a zucchini` — yes, that’s a real movie. No, I didn’t make it up.\n\n"
        "🎭 *This concludes your lesson. I’ve been Crow T. Robot — your movie mentor, your mechanical muse, and your last hope for good taste.*\n"
        "*Now go. Curate your list like the tasteless genius you were clearly born to be.*"
    )

def check_movies_loaded():
    global MOVIES
    if not isinstance(MOVIES, dict):
        return "MOVIES is not a dictionary."
    if 'titles' not in MOVIES:
        return "MOVIES dictionary is missing the 'titles' key."
    if not isinstance(MOVIES['titles'], list):
        return "'titles' in MOVIES is not a list."
    if len(MOVIES['titles']) == 0:
        return "MOVIES['titles'] is an empty list."
    return f"MOVIES loaded successfully with {MOVIES['titles']} titles."

def pick_random_movie(movie_que=MOVIES):
    if not movie_que['titles']:
        return "The movie queue is empty."
    return f"🎬 Your random movie pick is: **{random.choice(movie_que['titles'])}**"

@bot.event
async def on_message(message):
    commands_in = {
        '!que': que_movie,
        '!add': que_movie,
        '!list': list_movie,
        '!watched':watched_movie,
        '!finished': finished_movie,
        '!remove': finished_movie,
        '!random': pick_random_movie,
        '!del': del_movie
        }
    try:
        if '!list' in message.content.lower():
            results = list_movie()
            await message.channel.send(f'🍿 The current movie que is 🍿:\n{results}')
        elif '!watched' in message.content.lower():
            results = watched_movie()
            await message.channel.send(f"🦾 You've bravely subjected yourself to the following cinematic wonders and blunders—stand tall, survivor! 🎬:\n{results}")
        elif message.content.lower().strip() == '!random':
            result = pick_random_movie()
            await message.channel.send(result)
            return
        elif message.content.lower().strip().startswith("!check"):
            result = check_movies_loaded()
            await message.channel.send(result)
            return
        elif message.content.lower().strip().startswith("!help"):
            result = crow_help_message()
            await message.channel.send(result)
            return
        elif ":" in message.content:
            message_array = message.content.split(':')
            message_command = message_array[0]
            message_content = message_array[1].strip()
            if message.author == bot.user:
                return
            results = commands_in.get(message_command)(message_content)
            global MOVIES
            MOVIES = results
            # save updated MOVIES to CSV
            with open('./movies.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['titles'])  # write header
                for title in MOVIES['titles']:
                    writer.writerow([title])
            with open('./watched.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['watched'])  # write header
                for title in MOVIES['watched']:
                    writer.writerow([title])
            await message.channel.send('🦾 Movie list updated!')
            print(f'Action successful with command: {message.content}')
        else:
            print(f'Nothing happened with command: {message.content}')
            return
    except Exception as e:
        print(f'Action failed due to {message.content}, the error was {e}')

@bot.event
async def on_ready():
    #on connection
    guild_count = 0
    for guild in bot.guilds:
        #itterate through the number of servers/guilds that have gained access through the Auth2link
        try:
            logger.info(f'Connected-{guild.id} (name:{guild.name})')
            #print the name and guild id and add one to the counter
            guild_count += 1
        except:
            logger.warning(f'Connection Falure-{guild.id} (name:{guild.name})')
            if guild_count != 0:
                guild_count -= 1
        #print a message showing the total number of servers connected. Ths can be useful in the future if multiple amount of servers will be used.
    logger.info(f'Connected to {guild_count} servers, how neat.')


if __name__ == "__main__":
    #establishes connection
    logger = utility.system_logs()
    bot.run(DISCORD_TOKEN)
