'''
The lib that will hold the assets for train game
'''

__authour__ = "Mike Mission"
__status__ = "ALPHA"
__license__ = "MIT"
import pygame 
from random import randint,choice
pygame.init()

from core_tools.tools import change_sprite
player_sprites = change_sprite()

player_idle = player_sprites["player_idle"]
player_walk_down = player_sprites["player_walk_down"]
player_walk_up = player_sprites["player_walk_up"]
player_left_frames = player_sprites["player_left_frames"]
player_left_frame_index = player_sprites["player_left_frame_index"]
player_right_frames = player_sprites["player_right_frames"]
player_right_frame_index = player_sprites["player_right_frame_index"]

bg = pygame.image.load("stage_3/train_images/bg.xcf")
bg_2 = pygame.image.load("stage_3/train_images/bg_2.xcf")
bg_ = pygame.image.load("stage_3/train_images/bg.xcf") #used for drawing collideable rects

#fonts
font = pygame.font.SysFont("Helvetica",10)
big_font = pygame.font.SysFont("Helvetica",35)

wall_properties = ((75,0,5,800),(715,0,5,800))
train_window_1 = pygame.image.load("stage_3/train_images/train_window_1.xcf")
train_window_2 = pygame.image.load("stage_3/train_images/train_window_2.xcf")

drunk_font = pygame.font.SysFont("Helvetica",20)
drunk_idle = pygame.image.load("stage_3/train_images/drunk/idle.xcf")
drunk_talk = pygame.image.load("stage_3/train_images/drunk/talk.xcf")
drunk_rect = drunk_idle.get_rect(topleft = (500,10))
drunk_frames = [pygame.image.load("stage_3/train_images/drunk/frame_1.xcf"),pygame.image.load("stage_3/train_images/drunk/frame_2.xcf")]
drunk_index = 0
drunk_animate = True


#sprite for enemy at state 2
drunk_idle1 = pygame.image.load("stage_3/train_images/drunk/idle1.xcf")
trashes = ("is THAT all you can do?","Keep crying","This is too easy","AHHAHAHA","huff","puff")


window_rect = train_window_1.get_rect(topleft = (82,0))
windown_rect_2 = train_window_2.get_rect(topleft = (616,0))
seat_rects = ((200,560),(200,220),(200,100),(200,700),(200,0),
              (500,560),(500,100),(500,220),(500,560),(500,700))

collidable_rects = [window_rect,windown_rect_2]
enemy_dialogue = ("So you are approaching me...","But did you know","IM DRUNK")
enemy_index = 0 

seats = []

for seat_rect in seat_rects:
    seat = pygame.image.load("stage_3/train_images/train_seat.xcf")
    rect = seat.get_rect(topleft = seat_rect)
    seats.append((seat,rect))

for property in wall_properties:
    wall = pygame.draw.rect(bg,(255,255,255),property)
    collidable_rects.append(wall)

#bossfight window
box = pygame.image.load("stage_3/train_images/drunk/box.xcf")
box_wall1 = pygame.draw.rect(bg_,(255,200,200),(150,500,5,250))
box_wall2 = pygame.draw.rect(bg_,(255,200,200),(642,500,5,250))
box_wall3 = pygame.draw.rect(bg_,(255,200,200),(155,500,500,5))
box_wall4 = pygame.draw.rect(bg_,(255,200,200),(155,742,500,5))
box_walls = (box_wall1,box_wall2,box_wall3,box_wall4)


class basic_projectile():
    def __init__(self,name,type):
        self.name = name
        self.type = type
        self.surf = pygame.image.load(f"stage_3/train_images/projectiles/f1{self.name}.xcf")
        self.rect = self.surf.get_rect(topleft = (0,0)) # default rect.
        self.frames = [pygame.image.load(f"stage_3/train_images/projectiles/f1{self.name}.xcf"),pygame.image.load(f"stage_3/train_images/projectiles/f2{self.name}.xcf")]
        self.index = 0
        self.generate()

    def collision(self,rect):
        ''' if player collides with projectile, kill '''
        if self.rect.colliderect(rect):
            return True

    def move(self):
        ''' move the projectile depending on type '''
        if self.type == "up to down":
            self.rect.y += 10
        elif self.type == "down to up":
            self.rect.y -= 10
        elif self.type == "left to right":
            self.rect.x += 10
        elif self.type == "right to left":
            self.rect.x -= 10
        elif self.type == "static":
            return True
    
    def generate(self):
        ''' used to re-generate after death '''
        match self.type:
            case "up to down":
                self.rect = self.surf.get_rect(topleft = (randint(150,605),randint(505,520))) 
            case "down to up":
                self.rect = self.surf.get_rect(topleft = (randint(150,605),randint(695,705)))
            case "left to right":
                self.rect = self.surf.get_rect(topleft = (randint(160,165),randint(505,705)))
            case "right to left":
                self.rect = self.surf.get_rect(topleft = (randint(615,620),randint(505,705)))


class complex_projectile():
    def __init__(self,direction):
        self.direction = direction
        if self.direction in ("up","down"):
            # initial frames are the caution frames.
            self.frames = [
                            pygame.image.load(f"stage_3/train_images/projectiles/box_{self.direction}.xcf"),
                            pygame.image.load(f"stage_3/train_images/projectiles/fist_{self.direction}/water1.xcf"),
                            pygame.image.load(f"stage_3/train_images/projectiles/fist_{self.direction}/water2.xcf"),
                            pygame.image.load(f"stage_3/train_images/projectiles/fist_{self.direction}/water3.xcf")]
        elif self.direction in ("left","right"):
            self.frames = [pygame.image.load(f"stage_3/train_images/projectiles/box_{self.direction}.xcf")] 
            for n in range(1,6): # start at one end at 6
                self.frames.append(pygame.image.load(f"stage_3/train_images/projectiles/fist_{self.direction}/fist{n}.xcf"))
        self.index = -1
        self.increasing = False
        self.collision_rect = None

    def animate(self):
        ''' animates the obj '''
        #everytime this is accesed, increment index, if max then decrease.
        global box 

        if self.index == -1 and not(self.increasing):
            self.increasing = True 

        if self.increasing:
            self.index += 1
            if self.index == len(self.frames):
                self.increasing = False 
        
        if not(self.increasing) and self.index != 0:
            self.index -= 1

        # print(self.index,self.increasing,self.index == len(self.frames),len(self.frames))
        box = self.frames[self.index]
        self.collision() # everytime animate, a new collision rect has to be drawn

    def collision(self):
        ''' draws a new collision rect each pass '''

        # 498 px wide
        # 248 px high

        left = (0,150,150,150,150,150) # y = 500
        right = (0,565,465,360,300,257) # y = 500
        down = (0,713,663,613) # x = 150
        up = (0,500,500,500) # x = 150
        up_r = (0,35,85,135)
        left_r = (0,46,103,238,293,390)
        match self.direction:
            case "up":
                self.collision_rect = pygame.draw.rect(bg_2,(100,255,50),(150,up[self.index],498,up_r[self.index]))
            case "down":
                self.collision_rect = pygame.draw.rect(bg_2,(100,255,50),(150,down[self.index],498,up_r[self.index]))
            case "left":
                self.collision_rect = pygame.draw.rect(bg_2,(100,255,50),(left[self.index],500,left_r[self.index],248))
            case "right":
                self.collision_rect = pygame.draw.rect(bg_2,(100,255,50),(right[self.index],500,left_r[self.index],248))
        return self.collision_rect
        

#size = choice(((20,50),(30,50),(40,50),(50,50))) #random size
bottle_names = ("bottle_1","bottle_2","bottle_3")

bottles = []
attack_direction = choice(("left","right","down","up"))

# for bottle in range(10+randint(1,5)): #random amount of bottles
#     bottle = basic_projectile(choice(bottle_names),"up to down")
#     bottles.append(bottle) #appends an instance of projectile with a random name.

def generate_bottle(n,type):
    ''' 
    appends bottle n amount of times with the same type 
    where type refers to type of attack
    '''
    bottle = basic_projectile(choice(bottle_names),type)
    bottle.generate()
    for _ in range(n):
        bottles.append(bottle)

attack_types = ("up to down","down to up","left to right","right to left")

def generate_caution(type):
    ''' 
    makes the arrow where the projectiles will go towards
    generates a tuple: img, location
    '''
    global box 
    #print(type[:9],type[9:])
    if type == "up to down":
        rect = (377,520)
    elif type == "down to up":
        rect = (377,680)
    elif type == "left to right":
        rect = (165,605)
    elif type == "right to left":
        rect = (590,605)
    elif type[:9] == "overwhelm":
        # box = pygame.image.load(f"stage_3/train_images/projectiles/box_{type[9:]}.xcf")
        return None 
        

    box = pygame.image.load("stage_3/train_images/drunk/box.xcf")
    return (pygame.image.load(f"stage_3/train_images/projectiles/{type} arrow.xcf"),rect)

# end text
end_dialogue = (
    "...","How do you feel?","all those people you've annoyed","good?","happy?","relieved?",
    "at school","at home","...","you've won but at what cost?","...","now go","there's no reason to be here",
    "goodbye")
end_index = 0
end = False