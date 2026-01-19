'''
A module to store all essential function code
'''
__authour__ = "Mike Mission"
__status__ = "ALPHA"
__license__ = "MIT"

import pygame
pygame.init()

font = pygame.font.SysFont('Helvetica', 20)
noise_block = pygame.image.load("core_tools/minigame_sprites/noise_meter/noise_block.xcf")
noise_text = font.render("Noise Meter",True,(255,0,0),(0,0,0))
    
def change_sprite(gender='male') -> dict:
    # print(gender)
    ''' A function that returns a dict full of player sprites'''

    if gender == "female": # will be true when menu says!
        #player sprites
        player_idle = pygame.image.load("core_tools/character_anim/female/idle_player.xcf")

        player_walk_up = pygame.image.load("core_tools/character_anim/female/up_player.xcf")
        player_walk_down = pygame.image.load("core_tools/character_anim/female/down_player.xcf")

        #player animations (left and right)

        #left
        player_frame1_L = pygame.image.load("core_tools/character_anim/female/left_player.xcf")
        player_frame2_L = pygame.image.load("core_tools/character_anim/female/left_player2.xcf")
        player_left_frames = [player_frame1_L,player_frame2_L]
        player_left_frame_index = 0
        player_surf = player_left_frames[player_left_frame_index]

        #right
        player_frame1_R = pygame.image.load("core_tools/character_anim/female/right_player.xcf")
        player_frame2_R = pygame.image.load("core_tools/character_anim/female/right_player2.xcf")
        player_right_frames = [player_frame1_R,player_frame2_R]
        player_right_frame_index = 0
        player_surf = player_right_frames[player_right_frame_index]

    elif gender == "male":
        #player sprites
        player_idle = pygame.image.load("core_tools/character_anim/male/idle_player.xcf")

        player_walk_up = pygame.image.load("core_tools/character_anim/male/up_player.xcf")
        player_walk_down = pygame.image.load("core_tools/character_anim/male/down_player.xcf")

        #player animations (left and right)

        #left
        player_frame1_L = pygame.image.load("core_tools/character_anim/male/left_player.xcf")
        player_frame2_L = pygame.image.load("core_tools/character_anim/male/left_player2.xcf")
        player_left_frames = [player_frame1_L,player_frame2_L]
        player_left_frame_index = 0
        player_surf = player_left_frames[player_left_frame_index]

        #right
        player_frame1_R = pygame.image.load("core_tools/character_anim/male/right_player.xcf")
        player_frame2_R = pygame.image.load("core_tools/character_anim/male/right_player2.xcf")
        player_right_frames = [player_frame1_R,player_frame2_R]
        player_right_frame_index = 0
        player_surf = player_right_frames[player_right_frame_index]

    return {"player_idle":player_idle,
            "player_walk_down":player_walk_down,
            "player_walk_up":player_walk_up,
            "player_left_frames":player_left_frames,
            "player_left_frame_index":player_left_frame_index,
            "player_right_frames":player_right_frames,
            "player_right_frame_index":player_right_frame_index,
            "player_surf":player_surf
            }

def play_player_animation(direction,asset_lib) -> pygame.surface:
    '''
    Function to play the player's animation if they are moving left or right
    Inputs = direction,asset_lib
    Output = player_surf
    '''
    if direction == "left":
        '''switch between both frames'''
        if asset_lib.player_left_frame_index == 0:asset_lib.player_left_frame_index = 1
        else: asset_lib.player_left_frame_index = 0

        return asset_lib.player_left_frames[asset_lib.player_left_frame_index]

    elif direction == "right":
        '''switch between both frames'''
        if asset_lib.player_right_frame_index == 0:asset_lib.player_right_frame_index = 1
        else: asset_lib.player_right_frame_index = 0

        return asset_lib.player_right_frames[asset_lib.player_right_frame_index]
    elif direction == "up":
        return asset_lib.player_walk_up
    elif direction == "down":
        return asset_lib.player_walk_down
    elif direction == "idle":
        return asset_lib.player_idle   
    
def collision_with_static(rect1,rect2) -> bool:
    '''
    Detects collision and disables movement accordingly
    '''
    keys = pygame.key.get_pressed()
    #print(abs(rect2.bottom - rect1.top))

    #top collision
    if abs(rect2.top - rect1.bottom) <= 5:
        if keys[pygame.K_s]:
            return False
        elif keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_d]:
            return True 
    #bottom collision
    elif abs(rect2.bottom - rect1.top) <= 5:
        if keys[pygame.K_w]:
            return False
        elif keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            return True 
    #right collision
    elif abs(rect2.left - rect1.right) <= 5:
        if keys[pygame.K_d]:
            return False
        elif keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_w]:
            return True 
    #left collision
    elif abs(rect2.right - rect1.left) <= 5:
        if keys[pygame.K_a]:
            return False
        elif keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_d]:
            return True 
    else:return True   

def time_determiner(secs,mins,font) -> pygame.font:
    ''' A function that takes values of secs and mins to traditionaly display them '''
    if len(str(secs)) == 1:
        secs = str("0") + str(secs)
        return font.render("{}:{}".format(mins,secs),True,(255,0,0),(0,0,0))
    else:
        return font.render("{}:{}".format(mins,secs),True,(255,0,0),(0,0,0))

noise = 0
def noise_meter(event,difficulty,factor = 0) -> int:
    '''

    function to display a meter that determines if the player is moving too much.
    active when enemies spawn.

    '''
    #max noise is 100 
    #factor is to increase main.difficulty (when the player has not detuned the bass and guitar)

    #draw the meter.

    global noise,noise_block
    
    # print(noise)
    noise_block = pygame.transform.scale(noise_block,(10+noise,30))

    if difficulty == 2:factor = 0.3
    elif difficulty == 3:factor = 0.5

    if event.type == pygame.KEYDOWN:noise += 15
    elif noise < 0:noise = 0 + factor
    elif noise < 50:noise -= 0.1 - factor
    elif noise > 50:noise -= 3 - factor
    elif noise > 100:noise -= 30 - factor

    
    #difficulty is at least 1 always

    if noise > 100: # top of the bar
        return 4 #returns this value to difficulty, so inc entity.difficulty
    elif noise > 50: # middle of bar
        return 3
    elif noise > 25: # bottom of bar
        return 2
    else:return 1   