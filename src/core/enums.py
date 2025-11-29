from enum import Enum


class Wind(Enum):
    EAST = 1
    SOUTH = 2
    WEST = 3
    NORTH = 4


class MeldType(Enum):
    CHII = 'chii'
    PAIR = 'pair'
    PON = 'pon'
    KAN = 'kan'


class TileSuit(Enum):
    MAN = 'm'
    PIN = 'p'
    SOU = 's'
    HONOR = 'z'
