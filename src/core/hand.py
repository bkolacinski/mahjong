from typing import Optional

from enums import MeldType
from tile import Tile, TileSuit


class Meld:
    meld_type: MeldType
    tiles: list[Tile]

    is_concealed: bool
    _original_owner = None

    def __init__(self, meld_type: MeldType,
                 tiles: list[Tile], is_concealed: bool = False):
        self.meld_type = meld_type
        self.tiles = tiles
        self.is_concealed = is_concealed
        self._original_owner = None

    def set_original_owner(self, owner) -> None:
        self._original_owner = owner

    def get_original_owner(self):
        return self._original_owner


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
        raise NotImplementedError()

    def can_pon(self, tile: Tile) -> bool:
        return self.concealed_tiles.count(tile) >= 2

    def can_kan(self, tile: Tile) -> bool:
        return self.concealed_tiles.count(tile) >= 3

    def can_chii(self, tile: Tile) -> list[list[Tile]]:
        if tile.suit == TileSuit.HONOR:
            return []

        possible_chiis = []
        for offset in [-2, -1, 0]:
            chii_tiles = []
            for i in range(3):
                needed_value = tile.value + offset + i
                if 1 > needed_value > 9:
                    break
                needed_tile = Tile(tile.suit, needed_value)
                if needed_tile == tile:
                    continue
                if needed_tile not in self.concealed_tiles:
                    break
                chii_tiles.append(needed_tile)
            if len(chii_tiles) == 2:
                possible_chiis.append(chii_tiles)

        return possible_chiis

    @staticmethod
    def make_pon(called_tile: Tile, hand_tiles: list[Tile]) -> Meld:
        return Meld(MeldType.PON, [called_tile] +
                    hand_tiles, is_concealed=False)

    @staticmethod
    def make_kan(called_tile: Tile, hand_tiles: list[Tile],
                 is_concealed: bool = False) -> Meld:
        return Meld(MeldType.KAN, [called_tile] +
                    hand_tiles, is_concealed=is_concealed)

    @staticmethod
    def make_chii(called_tile: Tile, hand_tiles: list[Tile]) -> Meld:
        return Meld(MeldType.CHII, [called_tile] +
                    hand_tiles, is_concealed=False)
