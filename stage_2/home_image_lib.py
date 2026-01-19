__authour__ = "Mike Mission"
__status__ = "ALPHA"
__license__ = "MIT"
'''
loader for home_game
'''

import pygame
pygame.init()
from core_tools.tools import change_sprite,collision_with_static
from random import randint
player_sprites = change_sprite()

player_idle = player_sprites["player_idle"]
player_walk_down = player_sprites["player_walk_down"]
player_walk_up = player_sprites["player_walk_up"]
player_left_frames = player_sprites["player_left_frames"]
player_left_frame_index = player_sprites["player_left_frame_index"]
player_right_frames = player_sprites["player_right_frames"]
player_right_frame_index = player_sprites["player_right_frame_index"]

bg = pygame.image.load("stage_2/home_images/bg.xcf")
bg_ = pygame.image.load("stage_2/home_images/bg.xcf")

#playersprites are stored in stage_1 
#font
interact_font = pygame.font.SysFont("Helvetica", 20)
Helvetica_font = pygame.font.SysFont("Helvetica",30)
speech_font = pygame.font.SysFont("Helvetica",15)
time_font = pygame.font.SysFont('Helvetica',50,False,False)

class interactive_object():
    def __init__(
            self,
            name,
            surf,
            x,y,
            minigame
                 ):
        self.name = name 
        self.surf = surf 
        self.rect = surf.get_rect(topleft = (x,y))
        self.minigame = minigame 
        self.won = False #var to keep track of minigame finished...
        self.text = interact_font.render("'e to interact'",True,(0,0,0))
        self.interaction_tab = False
        self.disabled = False

        if (self.minigame == "bar"): self.stopped = False 
        elif (self.minigame == "spam"):
            self.space_requirement = randint(40,60)
            self.space_amount = 0
        elif (self.minigame == "click&drag"): self.clicked_obj = None 

        if self.name == "tv":
            self.won = True #well done, u completed tv's task how amazing (there's no task, just to make all statement true in program)

        #click task won't need any special attributes

    def interaction_text(self):
        ''' returns rects for text to go on '''
        if self.name == "fridge":return (525,375)
        elif self.name == "toys":return (275,524)
        elif self.name == "alarm_clock":return (665,320)
        elif self.name == "r_bin":return (390,65)
        elif self.name == "tv":return (900,900) #get outta here


bin = interactive_object(
    "bin",
    pygame.image.load("stage_2/home_images/bin.xcf"),
    315,65,
    "click&drag")

r_bin = interactive_object(
    "r_bin",
    pygame.image.load("stage_2/home_images/recycle.xcf"),
    381,65,
    "click&drag")

toys = interactive_object(
    "toys",
    pygame.image.load("stage_2/home_images/toys.xcf"),
    231,505,
    "spam")

alarm_clock = interactive_object(
    "alarm_clock",
    pygame.image.load("stage_2/home_images/alarm.xcf"),
    710,320,
    "bar"
)

fridge = interactive_object(
    "fridge",
    pygame.image.load("stage_2/home_images/fridge.xcf"),
    505,325,
    "click"
)
tv = interactive_object(
    "tv",
    pygame.image.load("stage_2/home_images/tv.xcf"),
    370,215,
    "None"
)

interactive_objects = [r_bin,toys,alarm_clock,fridge,tv]#tv isn't a interactive object but just for the sake of it not blitting 

#collideable walls
counter_1 = pygame.draw.rect(bg,(190,190,190),(539,62,209,40))
counter_2 = pygame.draw.rect(bg,(190,190,190),(710,102,38,270))

collidable_rects = [
    fridge.rect,toys.rect,r_bin.rect,bin.rect,tv.rect,
    counter_1,counter_2
    ]
#exhaustive list full of all the collideable walls (so much effort)
wall_rect_properties = ((31,172,145,31),(265,31,32,170),(297,169,206,32),(470,200,33,258),(473,574,33,300),(0,163,33,700),(0,0,800,32),(0,768,800,32),(0,10,3,300))

for rect_property in wall_rect_properties:
    collidable_rects.append(pygame.draw.rect(bg,(0,0,0),rect_property))

couch_1 = pygame.draw.rect(bg_,(255,200,200),(70,251,125,460))
couch_2 = pygame.draw.rect(bg_,(255,200,200),(191,544,240,170))
dad_switch = pygame.draw.rect(bg_,(255,200,200),(620,544,10,10))

collidable_rects.append(couch_1)
collidable_rects.append(couch_2)
collidable_rects.append(dad_switch)

class clickable_object:
    def __init__(self,x,y,surf):
        self.surf = surf
        self.rect = self.surf.get_rect(topleft=(x,y)) 
        self.clicked = False

trash_bg = pygame.image.load("stage_2/home_images/trash/trash_bg.xcf")
trash_1 = clickable_object(265,264,pygame.image.load("stage_2/home_images/trash/trash_1.xcf"))
trash_2 = clickable_object(400,264,pygame.image.load("stage_2/home_images/trash/trash_2.xcf"))
r_trash_1 = clickable_object(265,364,pygame.image.load("stage_2/home_images/trash/r_trash_1.xcf"))
r_trash_2 = clickable_object(400,364,pygame.image.load("stage_2/home_images/trash/r_trash_2.xcf"))

click_drag_objects = [
    [trash_1.rect,trash_1.surf],
    [trash_2.rect,trash_2.surf],
    [r_trash_1.rect,r_trash_1.surf],
    [r_trash_2.rect,r_trash_2.surf]
                     ]

fridge_bg = pygame.image.load("stage_2/home_images/fridge/fridge_bg.xcf")
milk = clickable_object(291,180,pygame.transform.scale(pygame.image.load("stage_2/home_images/fridge/milk.xcf"),(100,100)))
cake = clickable_object(280,580,pygame.transform.scale(pygame.image.load("stage_2/home_images/fridge/cake.xcf"),(100,100)))
bread = clickable_object(450,190,pygame.transform.scale(pygame.image.load("stage_2/home_images/fridge/bread.xcf"),(100,100)))
drink = clickable_object(200,400,pygame.transform.scale(pygame.image.load("stage_2/home_images/fridge/drink.xcf"),(200,100)))

clickable_objects = [
    [milk.rect,milk.surf,milk.clicked],
    [cake.rect,cake.surf,cake.clicked],
    [bread.rect,bread.surf,bread.clicked],
    [drink.rect,drink.surf,drink.clicked]
]

class Enemy:
    def __init__(self,name,x,y,text,direction,difficulty):
        self.name = name 
        self.surf = pygame.transform.scale(pygame.image.load(f"stage_2/home_images/{self.name}/idle.xcf"),(50,90)) 
        self.rect = self.surf.get_rect(topleft = (x,y))
        self.text = speech_font.render(text,True,(255,255,255))
        self.direction = direction
        self.animate_index = 0
        self.disabled = False
        self.difficulty = difficulty

    def talk(self,win):
        if self.name not in ("mother","father"):
            self.surf = pygame.transform.scale(pygame.image.load(f"stage_2/home_images/{self.name}/talk.xcf"),(50,90))
        win.blit(self.text,(self.rect.x + 5,self.rect.y - 30))

    def move(self,game_difficulty):
        for rect in collidable_rects:
            if rect.colliderect(self.rect):
                if rect == counter_1 or rect == collidable_rects[9]: #counter for father, wall for mother
                    self.direction = "down"
                elif rect == collidable_rects[4]: #brother
                    self.direction = "left"
                elif rect == collidable_rects[16]: #brother
                    self.direction = "right"
                elif rect == collidable_rects[17]: #mother
                    self.direction = "up"
                elif rect == collidable_rects[18]: #father
                    self.direction = "up"
        self.difficulty = game_difficulty
        if self.direction == "right":self.rect.x += self.difficulty
        elif self.direction == "left":self.rect.x -= self.difficulty
        elif self.direction == "up":self.rect.y -= self.difficulty
        elif self.direction == "down":self.rect.y += self.difficulty

    def idle(self):
        self.surf = pygame.transform.scale(pygame.image.load(f"stage_2/home_images/{self.name}/idle.xcf"),(50,90)) 
    
    def animate(self):
        if self.name == "sister":
            frame_1 = frame_2 = self.surf
        else:
            frame_1 = pygame.transform.scale(pygame.image.load(f"stage_2/home_images/{self.name}/{self.direction}_1.xcf"),(50,90))
            frame_2 = pygame.transform.scale(pygame.image.load(f"stage_2/home_images/{self.name}/{self.direction}_2.xcf"),(50,90))

        if self.animate_index == 0:
            self.animate_index = 1
        else:
            self.animate_index = 0

        self.frames = [frame_1,frame_2]
        self.surf = self.frames[self.animate_index]
    
    
brother = Enemy(
    "brother",
    150,396,
    "hola mi hermano",
    "right",
    1
    )

sister = Enemy(
    "sister",
    600,600,
    "...",
    "None",
    0
)

mother = Enemy(
    "mother",
    300,264,
    "cook the rice",
    "down",
    2
)

father = Enemy(
    "father",
    600,200,
    "ya good one justin",
    "down",
    1
)
enemies = [brother,sister,mother,father]

state_2_txt = ["...","avoid family members at all costs."]
state_2_txt_index = 0
