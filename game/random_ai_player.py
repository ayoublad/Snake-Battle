import random
from game.directions import Direction
from game.move_result import MoveResult

class RandomAIPlayer:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id

    def choose_direction(self, game):
        list_directions_possible = []
        for direction in Direction:
            result_move = game.validate_move(self.player_id, direction)
            if result_move != MoveResult.REFUSED:
                list_directions_possible.append(direction)
        return random.choice(list_directions_possible)
    