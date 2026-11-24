from random import choice
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

        valid_move = [direction for direction, result in dict_directions_possible.items() if result == MoveResult.VALID]
        if valid_move:
            return choice(valid_move)
        else:
            move_not_refused = [direction for direction, result in dict_directions_possible.items() if result != MoveResult.REFUSED]
            return choice(move_not_refused)
