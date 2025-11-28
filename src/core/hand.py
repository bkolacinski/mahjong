from enum import Enum
from typing import Optional

from .tile import Tile, TileSuit


class MeldType(Enum):
    CHII = 'chii'
    PAIR = 'pair'
    PON = 'pon'
    KAN = 'kan'


class Meld:
    meld_type: MeldType
    tiles: list[Tile]

    is_concealed: bool
    original_owner = None

    def __init__(self, meld_type: MeldType,
                 tiles: list[Tile], is_concealed: bool = False):
        self.meld_type = meld_type
        self.tiles = tiles
        self.is_concealed = is_concealed
        self.original_owner = None


class Hand:
    concealed_tiles: list[Tile]
    discarded_tiles: list[Tile]
    last_drawn_tile: Optional[Tile]

    is_riichi: bool
    is_discarded: bool

    def __init__(self):
        self.concealed_tiles = []
        self.discarded_tiles = []
        self.last_drawn_tile = None

        self.is_riichi = False
        self.is_discarded = False

    def add_tile(self, tile: Tile) -> None:
        self.concealed_tiles.append(tile)
        self.last_drawn_tile = tile

    def discard_tile(self, tile: Tile) -> bool:
        if tile not in self.concealed_tiles:
            return False

        self.concealed_tiles.remove(tile)
        self.discarded_tiles.append(tile)

        self.is_discarded = True
        self.last_drawn_tile = None
        return True

    def sort_hand(self) -> None:
        self.concealed_tiles.sort()

    def tile_count_in_hand(self, tile: Tile) -> int:
        return len(self.concealed_tiles)

    def tile_count_total(self, tile: Tile) -> int:
        NotImplementedError()

    def can_pon(self, tile: Tile) -> bool:
        return self.concealed_tiles.count(tile) >= 2

    def can_kan(self, tile: Tile) -> bool:
        return self.concealed_tiles.count(tile) >= 3

    def can_chii(self, tile: Tile) -> list[Optional(list[Tile])]:
        if tile.suit == TileSuit.HONOR:
            return []

        possible_chiis = []
        NotImplementedError()

        return possible_chiis

    def make_pon(self, called_tile: Tile, hand_tiles: list[Tile]) -> None:
        NotImplementedError()

    def make_kan(self, called_tile: Tile, hand_tiles: list[Tile],
                 is_concealed: bool = False) -> None:
        NotImplementedError()

    def make_chii(self, called_tile: Tile, hand_tiles: list[Tile]) -> None:
        NotImplementedError()
