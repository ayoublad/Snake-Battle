from game.move_result import MoveResult
from game.directions import next_cell

class Game():
    def __init__(self, arena, snake_human, snake_ai, turn=0):
        self.arena = arena
        self.snakes = [snake_human, snake_ai]
        self.turn = turn

    def is_growth_turn(self):
        """Retourne True si c'est un tour de croissance, False sinon."""
        return self.turn % 5 == 0

    def validate_move(self, snake_id, direction):
        """Vérifie si le déplacement du serpent vers la destination est valide.
        Retourne un MoveResults indiquant le résultat du déplacement."""
        current_snake = self.snakes[snake_id]
        other_snake = self.snakes[1 - snake_id]
        next_position = next_cell(current_snake.head(), direction=direction)

        # Vérifie si notre serpent essaie de faire un demi-tour
        if next_position == current_snake.neck():
            return MoveResult.REFUSED

        # Vérifie si la prochaine position est à l'intérieur de l'arène et n'est pas un mur
        if not self.arena.is_inside(next_position) or self.arena.is_wall(next_position):
            return MoveResult.FATAL

        # Vérifie si la prochaine position est occupée par notre propre serpent
        if current_snake.is_cell_occupied(next_position):
            if next_position != current_snake.tail() or (self.is_growth_turn() and next_position == current_snake.tail()):
                return MoveResult.FATAL

        # Vérifie si la prochaine position est occupée par l'autre serpent
        if other_snake.is_cell_occupied(next_position):
            return MoveResult.FATAL
        return MoveResult.VALID