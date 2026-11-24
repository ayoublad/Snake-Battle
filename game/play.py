from game.move_result import MoveResult
from game.arena import generate_arena, start_positions
from game.snake import Snake
from game.game import Game
from random import choice

def create_game(width, height, density):
    arena = generate_arena(width=width, height=height, density=density)
    start_cell_for_human, start_cell_for_ai = start_positions(width=width, height=height)
    snake_human = Snake(start_cell_for_human)
    snake_ai = Snake(start_cell_for_ai)
    first_player = choice([0, 1])
    game = Game(arena=arena, snake_human=snake_human, snake_ai=snake_ai, first_player=first_player)
    return game


def play_game(game, players, display=None):
    while not game.is_over():
        current_player = players[game.current_player]
        if display is not None:
            display.show_turn(game=game, player=current_player)
        direction = current_player.choose_direction(game)
        result_move = game.play(direction)
        while result_move == MoveResult.REFUSED:
            if display is not None:
                display.show_refused(player=current_player)
            direction = current_player.choose_direction(game)
            result_move = game.play(direction)
        if display is not None:
            display.show_move(player=current_player, direction=direction)
    if display is not None:
        display.show_game_over(game=game, winner=players[game.winner].name)
    return game.winner