import pytest

from random import seed
from game.arena import Arena
from game.prudent_ai_player import PrudentAIPlayer
from game.directions import Direction
from game.snake import Snake
from game.game import Game
from game.move_result import MoveResult

@pytest.fixture
def build_game():
    arena = Arena(width=7, height=7, walls=[(4, 4)])

    snake_ia = Snake(initial_position=(4, 1))
    snake_ia.move_forward(destination=(4, 2), growth=True)
    snake_ia.move_forward(destination=(4, 3), growth=True)

    assert snake_ia.neck() == (4, 2)

    snake_human = Snake(initial_position=(1, 3))
    snake_human.move_forward(destination=(0, 3), growth=True)

    assert snake_human.neck() == (1, 3)

    game = Game(arena=arena, snake_human=snake_human, snake_ai=snake_ia, first_player=0)

    return game

def test_never_fatal_move(build_game):
    game = build_game
    ai_player = PrudentAIPlayer(name="AI", player_id=1)
    direction_chosed_by_prudent_ai_player = set()
    for _ in range(100):
        direction = ai_player.choose_direction(game)
        direction_chosed_by_prudent_ai_player.add(direction)
    assert direction_chosed_by_prudent_ai_player == {Direction.LEFT, Direction.RIGHT}

def test_return_always_a_move_even_if_all_are_fatal():
    arena = Arena(width=4, height=4, walls=[(0, 1)])

    snake_ai = Snake((2, 0))
    snake_ai.move_forward(destination = (1, 0), growth = True)
    snake_ai.move_forward(destination = (0, 0), growth = True)

    snake_human = Snake((3, 3))
    snake_human.move_forward(destination = (2, 3), growth = True)
    snake_human.move_forward(destination = (1, 3), growth = True)

    game = Game(arena=arena, snake_human=snake_human, snake_ai=snake_ai, first_player=0)

    ai_player = PrudentAIPlayer(name="AI", player_id=1)
    direction_chosed_by_prudent_ai_player = set()
    for _ in range(100):
        direction = ai_player.choose_direction(game=game)
        direction_chosed_by_prudent_ai_player.add(direction)
        assert direction != Direction.RIGHT
        assert game.validate_move(1, direction) == MoveResult.FATAL
    assert direction_chosed_by_prudent_ai_player == {Direction.UP, Direction.LEFT, Direction.DOWN}