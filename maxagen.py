import discord
from distutils.util import strtobool
import random


class MaxxaGen:
    def __init__(self, settings, file):
        self.all_phrs = settings["all_phrases"]
        self.line_phrs = settings["line_phrases"]
        self.captlz = settings["capitalize"]
        self.allow_repeats = settings["allow_repeats"]
        self.file = file
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


client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    # list of bot commands
    sorry_commands = ["прощение", "sry", "sorry"]
    gen_commands = ["gen", "ген"]
    help_commands = ["help", "помощь", "помогите"]
    hello_commands = ["привет", "здарова", "hello", "йоу"]

    all_cmds = sorry_commands + gen_commands + help_commands + hello_commands

    msg_content_splitted = message.content.lower().split(",")
    msg_content = msg_content_splitted[0]

    # parameters
    mute_maxxa = True
    cmd_prefix = "$"

    help = f"Данный бот был создан для сохранения удаленных сообщений Махмуда, чтобы была видна структура переписки." \
           f"\nСторонние боты не позволяли этого делать, ибо под Махамада Ибрагиомва требуется " \
           f"опредленная настройка, зная встроенный в его мозг скрипт.\n" \
           f"Команды: (префикс: {cmd_prefix})" \
           f"\n{hello_commands} - приветствие\n{gen_commands} - рандомная фраза из лексикона махмуда\n" \
           f"{sorry_commands} - извинение от ИИ махи\n"\
           f"\nГенератор имеет настройки, которые устанавливаются через запятую, параметры: [кол-во фраз всего (int),"\
           f" кол-во фраз в строке (int), заглавные буквы (bool), разрешение повторений (bool)]"\
           f"\nНапример: {cmd_prefix}gen,5,5,t,t"

    # ebatj ja bidlo ebanoe
    try:
        all_count = int(msg_content_splitted[1])
    except Exception:
        all_count = 5
    try:
        line_count = int(msg_content_splitted[2])
    except Exception:
        line_count = 5
    try:
        cap = strtobool(msg_content_splitted[3])
    except Exception:
        cap = True
    try:
        rep = strtobool(msg_content_splitted[4])
    except Exception:
        rep = False

    settings = {
        "all_phrases": all_count,
        "line_phrases": line_count,
        "capitalize": cap,
        "allow_repeats": rep
    }

    # ignore bot messages
    if message.author == client.user:
        return

    # mahammad20 messages duplicator
    if message.author.id == 373115287828037632:
        if mute_maxxa:
            await message.delete()
        await message.channel.send(f"```{message.content}```")
    # if message.author.id == 373115287828037632:
    #     await message.channel.send(f"```{message.content}```")
    if msg_content.startswith(cmd_prefix) and any(ele in msg_content for ele in all_cmds):
        # delete command message
        if msg_content.startswith(f"{cmd_prefix}?"):
            await message.delete()

        # checks if dolboeb maha writes command without mistakes
        if message.author.id == 373115287828037632 and message.content.startswith(all_cmds) and " " in message.content:
            await message.channel.send("Махмуд пошёл нахуй, читай команды долбаёб")
        # if maha asks somebody say "jo", bot will print "jo" 60 times in 1 msg
        elif message.author.id == 373115287828037632 and 'пойоукай' in message.content:
            await message.channel.send('йоу ' * 60)
        # $gen command
        elif any(ele in msg_content for ele in gen_commands):
            # print(settings_gen)
            # print(MaxxaGen(settings_gen))
            await message.channel.send(MaxxaGen(settings, "phrases.txt"))
        # $sry command
        elif any(ele in msg_content for ele in sorry_commands):
            await message.channel.send(MaxxaGen(settings, "forgiveness_phrases.txt"))
        # $help command
        elif any(ele in msg_content for ele in help_commands):
            await message.channel.send(f"```{help}```")
        # $hi command
        elif any(ele in msg_content for ele in hello_commands):
            await message.channel.send(MaxxaGen(settings, "hello.txt"))
        # skips written command /play (Rhytm bot) by maha
        elif message.author.id == 373115287828037632 and '/play' in message.content:
            pass


client.run('token')
