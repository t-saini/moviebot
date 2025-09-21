# Crow T. Robot The Discord Movie Bot Tracker

A lightweight Discord bot designed to help you manage your movie queue with flair, sarcasm, and just a little bit of robotic superiority. 
Run it on your own server to track what you want to watch, what you've already seen, and to let chaos decide your next movie night.
_The bot identifies itself as **Crow T. Robot**, your mechanical movie guide with more sass than RAM._


## Features
- Add movies to your queue or watched list
- List currently queued or watched movies
- Remove or permanently delete entries
- Let Crow choose a random movie for you
- Get help with a built-in Crow-flavored guide
---

## Commands
Comands can be ran within the Discord channel that Crow has been given access to.

- !que:<movie name> – Add a movie to the list.
- !list – Prints out your collection of unwatched films.
- !watched – Prints out your collection of watched films.
- !remove:<movie name> – Removes a movie from the list. !finished does the same thing.
- !del:<movie name> – Removes a movie from the watch list without moving it into "watched"
- !random – Randomly selects a movie from the watch list.
- !help – Displays a help message with these commands but in the style of Crow T. Robot

## Getting Started
1. Clone this repository

2. Set up your environment (e.g., python -m venv, install dependencies)

3. Add your Discord token in an .ini config file

4. Run the bot using your preferred process manager (e.g., screen, systemd, etc.)

**Note**: Version 1 of was built to be ran on a 32 bit Raspberry Pi 4. In a future update the code base will be adjusted to run on
a 64 bit hardware. This will also allow for the use of Python libraries such as Pandas.

## Roadmap
- [ ] Update how the bot watches for a message event.
- [ ] Rewrite for 64-bit hardware. Dependency is on my equipment upgrades.
- [ ] Make movie que management (adding, removing, deleteing, etc etc) a little bit easier.
- [ ] Stretch goal: Have the bot download information about a given movie in the list, and create a sarcastic spoiler free review
of the movie. This "review" would be very brief and it would appear when `!random` is used, just to give the bot a bit more personality.

