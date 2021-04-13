import discord
import os
import random

class MaxxaGen:
    def __init__(self, settings):
        self.all_phrs = settings["all_phrases"]
        self.line_phrs = settings["line_phrases"]
        self.captlz = settings["capitalize"]
        self.allow_repeats = settings["allow_repeats"]
        self.file = settings["file"]
        self.phrases = self.read_from_file()

    def read_from_file(self):
        """Read file with phrases."""
        phrases = {}
        counter = 0
        with open(self.file, encoding="utf-8") as file:
            for line in file:
                phrases[counter] = line.strip()
                counter += 1
        return phrases

    def get_random(self, delete):
        """IDK why i need this."""
        try:
            result = random.choice(list(self.phrases.items()))
            if delete:
                self.phrases.pop(result[0])
            return result[1]
        except IndexError:
            pass

    def union(self):
        """Make text from phrases."""
        lines = {}
        counter = 0
        line = 0
        line_counter = 0
        while counter != self.all_phrs:
            counter += 1

            phrase = self.get_random(False) if self.allow_repeats else self.get_random(True)

            if phrase:
                if line_counter == self.line_phrs:
                    # when line is full, creates new line
                    line += 1
                    lines[line] = phrase
                    line_counter = 1
                else:
                    # first line and when it isn't full
                    if line in lines:
                        current_val = lines.get(line)
                        lines[line] = f"{current_val} {phrase}"
                    else:
                        lines[line] = phrase

                    line_counter += 1

        return lines

    def __str__(self):
        res_dict = self.union()
        res_str = ""
        for val in res_dict.values():
            if res_str:
                res_str += "\n"
            res_str += val.capitalize() if self.captlz else val

        return res_str


settings_gen = {
    "all_phrases": 50,
    "line_phrases": 2,
    "capitalize": True,
    "allow_repeats": True,
    "file": "phrases.txt",
}

settings_forgiveness = {
    "all_phrases": 50,
    "line_phrases": 2,
    "capitalize": True,
    "allow_repeats": True,
    "file": "forgiveness_phrases.txt",
}


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
        await message.channel.send(MaxxaGen(settings_gen))

    if message.content.startswith('/прощение') or message.content.startswith('$sry'):
        await message.channel.send(MaxxaGen(settings_forgiveness))

    if message.author.id == 373115287828037632:
        if "пойоукай" in message.content:
            await message.channel.send("йоу " * 60)

    """if message.content.startswith('$kazantip') or message.content.startswith('/казантип'):
        await message.channel.send("/play song:https://www.youtube.com/watch?v=O8W6TSwABak")

    if message.content.startswith('$dnb') or message.content.startswith('/днб'):
        await message.channel.send("/play input:https://youtu.be/_FWirIjoCAQ")"""

  #чс - автокик/автобан



client.run('TOKEN')
