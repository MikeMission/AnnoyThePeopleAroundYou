__author__ = "Mike Mission"
__version__ = "2"

import pygame
#background is C:\Users\cheez\OneDrive\Documents\PythonProjects\Annoy_The_People_Around_You_Project\Game_photos.Grass
#https://www.youtube.com/watch?v=AY9MnQ4x3zk
def display_background(x,y):
    global test_surface
    global text_surface
    
    pygame.init()
    screen = pygame.display.set_mode((x,y))
    pygame.display.set_caption("Background Prototype")
    clock = pygame.time.Clock()
    test_font = pygame.font.SysFont('Helvetica', 20)
    test_surface = pygame.image.load("game_photos/grass.xcf")
    text_surface = test_font.render("Helvetica Standard", True, (0,0,0)) 
    #text_surface will be used to actively see things while game is running

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(test_surface,(0,0))
        screen.blit(text_surface,(0,0))

        pygame.display.update()
        clock.tick(60)

display_background(800,800)