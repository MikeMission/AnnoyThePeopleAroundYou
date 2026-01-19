'''
This module will now contain classes of the npcs and interactive objects in the game
'''
__author__ = "Mike Mission"
__version__ = "5"
__status__ = "development"
__license__ = "MIT"

import pygame

#background is C:\Users\cheez\OneDrive\Documents\PythonProjects\Annoy_The_People_Around_You_Project\Game_photos.Grass

# def get_cd(image):
#     variables = {
#         "test_surface":"C:\Users\cheez\OneDrive\Documents\PythonProjects\Annoy_The_People_Around_You_Project\Game_photos.Grass"
#         }
#     if image in variables:
#         return True
#^idea to get a cd when needed.
pygame.font.init()

#game_active screen
background = pygame.image.load("stage_0/tutorial_image/grass.xcf")

player_surf = pygame.image.load("stage_0/tutorial_image/character.xcf")


npc_state = "idle"

#font
Helvetica_font = pygame.font.SysFont('Helvetica', 20)

def upd_state():
    global baby_surf,task_baby
    if npc_state == "idle":
        baby_surf = pygame.image.load("stage_0/tutorial_image/baby_idle.xcf")
        task_baby = Helvetica_font.render("Give a microphone to the baby", True, (0,0,0)) 
    elif npc_state == "crying":
        baby_surf = pygame.image.load("stage_0/tutorial_image/baby_cry.xcf")
        task_baby = Helvetica_font.render("Escape without alerting the people",True,(0,0,0))

upd_state()

baby_rect = baby_surf.get_rect(midbottom = (87, 717))

bush_surf = pygame.image.load("stage_0/tutorial_image/bush.xcf")
bush_surf = pygame.transform.scale(bush_surf, (600,300))
bush_rect = bush_surf.get_rect(midbottom = (215, 372))

bush2_surf = pygame.image.load("stage_0/tutorial_image/bush.xcf")
bush2_surf = pygame.transform.scale(bush2_surf, (600,300))
bush2_rect = bush2_surf.get_rect(midbottom = (1000, 800))


#item
microphone_surf = pygame.image.load("stage_0/tutorial_image/microphone.xcf")
microphone_rect = microphone_surf.get_rect(midbottom = (27, 450))

#enemies
enemy_frame1 = pygame.image.load("stage_0/tutorial_image/enemy_walk1.xcf")
enemy_frame2 = pygame.image.load("stage_0/tutorial_image/enemy_walk2.xcf")
enemy_frames = [enemy_frame1,enemy_frame2]
enemy_index = 0
enemy_surf = enemy_frames[enemy_index]

enemy_rect = enemy_surf.get_rect(midbottom = (650, 730))

#gate
gate_surf = pygame.image.load("stage_0/tutorial_image/tutorial_finish_gate.xcf")
gate_rect = gate_surf.get_rect(midbottom = (50,50))

#game over screen
game_over_font = pygame.font.SysFont('Helvetica', 70)
x_game_text = game_over_font.render("Game Over", True, (255,255,255))
restart_q = Helvetica_font.render("'press r to restart'",True,(255,255,255))

def death_by(deathobj):#passes death obj from movement.
    global deathmessage
    deathmessage = Helvetica_font.render("Death by: "+str(deathobj),True, (255,0,0))

deathmessage = Helvetica_font.render("Death by NULL", True, (255,255,255))
#finish
finish_tutorial_txt = game_over_font.render("Tutorial Completed", True, (0,255,0))
finish_q = Helvetica_font.render("'press r to continue'",True,(255,255,255))

#tutorial text 
tutorial_texts = ["WASD to move","Do not hit the bushes..."]
tutorial_texts = [Helvetica_font.render(x,True,(0,0,0),(255,255,255)) for x in tutorial_texts]

text_index = 0

