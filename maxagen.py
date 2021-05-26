import discord
from distutils.util import strtobool
import random
from configparser import ConfigParser
import time

# TODO: config file, save settings
# TODO: Add phrases


class Settings:
    def __init__(self, config_file):
        self.conf = ConfigParser()
        self.config_section = "main"
        self.config_file = config_file

        # default configuration
        self.def_cmd_prefix = "$"
        self.def_all_phrases = 5
        self.def_line_phrases = 5
        self.def_capitalize = True
        self.def_allow_repeats = False
        self.def_user_mute = True
        self.def_user_ids = 373115287828037632

    def initialize_file(self):
        if not self.conf.read(self.config_file):
            self.conf.add_section(self.config_section)
            self.conf.set(self.config_section, 'cmd_prefix', str(self.def_cmd_prefix))
            self.conf.set(self.config_section, 'all_phrases', str(self.def_all_phrases))
            self.conf.set(self.config_section, 'line_phrases', str(self.def_line_phrases))
            self.conf.set(self.config_section, 'capitalize', str(self.def_capitalize))
            self.conf.set(self.config_section, 'allow_repeats', str(self.def_allow_repeats))
            self.conf.set(self.config_section, 'user_mute', str(self.def_user_mute))
            self.conf.set(self.config_section, 'user_ids', str(self.def_user_ids))
            with open(self.config_file, "w") as file: self.conf.write(file)
        else:
            print("Config file found, you can delete it for new configuration.")

    def read_config(self):
        self.initialize_file()
        self.conf.read(self.config_file)

        cmd_prefix = self.conf[self.config_section]["cmd_prefix"]
        all_phrases = int(self.conf[self.config_section]["all_phrases"])
        line_phrases = int(self.conf[self.config_section]["line_phrases"])
        capitalize = strtobool(self.conf[self.config_section]["capitalize"])
        allow_repeats = strtobool(self.conf[self.config_section]["allow_repeats"])
        user_mute = strtobool(self.conf[self.config_section]["user_mute"])
        user_ids = self.conf[self.config_section]["user_ids"].split(",")

        return cmd_prefix, all_phrases, line_phrases, capitalize, allow_repeats, user_mute, user_ids

    def write_config(self, *args):
        if len(args[0]) >= 1:
            self.conf.set(self.config_section, 'cmd_prefix', str(args[0][0]))
        if len(args[0]) >= 2:
            self.conf.set(self.config_section, 'all_phrases', str(args[0][1]))
        if len(args[0]) >= 3:
            self.conf.set(self.config_section, 'line_phrases', str(args[0][2]))
        if len(args[0]) >= 4:
            self.conf.set(self.config_section, 'capitalize', str(args[0][3]))
        if len(args[0]) >= 5:
            self.conf.set(self.config_section, 'allow_repeats', str(args[0][4]))
        if len(args[0]) >= 6:
            self.conf.set(self.config_section, 'user_mute', str(args[0][5]))
        if len(args[0]) == 7:
            self.conf.set(self.config_section, 'user_ids', str(''.join(args[0][6])))

        print(args[0], args[0][0])

        with open(self.config_file, "w") as file: self.conf.write(file)

class Phrases:
    def __init__(self, phrases_file):
        self.phrases_file = phrases_file

    def check_exists(self, phrase):
        content = self.get_phrases()
        if phrase in content:
            return True
        else:
            return False

    def add_phrase(self, phrase):
        if not self.check_exists(phrase):
            with open(self.phrases_file, "a") as file: file.write(f"\n{phrase}")

    def get_phrases(self):
        with open(self.phrases_file, "r", encoding="utf-8") as file:
            content = file.read().splitlines()
        return content

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

    if message.author == client.user:
        if message.author.bot:
            return
        return

    # list of bot commands
    sorry_commands = ["прощение", "sry", "sorry"]
    gen_commands = ["gen", "ген"]
    help_commands = ["help", "помощь", "помогите"]
    hello_commands = ["привет", "здарова", "hello", "йоу"]
    sh_conf = ["shconf", "showconfig"]
    write_conf = ["wrconf", "writeconfig"]

    all_cmds = sorry_commands + gen_commands + help_commands + hello_commands + sh_conf + write_conf
    gen_cmds = gen_commands + hello_commands + sorry_commands
    parameters_cmds = write_conf + gen_cmds

    msg_content_splitted = message.content.lower().split(",", 1)
    prefix_part = msg_content_splitted[0][0]
    users_part = []

    if msg_content_splitted[0][1] == "?":
        silent = True
        command_part = msg_content_splitted[0][2:]
    else:
        silent = False
        command_part = msg_content_splitted[0][1:]

    if len(msg_content_splitted) > 1:
        arguments_part = msg_content_splitted[1].split(",", 6)
        users_part = arguments_part[-1]
    else:
        arguments_part = False

    print(prefix_part, silent, command_part, arguments_part, users_part)

    # parameters
    s = Settings("config.ini")
    loaded_conf = s.read_config()
    mute_users = loaded_conf[-2]
    cmd_prefix = loaded_conf[0]

    help = f"Данный бот был создан для сохранения удаленных сообщений Махмуда, чтобы была видна структура переписки." \
           f"\nСторонние боты не позволяли этого делать, ибо под Махамада Ибрагиомва требуется " \
           f"опредленная настройка, зная встроенный в его мозг скрипт.\n" \
           f"Команды: (префикс: {cmd_prefix})" \
           f"\n{hello_commands} - приветствие\n{gen_commands} - рандомная фраза из лексикона махмуда\n" \
           f"{sorry_commands} - извинение от ИИ махи\n"\
           f"\nГенератор имеет настройки, которые устанавливаются через запятую, параметры: [кол-во фраз всего (int),"\
           f" кол-во фраз в строке (int), заглавные буквы (bool), разрешение повторений (bool)]"\
           f"\nНапример: {cmd_prefix}gen,5,5,t,t"

    # messages duplicator
    if str(message.author.id) in loaded_conf[-1]:
        if mute_users:
            await message.delete()
        await message.channel.send(f"```{message.content}```")

    if prefix_part == cmd_prefix and any(ele in command_part for ele in all_cmds):

        # arguments check
        if command_part in parameters_cmds:
            cmd_prefix = loaded_conf[0]
            all_count = loaded_conf[1]
            line_count = loaded_conf[2]
            cap = loaded_conf[3]
            rep = loaded_conf[4]
            mute = loaded_conf[5]
            users = loaded_conf[6]

            if command_part in write_conf:
                shift_pos = 1
            else:
                shift_pos = 0

            if isinstance(arguments_part, list):
                if len(arguments_part) >= 1 and arguments_part[0] and shift_pos:
                    cmd_prefix = arguments_part[0]

                if len(arguments_part) >= 1+shift_pos and arguments_part[0+shift_pos]:
                    all_count = arguments_part[0+shift_pos]

                if len(arguments_part) >= 2+shift_pos and arguments_part[1+shift_pos]:
                    line_count = arguments_part[1+shift_pos]

                if len(arguments_part) >= 3+shift_pos and arguments_part[2+shift_pos]:
                    cap = strtobool(arguments_part[2+shift_pos])

                if len(arguments_part) >= 4+shift_pos and arguments_part[3+shift_pos]:
                    rep = strtobool(arguments_part[3+shift_pos])

                if len(arguments_part) >= 5+shift_pos and arguments_part[4+shift_pos]:
                    mute = arguments_part[4+shift_pos]

                if len(arguments_part) >= 6+shift_pos and arguments_part[5+shift_pos]:
                    users = arguments_part[5+shift_pos]

            if command_part in gen_cmds:
                generator_settings = {
                    "all_phrases": int(all_count),
                    "line_phrases": int(line_count),
                    "capitalize": cap,
                    "allow_repeats": rep
                }

                if any(ele in command_part for ele in hello_commands):
                    await message.channel.send(MaxxaGen(generator_settings, "hello.txt"))
                elif any(ele in command_part for ele in gen_commands):
                    await message.channel.send(MaxxaGen(generator_settings, "phrases.txt"))
                # $sry command
                elif any(ele in command_part for ele in sorry_commands):
                    await message.channel.send(MaxxaGen(generator_settings, "forgiveness_phrases.txt"))

            elif command_part in write_conf:
                new_config = [cmd_prefix, all_count, line_count, cap, rep, mute, users]
                print(f"users: {users}")
                if any(ele in command_part for ele in write_conf):
                    previous_config = loaded_conf
                    s.write_config(new_config)
                    await message.channel.send(f"{previous_config} -> {s.read_config()}")

        # delete command message
        if silent:
            await message.delete()

        # checks if dolboeb maha writes command without mistakes
        if str(message.author.id) in loaded_conf[-1] and message.content.startswith(all_cmds) and " " in message.content:
            await message.channel.send("Махмуд пошёл нахуй, читай команды долбаёб")
        # if maha asks somebody say "jo", bot will print "jo" 60 times in 1 msg
        elif str(message.author.id) in loaded_conf[-1] and 'пойоукай' in message.content:
            await message.channel.send('йоу ' * 60)
        elif any(ele in command_part for ele in help_commands):
            await message.channel.send(f"```{help}```")
        elif str(message.author.id) in loaded_conf[-1] and '/play' in message.content:
            pass
        elif any(ele in command_part for ele in sh_conf):
            await message.channel.send(loaded_conf)

if __name__ == '__main__':
    client.run('ODMxNjQ3OTAyNjkzOTgyMjI4.YHYSdw.uyYpwtdNK_yD77GMFw9MVH8V0Po')
