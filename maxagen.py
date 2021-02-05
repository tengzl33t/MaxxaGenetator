"""Maxa text generator."""
import random


def read_from_file() -> list:
    """Read file with phrases."""
    phrases = []
    with open("phrases.txt", encoding="utf-8") as file:
        for line in file:
            phrases.append(line.strip())

    return phrases


def get_random_from_list():
    """IDK why i need this."""
    return random.choice(read_from_file())


def union_random(all_count, line_count, capitalize):
    """Make text from phrases."""
    res_str = ""
    counter = 0
    line_counter = 0
    while counter != all_count:
        counter += 1

        if line_counter == line_count:
            res_str += "\n" + (get_random_from_list().capitalize() if capitalize else get_random_from_list()) + " "
            line_counter = 1
        else:
            res_str += (get_random_from_list().capitalize() if len(
                res_str) == 0 and capitalize else get_random_from_list()) + " "
            line_counter += 1

    return res_str


# union_random(all phrases count, phrases in line count, capitalize first char on line)
print(union_random(20, 2, 1))
