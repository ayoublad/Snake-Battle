import pygame

pygame.init() #Initialize all modules

pygame.display.set_caption("Snake Battle")
screen = pygame.display.set_mode(size=(800, 600))

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 255, 0)) #Fill the screen with green color
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(100, 100, 200, 200)) #Draw a red rectangle
    pygame.display.flip() #Update the display
    clock.tick(60) #Limit the frame rate to 60 FPS
pygame.quit()
