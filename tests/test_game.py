from game.game import Game
from game.snake import Snake
from game.arena import Arena
from game.move_result import MoveResult
from game.directions import Direction, next_cell

def build_game_arena():
    arena = Arena(7, 7, walls=[(2, 4)])
    return arena

def build_snake(cells):
    snake = Snake(cells[0])
    for cell in cells[1:]:
        snake.move_forward(cell, growth=True)
    return snake

def test_collision_with_own_tail_during_normal_turn():
    arena = build_game_arena()
    snake = build_snake([(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1)])
    other_snake = build_snake([(4, 4), (4, 3), (3, 3)])
    game = Game(arena, snake, other_snake, turn=1)
    result = game.validate_move(0, Direction.UP)  
    assert result == MoveResult.VALID

def test_collision_with_own_tail_during_growth_turn():
    arena = build_game_arena()
    snake = build_snake([(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1)])
    other_snake = build_snake([(4, 4), (4, 3), (3, 3)])
    game = Game(arena, snake, other_snake, turn=5)
    result = game.validate_move(0, Direction.UP)  
    assert result == MoveResult.FATAL

def test_collision_with_own_body():
    arena = build_game_arena()
    snake = build_snake([(0, 0), (1, 0), (2, 0), (2, 1), (1, 1)])
    other_snake = build_snake([(4, 4), (4, 3), (3, 3)])
    game = Game(arena, snake, other_snake, turn=3)
    result = game.validate_move(0, Direction.UP)  
    assert result == MoveResult.FATAL

def test_collision_with_own_neck():
    arena = build_game_arena()
    snake = build_snake([(0, 0), (1, 0), (2, 0)])
    other_snake = build_snake([(4, 4), (4, 3), (3, 3)])
    game = Game(arena, snake, other_snake, turn=3)
    result = game.validate_move(0, Direction.LEFT)  
    assert result == MoveResult.REFUSED

# test s'il entre en collision avec un mur
def test_collision_with_wall():
    arena = build_game_arena()
    snake = build_snake([(2, 0), (2, 1), (2, 2), (2, 3)])
    other_snake = build_snake([(4, 4), (4, 3), (3, 3)])
    game = Game(arena, snake, other_snake, turn=1)
    result = game.validate_move(0, Direction.DOWN)
    # comme defini au dessus, (2, 4) est un mur
    # donc le résultat attendu est FATAL
    assert arena.is_wall((2, 4))  
    assert result == MoveResult.FATAL

# test s'il sort de l'arène
def test_collision_with_outside_arena():
    arena = build_game_arena()
    snake = build_snake([(0, 0), (1, 0), (1, 1), (0, 1)])
    other_snake = build_snake([(4, 4), (4, 3), (3, 3)])
    game = Game(arena, snake, other_snake, turn=1)
    result = game.validate_move(0, Direction.LEFT)
    # (-1, 1) est en dehors de l'arène
    # donc le résultat attendu est FATAL
    assert not arena.is_inside((-1, 1))  
    assert result == MoveResult.FATAL

# test s'il entre en collision avec la queue de l'autre serpent
def test_collision_with_other_snake_tail():
    arena = build_game_arena()
    snake = build_snake([(0, 0), (1, 0), (2, 0)])
    other_snake = build_snake([(2, 1), (2, 2), (2, 3)])
    game = Game(arena, snake, other_snake, turn=3)
    result = game.validate_move(0, Direction.DOWN) 
    # ici on a défini que (2, 1) est la queue de l'autre serpent
    # donc le résultat attendu est FATAL
    assert other_snake.tail() == (2, 1)
    assert result == MoveResult.FATAL
    #maintenant au tour 5, c'est un tour de croissance, la résultat devrait toujours être FATAL
    game.turn = 5
    result = game.validate_move(0, Direction.DOWN)
    assert result == MoveResult.FATAL

def test_collision_with_other_snake_body():
    arena = build_game_arena()
    snake = build_snake([(0, 0), (1, 0), (1, 1), (1, 2)])
    other_snake = build_snake([(2, 1), (2, 2), (2, 3)])
    game = Game(arena, snake, other_snake, turn=3)
    result = game.validate_move(0, Direction.RIGHT)  
    assert other_snake.is_cell_occupied((2, 2))
    assert result == MoveResult.FATAL

# test si au tour 0, le serpent peut effectuer les 4 directions sans problème
def test_valid_moves_at_turn_0():
    arena = build_game_arena()
    snake = build_snake([(1, 1)]) # c'est une case stratégique, car elle n'est pas entourée de murs et de l'autre serpent
    other_snake = build_snake([(4, 4)])
    game = Game(arena, snake, other_snake, turn=0)
    for direction in Direction:
        neighbor_cell = next_cell(snake.head(), direction)
        assert arena.is_inside(neighbor_cell) and not arena.is_wall(neighbor_cell) and not other_snake.is_cell_occupied(neighbor_cell)
        result = game.validate_move(0, direction)
        assert result == MoveResult.VALID


def test_validate_move_does_not_modify_snakes():
    # l'IA appelle validate_move pour tesster ses coups
    # la méthode doit seulement lire l'état du jeu, et ne pas modifier les serpents
    arena = build_game_arena()
    snake = build_snake([(1, 1), (1, 2), (1, 3)])
    other_snake = build_snake([(4, 1), (4, 2), (4, 3)])
    game = Game(arena, snake, other_snake, turn=3)

    snake_before = list(snake.body)
    other_snake_before = list(other_snake.body)
    for direction in Direction:
        game.validate_move(0, direction)
        assert list(snake.body) == snake_before, f"Le serpent a été modifié après validate_move avec direction {direction.name}"
        assert list(other_snake.body) == other_snake_before, f"L'autre serpent a été modifié après validate_move avec direction {direction.name}"