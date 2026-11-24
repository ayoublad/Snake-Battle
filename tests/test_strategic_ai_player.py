import pytest

from game.arena import Arena
from game.strategic_ai_player import StrategicAIPlayer
from game.directions import Direction
from game.snake import Snake
from game.game import Game
from game.move_result import MoveResult

@pytest.fixture
def build_arena():
    return Arena(width=6, height=4, walls=[
        (0, 1), (1, 1), (2, 1),
        (0, 3), (1, 3), (2, 3)
    ])

def test_avoids_trap_and_randomly_ties_allowed_directions(build_arena):
    snake_ai = Snake(initial_position=(3, 0))
    snake_ai.move_forward(destination=(3, 1), growth=True)
    snake_ai.move_forward(destination=(3, 2), growth=True)

    assert snake_ai.neck() == (3, 1)

    snake_human = Snake(initial_position=(5, 3))

    game = Game(arena=build_arena, snake_human=snake_human, snake_ai=snake_ai, first_player=0)

    ai_player = StrategicAIPlayer(name = "AI", player_id = 1)
    direction_chosed_by_strategic_ai_player = set()
    for _ in range(100):
        direction = ai_player.choose_direction(game)
        direction_chosed_by_strategic_ai_player.add(direction)
        assert direction != Direction.LEFT
    assert direction_chosed_by_strategic_ai_player == {Direction.RIGHT, Direction.DOWN}
   
def test_dead_end_still_chooses_an_allowed_direction(build_arena):
    snake_ai = Snake(initial_position=(2, 2))
    snake_ai.move_forward(destination=(1, 2), growth=True)
    snake_ai.move_forward(destination=(0, 2), growth=True)

    assert snake_ai.neck() == (1, 2)

    snake_human = Snake(initial_position=(5, 3))

    game = Game(arena=build_arena, snake_human=snake_human, snake_ai=snake_ai, first_player=0)

    ai_player = StrategicAIPlayer(name="AI", player_id=1)
    direction_chosed_by_strategic_ai_player = set()
    for _ in range(100):
        direction = ai_player.choose_direction(game=game)
        direction_chosed_by_strategic_ai_player.add(direction)
        move_result = game.validate_move(snake_id=ai_player.player_id, direction=direction)
        assert move_result == MoveResult.FATAL
    assert direction_chosed_by_strategic_ai_player == {Direction.UP, Direction.DOWN, Direction.LEFT}