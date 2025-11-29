from enums import Wind
from hand import Hand, Meld
from tile import Tile


class Player:
    name: str
    hand: Hand
    score: int
    melds: list[Meld]
    seat_wind: Wind
    is_dealer: bool

    is_riichi: bool
    is_ippatsu: bool
    riichi_turn: int | None

    def __init__(self, name: str, seat_wind: Wind,
                 starting_score: int = 25000):
        self.name = name
        self.score = starting_score

        self.reset_for_new_round(seat_wind)

    def __str__(self) -> str:
        dealer_str = ' (Dealer)' if self.is_dealer else ''
        riichi_str = ' (Riichi)' if self.is_riichi else ''

        return (f'{self.name} ({self.seat_wind.name}){dealer_str}{riichi_str}'
                f' - Score: {self.score} - '
                f'Hand: {len(self.hand.concealed_tiles)} tiles - '
                f'Melds: {len(self.melds)}')

    def draw_tile(self, tile: Tile) -> None:
        self.hand.add_tile(tile)
        tile.set_owner(self)
        self.is_ippatsu = False

    def discard_tile(self, tile: Tile) -> bool:
        is_success = self.hand.discard_tile(tile)
        if is_success:
            tile.is_discarded = True
            tile.owner = self
        return is_success

    def add_meld(self, meld: Meld) -> None:
        self.melds.append(meld)
        meld.set_original_owner(self)
        for tile in meld.tiles:
            if tile in self.hand.concealed_tiles:
                self.hand.concealed_tiles.remove(tile)

        self.is_ippatsu = False

    def declare_riichi(self, current_turn: int) -> bool:
        if self.is_riichi:
            return False

        if len(self.melds) > 0:
            return False

        if self.score < 1000:  # TODO - check if this is in rules
            return False

        self.is_riichi = True
        self.is_ippatsu = True
        self.riichi_turn = current_turn
        self.score -= 1000

        return True

    def can_call_pon(self, tile: Tile) -> bool:
        if self.is_riichi:
            return False
        return self.hand.can_pon(tile)

    def can_call_kan(self, tile: Tile) -> bool:
        return self.hand.can_kan(tile)

    def can_call_chi(self, tile: Tile) -> bool:
        if self.is_riichi:
            return False
        return (True if self.hand.can_chii(tile) else False)

    def add_score(self, points: int) -> None:
        self.score += points

    def deduct_score(self, points: int) -> None:
        self.score -= points

    def reset_for_new_round(self, new_seat_wind: Wind) -> None:
        self.hand = Hand()
        self.melds = []
        self.seat_wind = new_seat_wind
        self.is_dealer = new_seat_wind == Wind.EAST

        self.is_riichi = False
        self.is_ippatsu = False
        self.riichi_turn = None
