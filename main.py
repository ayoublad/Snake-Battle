from game.arena import generate_arena, start_positions
from game.game import Game
from game.strategic_ai_player import StrategicAIPlayer
from game.snake import Snake
from game.human_player import HumanPlayer
from game.console_display import ConsoleDisplay
from game.play import play_game

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
    players = [HumanPlayer(name_human, player_id=0), StrategicAIPlayer("AI", player_id=1)] 
    display = ConsoleDisplay()
    play_game(game=game, players=players, display=display)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")