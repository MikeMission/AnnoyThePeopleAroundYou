__author__ = "Mike Mission"
__version__ = "3"
'''
This module will now contain classes of the npcs and interactive objects in the game
'''
from random import randint
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

baby = pygame.image.load("game_photos/baby.xcf")
#text_surface will be used to actively see things while game is running

class Npc:
    def __init__(self,x,y,image):
        self.x = x
        self.y = y
        self.image = image
    def move(self):#baby movement algorithm 
        self.x += randint(3,5)
        self.y += randint(-1,1)
    def pic(self):
        return pygame.image.load(self.image)
        

npc_baby = Npc(40,400,"game_photos/baby.xcf")


#get_cd("test_surface")
