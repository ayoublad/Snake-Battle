from game.move_result import MoveResult
from game.directions import next_cell

class Game():
    def __init__(self, arena, snake_human, snake_ai, first_player, turn=0):
        self.arena = arena
        self.snakes = [snake_human, snake_ai]
        self.turn = turn
        self.first_player = first_player
        self.current_player = first_player 
        self.winner = None  

    def is_growth_turn(self):
        """Retourne True si c'est un tour de croissance, False sinon."""
        return self.turn % 5 == 0

    def apply_move(self, direction):
        """
        Applique un déplacement déjà validé.

        Précondition :
        validate_move(current_player, direction) doit avoir retourné MoveResult.VALID.
        """
        current_snake = self.snakes[self.current_player]
        next_position = next_cell(current_snake.head(), direction=direction)
        current_snake.move_forward(next_position, self.is_growth_turn())

        self.current_player = 1 - self.current_player # on passe au joueur suivant
        if self.current_player == self.first_player:
            self.turn += 1

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

    def is_over(self):
        """Retourne True si la partie est terminée, False sinon."""
        return self.winner is not None

    def play(self, direction):
        if self.is_over():
            raise Exception("La partie est déjà terminée.")
        
        result = self.validate_move(snake_id=self.current_player, direction=direction)
        if result == MoveResult.VALID:
            self.apply_move(direction=direction)

        if result == MoveResult.FATAL:
            self.winner = 1 - self.current_player

        return result