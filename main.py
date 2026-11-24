from game.arena import generate_arena, start_positions
from game.game import Game
from game.prudent_ai_player import PrudentAIPlayer
from game.snake import Snake
from game.human_player import HumanPlayer
from game.console_display import ConsoleDisplay
from game.move_result import MoveResult

import random

WIDTH = 15
HEIGHT = 10
DENSITY = 0.2

def main():
    arena = generate_arena(width=WIDTH, height=HEIGHT, density=DENSITY)
    start_cell_for_human, start_cell_for_ai = start_positions(WIDTH, HEIGHT)
    snake_human = Snake(start_cell_for_human)
    snake_ai = Snake(start_cell_for_ai)
    first_player = random.choice([0, 1])
    game = Game(arena=arena, snake_human=snake_human, snake_ai=snake_ai, first_player=first_player)
    name_human = input("Enter your name: ")
    players = [HumanPlayer(name_human, player_id=0), PrudentAIPlayer("AI", player_id=1)] 
    display = ConsoleDisplay()
    while not game.is_over():
        current_player = players[game.current_player]
        print(f"Turn {game.turn} - It's up to {current_player.name} to play.\n")
        print(display.render(game))
        direction = current_player.choose_direction(game)
        result_move = game.play(direction)
        while result_move == MoveResult.REFUSED:
            print("No U-turns")
            direction = current_player.choose_direction(game)
            result_move = game.play(direction)
        print(f"{current_player.name} played direction: {direction.name}\n")
    print(display.render(game))
    print(f"Game over! Winner: {players[game.winner].name}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")