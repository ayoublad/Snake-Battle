import pytest

from random import seed
from game.arena import Arena
from game.random_ai_player import RandomAIPlayer
from game.directions import Direction
from game.snake import Snake
from game.game import Game

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

def test_never_u_turn(build_game):
    game = build_game
    ai_player = RandomAIPlayer(name="AI", player_id=1)

    for _ in range(100):
        direction = ai_player.choose_direction(game)
        assert direction != Direction.UP 

@pytest.mark.parametrize("random_seed", range(100))
def test_random_ai_uses_all_valid_directions(build_game, random_seed):
    seed(random_seed)
    game = build_game
    ai_player = RandomAIPlayer(name="AI", player_id=1)
    set_direction_chosed_by_ai = set()
    for _ in range(100):
        direction = ai_player.choose_direction(game)
        set_direction_chosed_by_ai.add(direction)
        
    assert set_direction_chosed_by_ai == {Direction.LEFT, Direction.RIGHT, Direction.DOWN}

