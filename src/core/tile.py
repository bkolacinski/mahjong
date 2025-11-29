from enums import TileSuit
from exceptions import MahjongException


class Tile:
    suit: TileSuit
    value: int
    is_red: bool

    owner = None
    is_discarded: bool
    is_revealed: bool

    def __init__(self, suit: TileSuit, value: int, is_red: bool = False):
        self.suit = suit
        self.value = value
        self.is_red = is_red
        self._validate()

        self.owner = None
        self.is_discarded = False
        self.is_revealed = False

    def _validate(self) -> None:
        if self.suit == TileSuit.HONOR:
            if not 1 <= self.value <= 7:
                raise MahjongException(
                    "Honor tiles must have a value between 1 and 7.")
        else:
            if not 1 <= self.value <= 9:
                raise MahjongException(
                    "Numbered tiles must have a value between 1 and 9.")

        if self.is_red and (self.suit == TileSuit.HONOR or self.value != 5):
            raise MahjongException(
                "Only 5-value numbered tiles can be red.")

    def __str__(self) -> str:
        red_marker = 'r' if self.is_red else ''
        return f'{self.suit.value}{self.value}{red_marker}'

    def __hash__(self) -> int:
        return hash((self.suit, self.value, self.is_red))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Tile):
            return False
        return (self.suit == other.suit and
                self.value == other.value and
                self.is_red == other.is_red)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Tile):
            raise MahjongException("Cannot compare Tile with non-Tile object.")
        if self.suit != other.suit:
            return self.suit.value < other.suit.value
        if self.value != other.value:
            return self.value < other.value
        return self.is_red < other.is_red

    def __gt__(self, other) -> bool:
        if not isinstance(other, Tile):
            raise MahjongException("Cannot compare Tile with non-Tile object.")
        if self.suit != other.suit:
            return self.suit.value > other.suit.value
        if self.value != other.value:
            return self.value > other.value
        return self.is_red > other.is_red

    def set_owner(self, owner) -> None:
        self.owner = owner

    def get_owner(self):
        return self.owner

    def get_image_path(self) -> str:
        return f'resources/images/tiles/{self.__str__()}.svg'

    def is_terminal(self) -> bool:
        return self.suit != TileSuit.HONOR and self.value in (1, 9)

    def is_honor(self) -> bool:
        return self.suit == TileSuit.HONOR

    def is_terminal_or_honor(self) -> bool:
        return self.is_terminal() or self.is_honor()

    def is_simple(self) -> bool:
        return not self.is_terminal_or_honor()
