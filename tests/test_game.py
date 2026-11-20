import pytest

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

def test_entering_own_tail_on_normal_turn_is_valid():
    arena = build_game_arena()
    snake = build_snake([(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1)])
    other_snake = build_snake([(4, 4), (4, 3), (3, 3)])
    game = Game(arena, snake, other_snake, first_player=0, turn=1)
    result = game.validate_move(0, Direction.UP)  
    assert result == MoveResult.VALID

def test_collision_with_own_tail_during_growth_turn():
    arena = build_game_arena()
    snake = build_snake([(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1)])
    other_snake = build_snake([(4, 4), (4, 3), (3, 3)])
    game = Game(arena, snake, other_snake, first_player=0, turn=5)
    result = game.validate_move(0, Direction.UP)  
    assert result == MoveResult.FATAL

def test_collision_with_own_body():
    arena = build_game_arena()
    snake = build_snake([(0, 0), (1, 0), (2, 0), (2, 1), (1, 1)])
    other_snake = build_snake([(4, 4), (4, 3), (3, 3)])
    game = Game(arena, snake, other_snake, first_player=0, turn=3)
    result = game.validate_move(0, Direction.UP)  
    assert result == MoveResult.FATAL

def test_collision_with_own_neck():
    arena = build_game_arena()
    snake = build_snake([(0, 0), (1, 0), (2, 0)])
    other_snake = build_snake([(4, 4), (4, 3), (3, 3)])
    game = Game(arena, snake, other_snake, first_player=0, turn=3)
    result = game.validate_move(0, Direction.LEFT)  
    assert result == MoveResult.REFUSED

# test s'il entre en collision avec un mur
def test_collision_with_wall():
    arena = build_game_arena()
    snake = build_snake([(2, 0), (2, 1), (2, 2), (2, 3)])
    other_snake = build_snake([(4, 4), (4, 3), (3, 3)])
    game = Game(arena, snake, other_snake, first_player=0, turn=1)
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
    game = Game(arena, snake, other_snake, first_player=0, turn=1)
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
    game = Game(arena, snake, other_snake, first_player=0, turn=3)
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
    game = Game(arena, snake, other_snake, first_player=0, turn=3)
    result = game.validate_move(0, Direction.RIGHT)  
    assert other_snake.is_cell_occupied((2, 2))
    assert result == MoveResult.FATAL

# test si au tour 0, le serpent peut effectuer les 4 directions sans problème
def test_valid_moves_at_turn_0():
    arena = build_game_arena()
    snake = build_snake([(1, 1)]) # c'est une case stratégique, car elle n'est pas entourée de murs et de l'autre serpent
    other_snake = build_snake([(4, 4)])
    game = Game(arena, snake, other_snake, first_player=0, turn=0)
    for direction in Direction:
        neighbor_cell = next_cell(snake.head(), direction)
        assert arena.is_inside(neighbor_cell) and not arena.is_wall(neighbor_cell) and not other_snake.is_cell_occupied(neighbor_cell)
        result = game.validate_move(0, direction)
        assert result == MoveResult.VALID


def test_validate_move_does_not_modify_snakes():
    # l'IA appelle validate_move pour tester ses coups
    # la méthode doit seulement lire l'état du jeu, et ne pas modifier les serpents
    arena = build_game_arena()
    snake = build_snake([(0, 1), (0, 2), (0, 3)])
    other_snake = build_snake([(4, 1), (4, 2), (4, 3)])
    game = Game(arena, snake, other_snake, first_player=0, turn=3)

    snake_before = list(snake.body)
    other_snake_before = list(other_snake.body)
    for direction in Direction:
        game.validate_move(0, direction)
        assert list(snake.body) == snake_before, f"Le serpent a été modifié après validate_move avec direction {direction.name}"
        assert list(other_snake.body) == other_snake_before, f"L'autre serpent a été modifié après validate_move avec direction {direction.name}"

@pytest.mark.parametrize("first_player, turn, length_body_snake_expected", [
    (0, 4, 3), (0, 5, 4), (0, 6, 3), 
    (1, 4, 3), (1, 5, 4), (1, 6, 3)
])
def test_apply_move_switches_players_and_updates_turn(first_player, turn, length_body_snake_expected):
    arena = build_game_arena()
    snake = build_snake([(0, 1), (0, 2), (0, 3)])
    other_snake = build_snake([(4, 1), (4, 2), (4, 3)])
    game = Game(arena, snake, other_snake, first_player=first_player, turn=turn)

    assert game.turn == turn, f"Le tour initial devrait être {turn}, mais il est {game.turn}"
    assert game.current_player == first_player, f"Le joueur courant initial devrait être {first_player}, mais il est {game.current_player}"

    # On applique un mouvement valide pour le premier joueur
    direction = Direction.RIGHT
    result = game.validate_move(game.current_player, direction)
    assert result == MoveResult.VALID

    first_player_snake = game.snakes[first_player]
    old_head = first_player_snake.head()
    game.apply_move(direction)

    #vérifie que la tête du serpent du joueur courant a été mise à jour correctement après apply_move
    assert first_player_snake.head() == (old_head[0]  + 1, old_head[1]), f"La tête du serpent du joueur {first_player} n'a pas été mise à jour correctement après apply_move"

    assert game.turn == turn, f"Le tour initial devrait être {turn}, mais il est {game.turn}"
    assert game.current_player == 1 - first_player, f"Le joueur courant devrait être {1 - first_player}, mais il est {game.current_player}"

    second_player_snake = game.snakes[1 - first_player]
    old_head_second_player = second_player_snake.head()
    game.apply_move(direction)

    assert second_player_snake.head() == (old_head_second_player[0] + 1, old_head_second_player[1] ), f"La tête du serpent du joueur {1 - first_player} n'a pas été mise à jour correctement après apply_move"

    assert game.turn == turn + 1, f"Le tour initial devrait être {turn + 1}, mais il est {game.turn}"
    assert game.current_player == first_player, f"Le joueur courant initial devrait être {first_player}, mais il est {game.current_player}"

    #vérifie la longueur des serpents après les mouvements
    assert len(snake.body) == length_body_snake_expected, f"La longueur du serpent humain devrait être {length_body_snake_expected}, mais elle est {len(snake.body)}"
    assert len(other_snake.body) == length_body_snake_expected, f"La longueur du serpent IA devrait être {length_body_snake_expected}, mais elle est {len(other_snake.body)}"
   
def test_valid_movement():
    arena = build_game_arena()
    snake = build_snake([(0, 1), (0, 2), (0, 3)])
    other_snake = build_snake([(4, 1), (4, 2), (4, 3)])
    game = Game(arena, snake, other_snake, first_player=0)

    assert game.current_player == 0, f"Le joueur courant initial devrait être 0, mais il est {game.current_player}"

    result = game.play(Direction.DOWN)
    assert result == MoveResult.VALID, f"Le mouvement devrait être valide, mais le résultat est {result}"

    assert game.current_player == 1, f"Le joueur courant devrait être 1 après le mouvement, mais il est {game.current_player}"
    assert not game.is_over(), "La partie ne devrait pas être terminée après un mouvement valide"

def test_refused_movement():
    arena = build_game_arena()
    snake = build_snake([(0, 1), (0, 2), (0, 3)])
    snake_body_before = list(snake.body)
    other_snake = build_snake([(4, 1), (4, 2), (4, 3)])
    other_snake_body_before = list(other_snake.body)
    game = Game(arena, snake, other_snake, first_player=0, turn=3)

    assert game.current_player == 0, f"Le joueur courant initial devrait être 0, mais il est {game.current_player}"
    assert game.turn == 3, f"Le tour initial devrait être 3, mais il est {game.turn}"

    result = game.play(Direction.UP)  # Le serpent essaie de faire demi-tour
    assert result == MoveResult.REFUSED, f"Le mouvement devrait être refusé, mais le résultat est {result}"
    assert game.turn == 3, f"Le tour devrait rester 3 après un mouvement refusé, mais il est {game.turn}"

    assert game.current_player == 0, f"Le joueur courant devrait rester 0 après un mouvement refusé, mais il est {game.current_player}"
    assert not game.is_over(), "La partie ne devrait pas être terminée après un mouvement refusé"

    assert list(snake.body) == snake_body_before, "Le serpent a bougé après un coup refusé"
    assert list(other_snake.body) == other_snake_body_before, "L'autre serpent a bougé après un coup refusé"

@pytest.mark.parametrize("first_player", [
    0, 1
])
def test_fatal_movement(first_player):
    arena = build_game_arena()
    snake = build_snake([(0, 1), (0, 2), (0, 3)])
    snake_body_before = list(snake.body)
    other_snake = build_snake([(3, 2), (3, 3), (3, 4)])
    other_snake_body_before = list(other_snake.body)
    game = Game(arena, snake, other_snake, first_player=first_player)

    assert game.current_player == first_player, f"Le joueur courant initial devrait être {first_player}, mais il est {game.current_player}"

    result = game.play(Direction.LEFT)  # Sort de l'arène pour 0, percute un mur pour 1
    assert result == MoveResult.FATAL, f"Le mouvement devrait être fatal, mais le résultat est {result}"

    assert game.current_player == first_player, f"Le joueur courant devrait rester {first_player} après un mouvement fatal, mais il est {game.current_player}"
    assert game.is_over(), "La partie devrait être terminée après un mouvement fatal"
    assert game.winner == 1 - first_player, f"Le joueur {1 - first_player} devrait être le gagnant après un mouvement fatal du joueur {first_player}, mais le gagnant est {game.winner}"

    assert list(snake.body) == snake_body_before, "Le serpent a bougé après un coup fatal"
    assert list(other_snake.body) == other_snake_body_before, "L'autre serpent a bougé après un coup fatal"

    with pytest.raises(RuntimeError):
        game.play(Direction.RIGHT)  # Essayer de jouer après la fin de la partie devrait lever une exception
