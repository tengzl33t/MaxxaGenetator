import discord
import os
import random


class MaxxaGen:
    def __init__(self, all_phrs, line_phrs, captlz, file):
        self.all_phrs = all_phrs
        self.line_phrs = line_phrs
        self.captlz = captlz
        self.file = file

    def read_from_file(self):
        """Read file with phrases."""
        phrases = []
        with open(self.file, encoding="utf-8") as file:
            for line in file:
                phrases.append(line.strip())

        return phrases

    def get_random_from_list(self):
        """IDK why i need this."""
        B = sorted(self.read_from_file(), key=lambda A: random.random())
        return B[:self.all_phrs]

    def __str__(self):
        """Make text from phrases."""
        res_str = ""
        for i in self.get_random_from_list():
            res_str += i + " "
        return res_str.capitalize()


client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    # ignore bot messages
    if message.author == client.user:
        return

    # help.txt reading to string
    with open("help.txt", "r") as file:
        data = file.read()

    # help command
    if message.content.startswith('$help'):
        await message.channel.send(f"```{data}```")

    # $hi command
    if message.content.startswith('/йоу') or message.content.startswith('$hi'):
        await message.channel.send("йоу бандишка братишка")

    # mahammad20 messages duplicator 
    if message.author.id == 373115287828037632:
        await message.channel.send(f"```{message.content}```")

    # $gen command
    if message.content.startswith('/ген') or message.content.startswith('$gen'):
        await message.channel.send(MaxxaGen(5, 5, True, 'phrases.txt'))

    if message.content.startswith('/прощение') or message.content.startswith('$sry'):
        await message.channel.send(MaxxaGen(5, 5, True, 'forgiveness_phrases.txt'))

    if message.author.id == 373115287828037632:
        if "пойоукай" in message.content:
            await message.channel.send("йоу " * 60)

    """if message.content.startswith('$kazantip') or message.content.startswith('/казантип'):
        await message.channel.send("/play song:https://www.youtube.com/watch?v=O8W6TSwABak")

    if message.content.startswith('$dnb') or message.content.startswith('/днб'):
        await message.channel.send("/play input:https://youtu.be/_FWirIjoCAQ")"""

  #чс - автокик/автобан



client.run('ODMxMDcyOTkwMzc1OTY4NzY5.YHP7CQ.0zCk7PBwtc0Dl4i_KYmwYD0kfCg')
