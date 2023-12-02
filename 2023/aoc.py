import sys
from pprint import pprint
from collections import namedtuple
from functools import reduce
from operator import mul

lines = sys.stdin.read().splitlines()

# Utils

def first(predicate, iterable):
    return next((x for x in iterable if predicate(x)), None)

# Problem 1

def first_digit(line):
    return next(filter(str.isdigit, line))

def last_digit(line):
    return first_digit(reversed(line))

def calibration_value(line):
    return int(first_digit(line) + last_digit(line))


DIGIT_NAME_TO_NUMERAL = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

def replace_digit_names(line):
    replaced_line = ""
    for i in range(len(line)):
        matched_digit_name = first(lambda x: line.startswith(x, i), DIGIT_NAME_TO_NUMERAL)
        if matched_digit_name:
            replaced_line += DIGIT_NAME_TO_NUMERAL[matched_digit_name]
        else:
            replaced_line += line[i]
    return replaced_line

# print(sum(map(calibration_value, lines)))
# print(sum(map(calibration_value, map(replace_digit_names, lines))))

# Problem 2

Game = namedtuple('Game', 'id draws')

def parse_game(line):
    game, draws = line.split(': ')
    game_id = int(game.split()[1])
    game_draws = []
    for draw in draws.split('; '):
        game_draw = {}
        for ball in draw.split(', '):
            num, name = ball.split()
            num = int(num)
            game_draw[name] = num
        game_draws.append(game_draw)
    return Game(game_id, game_draws)

games = list(map(parse_game, lines))

REAL_CONTENTS = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

def includes_draw(draw, real_contents):
    return all(
        name in real_contents and real_contents[name] >= num
        for name, num, in draw.items()
    )

def game_is_possible(game):
    return all(
        includes_draw(draw, REAL_CONTENTS)
        for draw in game.draws
    )

def draw_upper_bound(draw1, draw2):
    return {
        'green': max(draw1.get('green', 0), draw2.get('green', 0)),
        'red': max(draw1.get('red', 0), draw2.get('red', 0)),
        'blue': max(draw1.get('blue', 0), draw2.get('blue', 0)),
    }

def draw_power(draw):
    return reduce(mul, draw.values())

def game_draw_upper_bound(game):
    return reduce(draw_upper_bound, game.draws)


# print(sum(game.id for game in games if game_is_possible(game)))
# print(sum(draw_power(game_draw_upper_bound(game)) for game in games))
