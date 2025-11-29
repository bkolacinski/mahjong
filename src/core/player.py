from hand import Hand, Meld


class Player:
    name: str
    hand: Hand
    score: int
    melds: list[Meld]
    seat_wind: int
    is_dealer: bool

    def __init__(self, name: str):
        pass
