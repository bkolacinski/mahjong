from enums import Wind
from player import Player
from round import Round


class Game:
    players: list[Player]
    rounds: list[Round]

    current_round_index: int
    current_round_wind: Wind

    riichi_sticks: int
    starting_score: int

    def __init__(
        self,
        players: list[Player],
        starting_score: int = 25000,
        starting_wind: Wind = Wind.EAST,
    ):
        self.players = players
        self.starting_score = starting_score
        self.riichi_sticks = 0

        self.rounds = []
        self.current_round_index = 0
        self.current_round_wind = starting_wind
