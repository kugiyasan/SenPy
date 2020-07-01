# SenPy
A discord bot written with discord.py to praise your favorite waifu!

# Features
* Send random pictures from https://reddit.com, https://nekos.life, https://thiswaifudoesnotexist.net and https://thisfursonadoesnotexist.com
* Play some mastermind against the bot, with various levels of difficulty!
* Collect MofuPoints, and compete with your friends (It lasted 5 minutes on my server before people were getting bored)
* Play some songs forever in the voice chat
* You can see a list of all commands with `xd help` (maybe there is some hidden commands in the code 😉)

# How to invite him on your server
## The easy way
https://discord.com/oauth2/authorize?client_id=671722338848342036&scope=bot&permissions=3537984

Note: For now, my bot is running on a raspberry pi 0 w, so don't expect it to be super reactive (especially in the voice chat)

## The hard way (run your own instance of SenPy)
* Make sure Python and Git are installed on your computer
* Follow the instructions [here](https://discordpy.readthedocs.io/en/latest/discord.html) to create a bot account
* Open the terminal
* Clone this repository with `git clone https://github.com/kugiyasan/SenPy.git`, then `cd SenPy`
* Install the required modules for python `pip install -r requirements.txt`
* Paste your discord token obtained on the Discord Developer Portal in `discordToken.py`. It should look like `token = 'ASFxccwaf...'`
* Make a `media` directory. Inside the `media` directory, place a `audio.mp3`, `welcome.mp3` and `seeya.mp3` if you want some sounds to come out!
* Enjoy! `python sen.py`

# DISCLAIMER
This bot is only a cool project that I did. Anything can break or change suddently according to my wishes.
Don't be shy to message me some comments, ideas or questions if youe have some!

[![forthebadge](https://forthebadge.com/images/badges/contains-cat-gifs.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/ages-18.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-science.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/you-didnt-ask-for-this.svg)](https://forthebadge.com)
