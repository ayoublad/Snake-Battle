from game.directions import Direction
import pygame

class PygameHumanPlayer:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id

    def choose_direction(self, game):
        print("Please choose a direction (↑=up, ↓=down, ←=left, →=right) : ")
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        return Direction.UP
                    elif event.key == pygame.K_LEFT:
                        return Direction.LEFT
                    elif event.key == pygame.K_DOWN:
                        return Direction.DOWN
                    elif event.key == pygame.K_RIGHT:
                        return Direction.RIGHT
                    else:
                        print("Invalid input. Please choose a direction (↑=up, ↓=down, ←=left, →=right) : ")
            clock.tick(60)  # Limit the frame rate to 60 FPS