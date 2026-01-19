'''
File loads the assets for 'stage_1' classroom.
'''

__author__ = "Mike Mission"
__status__ = "ALPHA"
__license__ = "MIT"

import pygame 
pygame.init()
from core_tools.tools import collision_with_static,change_sprite
from random import randint

player_sprites = change_sprite()

player_idle = player_sprites["player_idle"]
player_walk_down = player_sprites["player_walk_down"]
player_walk_up = player_sprites["player_walk_up"]
player_left_frames = player_sprites["player_left_frames"]
player_left_frame_index = player_sprites["player_left_frame_index"]
player_right_frames = player_sprites["player_right_frames"]
player_right_frame_index = player_sprites["player_right_frame_index"]
player_surf = player_sprites["player_surf"]

#spam sprites
Helvetica_font = pygame.font.SysFont('Helvetica', 20)
Helvetica_font_small = pygame.font.SysFont('Helvetica', 10)
time_font = pygame.font.SysFont('Helvetica',50,False,False)
#may need to be rendered inside classroom_game, since has to be updated with the amount u have to click.
#drum_kit = pygame.transform.scale(drum_kit,(250,225))

#text for the task
st1_line = 0
st_1_txt_list = ["You are frustrated with musicians being so loud during your study periods","so you decide to detune their instruments at lunch..."]

#text for stage 2
st2_line = 0
st_2_txt_list = ["...","What","Are","You","Doing?"]

#text for end 
st_3_txt_list = ["...","You managed to escape for today unnoticed","You go home after a day of school","stage 1 complete"]
st3_line = 0
bg = pygame.image.load("stage_1/classroom_image/bg.xcf")
#collideable rectangles
wall_1 = pygame.draw.rect(bg,(0,0,0),(23,271,505,31))
wall_2 = pygame.draw.rect(bg,(0,0,0),(769,0,31,800))
wall_3 = pygame.draw.rect(bg,(0,0,0),(0,0,31,800))
wall_4 = pygame.draw.rect(bg,(0,0,0),(0,0,100,31))
wall_5 = pygame.draw.rect(bg,(0,0,0),(250,0,600,31))
#in a list incase need to add a collideable obj

class Enemy():
    def __init__(self,
                 name,
                 x,
                 y,
                 difficulty,
                 idle_frame,
                 direction
                 ):
        #(600,500)
        self.name = name
        self.rect = idle_frame.get_rect(topleft = (x,y)) 
        self.difficulty = difficulty
        self.idle_frame = pygame.transform.scale(idle_frame,(45,50))
        self.direction = direction
        #self.frame will be rewritten when animated
        self.frame = pygame.transform.scale(idle_frame,(45,50))

        self.gpli = 0
        self.gpri = 0
        self.right_frames = []

    def generate_frames(self,frame_direction,frame1,frame2):
        ''' generates the frames animation '''
        #scale each frame 
        frame1 = pygame.transform.scale(frame1,(45,50))
        frame2 = pygame.transform.scale(frame2,(45,50))
        #indexes

        if frame_direction == "left":
            self.left_frames = [frame1,frame2]
        elif frame_direction == "right":
            self.right_frames = [frame1,frame2]

    def move(self):
        ''' moves the enemy '''
        if self.direction == "right":
            self.rect.x += self.difficulty 
        elif self.direction == "left":
            self.rect.x -= self.difficulty


        #set the direction to the other when collided
        if self.rect.colliderect(wall_2):
            if collision_with_static(self.rect,wall_2):
                self.direction = "left"

        elif self.rect.colliderect(wall_3):
            if collision_with_static(self.rect,wall_3):
                self.direction = "right"
            
                
    def death_msg(self):
        ''' updates death message '''
        return Helvetica_font.render(f"you died to {self.name}",False,(255,0,0))

guitar_player = Enemy(
    "guitar_player",
    300,400,
    1,
    pygame.image.load("stage_1/classroom_image/enemy_surf/guitar_player/idle.xcf"),
    "right"
)

bass_player = Enemy(
    "bass_player",
    600,500,
    1.5,
    pygame.image.load("stage_1/classroom_image/enemy_surf/bass_player/idle.xcf"),
    "right"
)

drum_player = Enemy(
    "drum_player",
    200,200,
    0.5,
    pygame.image.load("stage_1/classroom_image/enemy_surf/drum_player/idle.xcf"),
    "left"
)

singer = Enemy(
    "singer",
    150,150,
    0.5,
    pygame.image.load("stage_1/classroom_image/enemy_surf/singer/idle.xcf"),
    "left"
)

cat = Enemy(
    "cat",
    340,287,
    0,
    pygame.image.load("stage_1/classroom_image/cat_1.xcf"),
    "None"
)
#cat will not be moving at all though but using right_frames cuz it feels right
cat_surfaces = [pygame.image.load("stage_1/classroom_image/cat_1.xcf"),
                pygame.image.load("stage_1/classroom_image/cat_2.xcf"),
                pygame.image.load("stage_1/classroom_image/cat_3.xcf"),
                pygame.image.load("stage_1/classroom_image/cat_4.xcf")]

cat.right_frames = [pygame.transform.scale(x,(60,70)) for x in cat_surfaces]

enemies = [guitar_player,bass_player,drum_player,singer]
collidable_rects = [wall_1,wall_2,wall_3,wall_4,wall_5]

for entity in enemies:
    for direction in ["left","right"]:
        entity.generate_frames(direction,pygame.image.load(f"stage_1/classroom_image/enemy_surf/{entity.name}/{direction}1.xcf"),pygame.image.load(f"stage_1/classroom_image/enemy_surf/{entity.name}/{direction}2.xcf"))

class Instrument():
    def __init__(
            self,
            minigame,
            surf,
            x,y,
            complete_surf
                 ):
        
        self.minigame = minigame
        self.surf = surf 
        self.rect = self.surf.get_rect(midbottom = (x,y))
        self.complete_surf = complete_surf

        if self.minigame == "spam":
            self.space_amount = 0
            self.space_requirement = randint(40,70)
        elif self.minigame == "bar":
            self.stopped = False 
        self.won = None



electric_guitar = Instrument(
    "bar",
    pygame.image.load("stage_1/classroom_image/electric_guitar.xcf"),
    700,700,
    pygame.image.load("stage_1/classroom_image/g_electric_guitar.xcf")
    )

bass_guitar = Instrument(
    "bar",
    pygame.image.load("stage_1/classroom_image/bass.xcf"),
    490,685,
    pygame.image.load("stage_1/classroom_image/g_bass.xcf")
    )
drum_kit = Instrument(
    "spam",
    pygame.image.load("stage_1/classroom_image/drum_kit.xcf"),
    185,750,
    pygame.image.load("stage_1/classroom_image/g_drum_kit.xcf")
    )
mic = Instrument(
    "spam",
    pygame.image.load("stage_1/classroom_image/mic.xcf"),
    160,440,
    pygame.image.load("stage_1/classroom_image/g_mic.xcf")
    )
instruments = [electric_guitar,bass_guitar,drum_kit,mic]
