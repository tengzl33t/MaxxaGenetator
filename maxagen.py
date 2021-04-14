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

            phrase = self.get_random(False) if self.allow_repeats is True else self.get_random(True)

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
            res_str += val.capitalize() if self.captlz is True else val

        return res_str


settings_gen = {
    "all_phrases": 5,
    "line_phrases": 5,
    "capitalize": True,
    "allow_repeats": True,
    "file": "phrases.txt",
}

settings_forgiveness = {
    "all_phrases": 5,
    "line_phrases": 5,
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
    # list of bot commands
    commands = ['$help', '/ген', '$gen', '/йоу', '$hi', '/прощение', '$sry']
    sorry_commands = ["прощение", "sry", "sorry"]
    gen_commands = ["gen", "ген"]
    help_commands = ["help", "помощь", "помогите"]
    hello_commands = ["привет", "здарова", "hello", "йоу"]

    msg_content_splitted = message.content.lower().split(",")
    msg_content = msg_content_splitted[0]
    #
    all_count = int(msg_content_splitted[1]) if len(msg_content_splitted) >= 2 else 5
    line_count = int(msg_content_splitted[2]) if len(msg_content_splitted) >= 3 else 5
    cap = msg_content_splitted[3] if len(msg_content_splitted) >= 4 else True   # TODO: Converting to bool
    rep = msg_content_splitted[4].bool if len(msg_content_splitted) == 5 else True

    # print(all_count, line_count, cap, rep)

    st = {
        "all_phrases": all_count,
        "line_phrases": line_count,
        "capitalize": cap,
        "allow_repeats": rep,
        "file": "phrases.txt",
    }

    # ignore bot messages
    if message.author == client.user:
        return

    # help.txt reading to string
    with open("help.txt", "r", encoding="utf8") as file:
        data = file.read()


    # mahammad20 messages duplicator
    if message.author.id == 373115287828037632:
        await message.channel.send(f"```{message.content}```")
    # if message.author.id == 373115287828037632:
    #     await message.channel.send(f"```{message.content}```")
    if msg_content.startswith('/'):
        # delete command message
        if msg_content.startswith('/?'):
            await message.delete()

        # checks if dolboeb maha writes command without mistakes
        if message.author.id == 373115287828037632 and message.content.startswith(tuple(commands)) and " " in message.content:
            await message.channel.send("Махмуд пошёл нахуй, читай команды долбаёб")
        # if maha asks somebody say "jo", bot will print "jo" 60 times in 1 msg
        elif message.author.id == 373115287828037632 and 'пойоукай' in message.content:
          await message.channel.send('йоу ' * 60)
        # $gen command
        elif any(ele in msg_content for ele in gen_commands):
            print(st)
            print(MaxxaGen(st))
            await message.channel.send(MaxxaGen(st))
        # $sry command
        elif any(ele in msg_content for ele in sorry_commands):
            await message.channel.send(MaxxaGen(settings_forgiveness))
        # $help command
        elif any(ele in msg_content for ele in help_commands):
            await message.channel.send(f"```{data}```")
        # $hi command
        elif any(ele in msg_content for ele in hello_commands):
            await message.channel.send("йоу бандишка братишка") # добавить файл с разными приветствиями и принтить рандомное
        # skips written command /play (Rhytm bot) by maha
        elif message.author.id == 373115287828037632 and '/play' in message.content:
            pass



client.run('ODMxNjQ3OTAyNjkzOTgyMjI4.YHYSdw.i7Eduu37I0bHcHr8bUWjmRRe4lY')
