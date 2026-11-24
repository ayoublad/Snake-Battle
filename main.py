from game.strategic_ai_player import StrategicAIPlayer
from game.human_player import HumanPlayer
from game.console_display import ConsoleDisplay
from game.play import play_game, create_game

import random

WIDTH = 15
HEIGHT = 10
DENSITY = 0.2

def main():
    game = create_game(width=WIDTH, height=HEIGHT, density=DENSITY)
    name_human = input("Enter your name: ")
    players = [HumanPlayer(name_human, player_id=0), StrategicAIPlayer("AI", player_id=1)] 
    display = ConsoleDisplay()
    play_game(game=game, players=players, display=display)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")