import sys
import re
from pprint import pprint
from collections import namedtuple, deque, Counter
from functools import reduce, cache
from operator import mul
from itertools import repeat, batched, starmap


# lines = sys.stdin.read().splitlines()

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


# Problem 3

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
    
# numbers = [number for line_num, line in enumerate(lines) for number in parse_numbers(line_num, line)]
# symbols = [symbol for line_num, line in enumerate(lines) for symbol in parse_symbols(line_num, line)]

# print(sum(number.value for number in numbers if any(adjacent_to_symbol(number, symbol) for symbol in symbols)))
# print(sum(gear_ratio(gear) for gear in gears(symbols, numbers)))

# Problem 4

Card = namedtuple('Card', 'index winning_numbers own_numbers')

def parse_card(line_number, line):
    _, numbers = line.split(': ')
    winning_numbers, own_numbers = numbers.split(' | ')
    return Card(
        line_number,
        set(map(int, winning_numbers.split())),
        set(map(int, own_numbers.split())),
    )

def matching_numbers(card):
    return len(card.winning_numbers & card.own_numbers)

def card_points(card):
    m = matching_numbers(card)
    if not m:
        return 0
    return 2**(m - 1)

def count_total_copies(cards):
    @cache
    def count_copies(i):
        m = matching_numbers(cards[i])
        return 1 + sum(
            count_copies(j)
            for j in range(
                cards[i].index + 1,
                min(len(cards), cards[i].index + 1 + m)
            )
        )
    return sum(map(count_copies, range(len(cards))))

# cards = [parse_card(line_number, line) for line_number, line in enumerate(lines)]

# print(sum(map(card_points, cards)))
# print(count_total_copies(cards))


# Problem 5

def intersect(range1, range2):
    start = max(range1.start, range2.start)
    end = min(range1.stop, range2.stop)
    if end > start:
        return range(start, end)
    return None

class ProductionMap:
    def __init__(self, mappings):
        self.mappings = mappings
    
    def map(self, value):
        for source_range, destination_start in self.mappings:
            if value in source_range:
                return destination_start - source_range.start + value
        return value
    
    def map_ranges(self, ranges):
        to_intersect = deque(ranges)
        intersected = []
        while to_intersect:
            current = to_intersect.popleft()
            for source_range, destination_start in self.mappings:
                intersection = intersect(source_range, current)
                if intersection is not None:
                    if intersection.start > current.start:
                        to_intersect.append(range(current.start, intersection.start))
                    if current.stop > intersection.stop:
                        to_intersect.append(range(intersection.stop, current.stop))
                    current = range(
                        destination_start - source_range.start + intersection.start,
                        destination_start - source_range.start + intersection.stop
                    )
                    break
            intersected.append(current)
        return intersected

def read_production_maps():
    blocks = sys.stdin.read().split('\n\n')
    iblocks = iter(blocks)
    seeds = list(map(int, next(iblocks).split(': ')[1].split()))
    production_maps = []
    for b in iblocks:
        lines = b.splitlines()
        mappings = []
        for line in lines[1:]:
            dst_start, source_start, lenght = tuple(map(int, line.split()))
            mappings.append((range(source_start, source_start + lenght), dst_start))
        production_maps.append(ProductionMap(mappings))        
    return seeds, production_maps

#seeds, prod_maps = read_production_maps()
#seed_ranges = [range(start, start + length) for start, length in batched(seeds, 2)]

def apply_prod_maps(prod_maps, seed):
    for prod_map in prod_maps:
        seed = prod_map.map(seed)
    return seed

def apply_prod_maps_range(prod_maps, seed_ranges):
    for prod_map in prod_maps:
        seed_ranges = prod_map.map_ranges(seed_ranges)
    return seed_ranges

# print(min(apply_prod_maps(prod_maps, seed) for seed in seeds))
# print(min(seed_range.start for seed_range in apply_prod_maps_range(prod_maps, seed_ranges)))

# Problem 6

Race = namedtuple('Race', 'time hs_distance')

def read_races():
    times, hs_distances = sys.stdin.read().split('\n')
    times = map(int, times.split(':')[1].split())
    hs_distances = map(int, hs_distances.split(':')[1].split())
    return [Race(time, distance) for time, distance in zip(times, hs_distances)]

def distance(time, hold):
    return time * hold - hold * hold

def count_ways_to_beat_hs(race):
    return sum(distance(race.time, hold) > race.hs_distance for hold in range(1, race.time))

#races = read_races()
# Brute force solves the big input in a couple of seconds no need do quadratics
# print(reduce(mul, map(count_ways_to_beat_hs, races)))


# Problem 7


def read_hand_bid_table():
    lines = sys.stdin.read().split('\n')
    lines = (line.split() for line in lines)
    return {tuple(hand): int(bid) for hand, bid in lines}

def hand_type(hand):
    c = Counter(hand)
    if len(c) == 1:
        return 7
    if len(c) == 2:
        _, count = c.most_common(1)[0]
        if count == 4:
            return 6
        else:
            return 5
    if len(c) == 3:
        _, count = c.most_common(1)[0]
        if count == 3:
            return 4
        else:
            return 3
    if len(c) == 4:
        return 2
    return 1

def fuzzy_hand_type(hand):
    c = Counter(hand)
    j_count = c.get('J', 0)
    c.pop('J', None)
    if len(c) == 1 or len(c) == 0:
        return 7
    if len(c) == 2:
        _, count = c.most_common(1)[0]
        if count + j_count == 4:
            return 6
        else:
            return 5
    if len(c) == 3:
        _, count = c.most_common(1)[0]
        if count + j_count == 3:
            return 4
        else:
            return 3
    if len(c) == 4:
        return 2
    return 1

CARD_STRENGTH_TABLE = {
    'A': 14,
    'K': 13,
    'Q': 12,
    # 'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
    'J': 1,
}

def hand_strength(hand):
    return tuple(map(CARD_STRENGTH_TABLE.get, hand))

def hand_rank(hand):
    return (fuzzy_hand_type(hand), hand_strength(hand))

hand_bid_table = read_hand_bid_table()

hands = sorted(hand_bid_table, key=hand_rank)

print(sum(hand_bid_table[hand] * (rank + 1) for rank, hand in enumerate(hands)))
