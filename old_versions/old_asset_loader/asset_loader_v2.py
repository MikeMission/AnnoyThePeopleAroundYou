__author__ = "Mike Mission"
__version__ = "2"
'''
This file will now store all the assets for the game to load.
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
player = pygame.image.load("game_photos/character.xcf")

#text_surface will be used to actively see things while game is running



#get_cd("test_surface")

