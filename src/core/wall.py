from random import shuffle
from typing import Optional

from tile import Tile, TileSuit


class Wall:
    tiles: Optional[list[Tile]]
    dead_wall: Optional[list[Tile]]
    dead_wall_size: int

    def __init__(self,
                 tiles_saved_state: tuple[list[Tile],
                                          list[list[Tile, bool]]] = None,
                 include_red_tiles: bool = False,
                 dead_wall_size: int = 2 * 7):
        self.dead_wall_size = dead_wall_size
        if tiles_saved_state is not None:
            self.tiles = tiles_saved_state[0]
            self.dead_wall = tiles_saved_state[1]
        else:
            self.tiles = []
            self.dead_wall = []
            for suit in TileSuit:
                values = range(1, 10)
                if suit == TileSuit.HONOR:
                    values = range(1, 8)

                for value in values:
                    self.tiles.extend([Tile(suit, value)] * 4)

                if include_red_tiles and suit != TileSuit.HONOR:
                    self.tiles.remove(Tile(suit, 5))
                    self.tiles.append(Tile(suit, 5, is_red=True))

            shuffle(self.tiles)
            for tile in self.tiles[-dead_wall_size:]:
                self.dead_wall.append([tile, False])
            self.dead_wall[2][1] = True
            self.tiles = self.tiles[:-dead_wall_size]

    def __str__(self) -> str:
        return f'wall: {" ".join(str(tile) for tile in self.tiles)}\n' + \
            f'dead wall: {" ".join(str(tile) for (tile, _) in self.dead_wall)}'

    def get_dora_indicators(self) -> list[Tile]:
        return [tile for tile, revealed in self.dead_wall if revealed]

    def get_ura_dora_indicators(self) -> list[Tile]:
        return [self.dead_wall[self.dead_wall_size // 2 + i][0]
                for i, (_, revealed) in enumerate(self.dead_wall)
                if revealed]


if __name__ == "__main__":
    wall = Wall(include_red_tiles=True)
    print(wall)
    print("Dora indicators:", " ".join(
        str(tile) for tile in wall.get_dora_indicators()))
    print("Ura Dora indicators:", " ".join(str(tile)
          for tile in wall.get_ura_dora_indicators()))
