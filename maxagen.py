import discord
import os
import random


class MaxxaGen:
    def __init__(self, all_phrs, line_phrs, captlz):
        self.all_phrs = all_phrs
        self.line_phrs = line_phrs
        self.captlz = captlz

    def read_from_file(self):
        """Read file with phrases."""
        phrases = []
        with open("phrases.txt", encoding="utf-8") as file:
            for line in file:
                phrases.append(line.strip())

        return phrases

    def get_random_from_list(self):
        """IDK why i need this."""
        return random.choice(self.read_from_file())

    def __str__(self):
        """Make text from phrases."""
        res_str = ""
        counter = 0
        line_counter = 0
        while self.all_phrs != counter:
            counter += 1

            if self.line_phrs == line_counter:
                res_str += "\n" + (self.get_random_from_list().capitalize(
                ) if self.captlz else self.get_random_from_list()) + " "
                line_counter = 1
            else:
                res_str += (self.get_random_from_list().capitalize()
                            if len(res_str) == 0 and self.captlz else
                            self.get_random_from_list()) + " "
                line_counter += 1

        return res_str


client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$help'):
        await message.channel.send(
            "```Данный бот был создан для сохранения удаленных сообщений Махмуда, чтобы была видна структура переписки. Сторонние боты не позволяли этого делать, ибо под Махамада Ибрагиомва требуется опредленная настройка, зная встроенный в его мозг скрипт.\n\nКоманды:\n$hello - приветствие\n$generate - рандомная фраза из лексикона махмуда (добавится в бета версии)```"
        )

    if message.content.startswith('$hello'):
        await message.channel.send("йоу бандишка братишка")

    if message.author.id == 373115287828037632:
        await message.channel.send(f"```{message.content}```")

    if message.content.startswith('$generate'):
        await message.channel.send(MaxxaGen(5, 5, True))

    if message.author.id == 373115287828037632:
        if "пойоукай" in message.content:
            await message.channel.send(
                "йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу йоу"
            )
    """
  чс - автокик/автобан
  """


client.run(os.getenv('TOKEN'))
