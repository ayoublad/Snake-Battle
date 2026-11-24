from random import choice
from game.directions import Direction, next_cell
from game.move_result import MoveResult

class StrategicAIPlayer:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id

    def choose_direction(self, game):
        dict_directions_possible = dict()
        for direction in Direction:
            move_result = game.validate_move(self.player_id, direction)
            dict_directions_possible[direction] = move_result

        set_cell_blocked = set(set(game.snakes[0].body) | set(game.snakes[1].body))
        move_valid = [direction for direction, result in dict_directions_possible.items() if result == MoveResult.VALID]
        if move_valid:
            dict_score_each_move = dict()
            for move in move_valid:
                set_visited = game.arena.reachable_cells(initial_cell=next_cell(game.snakes[self.player_id].head(), move), set_cell_blocked=set_cell_blocked)
                dict_score_each_move[move] = len(set_visited)
            best_score = max(dict_score_each_move.values())
            candidates_for_best_move = [move for move, score in dict_score_each_move.items() if score == best_score]
            return choice(candidates_for_best_move)
        else:
            move_not_refused = [direction for direction, result in dict_directions_possible.items() if result != MoveResult.REFUSED]
            return choice(move_not_refused)        
        
