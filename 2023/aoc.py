import sys
import re
from pprint import pprint
from collections import namedtuple
from functools import reduce
from operator import mul
from itertools import repeat

lines = sys.stdin.read().splitlines()

# Utils

def first(predicate, iterable):
    return next((x for x in iterable if predicate(x)), None)

def max_axis_dist(p1, p2):
    p1x, p1y = p1
    p2x, p2y = p2
    return max(abs(p1x - p2x), abs(p1y - p2y))

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


# games = list(map(parse_game, lines))
# print(sum(game.id for game in games if game_is_possible(game)))
# print(sum(draw_power(game_draw_upper_bound(game)) for game in games))


# Problem 2

Number = namedtuple('Number', 'value locs')
Symbol = namedtuple('Symbol', 'value loc')
Gear = namedtuple('Gear', 'parts')


def parse_numbers(line_number, line):
    for n in re.finditer(r"\d+", line):
        yield Number(
            int(n.group(0)),
            list(
                zip(
                    repeat(line_number),
                    range(n.start(), n.end())
                )
            )
        )

def parse_symbols(line_number, line):
    for s in re.finditer(r"[^\d\.]", line):
        yield Symbol(
            s.group(0),
            (line_number, s.start())
        )

def adjacent(p1, p2):
    return max_axis_dist(p1, p2) == 1

def adjacent_to_symbol(num, symbol):
    return any(adjacent(num_loc, symbol.loc) for num_loc in num.locs)

def adjacent_numbers(symbol, numbers):
    return [number for number in numbers if adjacent_to_symbol(number, symbol)]

def gears(symbols, numbers):
    for symbol in symbols:
        if symbol.value == '*':
            adj = adjacent_numbers(symbol, numbers)
            if len(adj) == 2:
                yield Gear([number.value for number in adj])

def gear_ratio(gear):
    return reduce(mul, gear.parts)
    
numbers = [number for line_num, line in enumerate(lines) for number in parse_numbers(line_num, line)]
symbols = [symbol for line_num, line in enumerate(lines) for symbol in parse_symbols(line_num, line)]
    
print(sum(number.value for number in numbers if any(adjacent_to_symbol(number, symbol) for symbol in symbols)))
print(sum(gear_ratio(gear) for gear in gears(symbols, numbers)))
