from game.strategic_ai_player import StrategicAIPlayer
from game.human_player import HumanPlayer
from game.pygame_display import PygameDisplay
from game.pygame_human_player import PygameHumanPlayer
from game.play import play_game, create_game

import pygame

WIDTH = 15
HEIGHT = 10
DENSITY = 0.2

def main():
    pygame.init()
    game = create_game(width=WIDTH, height=HEIGHT, density=DENSITY)
    name_human = input("Enter your name: ")
    players = [PygameHumanPlayer(name_human, player_id=0), StrategicAIPlayer("AI", player_id=1)] 
    display = PygameDisplay(width=WIDTH, height=HEIGHT, size_cell=40)
    display.draw_arena(game)
    display.show_turn(game, players[0])
    play_game(game=game, players=players, display=display)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        clock.tick(60) #Limit the frame rate to 60 FPS
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")