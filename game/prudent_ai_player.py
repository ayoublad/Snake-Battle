from game.directions import Direction
from game.move_result import MoveResult

class PrudentAIPlayer:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id

    def choose_direction(self, game):
        dict_directions_possible = dict()
        for direction in Direction:
            result_move = game.validate_move(self.player_id, direction)
            dict_directions_possible[direction] = result_move
        return dict_directions_possible

