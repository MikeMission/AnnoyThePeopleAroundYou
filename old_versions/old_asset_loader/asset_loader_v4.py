__author__ = "Mike Mission"
__version__ = "4"
'''
This module will now contain classes of the npcs and interactive objects in the game
'''
import pygame
#background is C:\Users\cheez\OneDrive\Documents\PythonProjects\Annoy_The_People_Around_You_Project\Game_photos.Grass

# def get_cd(image):
#     variables = {
#         "test_surface":"C:\Users\cheez\OneDrive\Documents\PythonProjects\Annoy_The_People_Around_You_Project\Game_photos.Grass"
#         }
#     if image in variables:
#         return True
#^idea to get a cd when needed.

#test_font = pygame.font.SysFont('Helvetica', 20)
test_surface = pygame.image.load("game_photos/grass.xcf")
#text_surface = test_font.render("Helvetica Standard", True, (0,0,0)) 
player_surface = pygame.image.load("game_photos/character.xcf")

baby_surface = pygame.image.load("game_photos/baby.xcf")
baby_rect = baby_surface.get_rect(midbottom = (380, 590))

bush_surface = pygame.image.load("game_photos/bush.xcf")
bush_rect = bush_surface.get_rect(midbottom = (770, 395))
#text_surface will be used to actively see things while game is running

Helvetica_font = pygame.font.SysFont('Helvetica', 20)
text_surface = Helvetica_font.render("Helvetica Standard", True, (0,0,0)) 

