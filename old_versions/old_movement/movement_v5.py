#https://www.youtube.com/watch?v=i6xMBig-pP4&
#tutorials 1&3
__author__ = "Mike Mission"
__version__ = "5"

'''
Trying to use collisions and output things
'''
finish = False
npc_state = "idle"
x = 50
y = 50

import pygame
import asset_lib_v5 as asset_lib
from random import randint

pygame.init()#initialise pygame

#timers
obstacle_rect_list = []
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)#time in milliseconds

enemy_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animation_timer,100)


# def display_lives():
'''
    Lives aren't implemented in this version yet.
'''
#     current_time = pygame.time.get_ticks()
#     print(current_time)

def obstacle_movement(win,obstacle_list):
    '''
        Using the event timer, allows enemies to move
        and displays them
    '''
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 10
            asset_lib.enemy_surf = pygame.transform.scale(asset_lib.enemy_surf,(50,50))
            win.blit(asset_lib.enemy_surf,obstacle_rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -1]
        #only copies items from the list if the condition that the x attribute is > -1

        return obstacle_list
    else:return []

def collisions(player,obstacles):
    '''
        Checks if player has collided with an obstacle
    '''
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): 
                asset_lib.death_by("Person")
                return False 

    return True


def movement(win,run,game_active,**kwargs):
    global x
    global y
    global npc_state
    global obstacle_rect_list

    '''
        Makes a pixel move via 'wasd'
        parameters:win,width,height,run,kwargs
        kwargs:{vel:1,x:1,y:1}
        output:None

        Displays Enemies,player,npc
    '''    
    #default values
    vel = 7.5

    x = 50
    y = 50
    #^ future reference for hitboxes, but will not be used for literal size (sprite usage)

    if "vel" in kwargs:vel = kwargs["vel"]
    elif "x" in kwargs:x = kwargs["x"]
    elif "y" in kwargs:y = kwargs["y"]
    #Default values for vel,x,y, for change:look^^^
    #function doesn't work properly if vars aren't definied in it
    
    clock = pygame.time.Clock()

    player_rect = asset_lib.player_surf.get_rect(midbottom = (x,y))

    
    got_obj = False #player spawns with no objects
    npc_got_obj = False #npcs spawn with no objects

    while run == True:
        pygame.time.delay(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:run = False

        if game_active:
            if event.type == obstacle_timer:
                obstacle_rect_list.append(asset_lib.enemy_surf.get_rect(midbottom = (randint(600,700),(randint(500,700)))))
            
            if event.type == enemy_animation_timer:
                if asset_lib.enemy_index == 0: asset_lib.enemy_index = 1
                else: asset_lib.enemy_index = 0
                
                asset_lib.enemy_surf = asset_lib.enemy_frames[asset_lib.enemy_index]
        
        #player_rect has to be initialised here as it is constantly adjusted
        if game_active:

            #display_lives()

            player_rect = asset_lib.player_surf.get_rect(midbottom = (x,y))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a] and x > vel:x -= vel
            if keys[pygame.K_d] and x < 775 - vel:x += vel
            if keys[pygame.K_w] and y > vel :y -= vel
            if keys[pygame.K_s] and y < 775 - vel :y += vel

            print(player_rect.midbottom)#get player's midbottom position

            #load background - since background has to be updated for each move the player does
            win.blit(asset_lib.background,(0,0))
            win.blit(asset_lib.bush_surf,asset_lib.bush_rect)
            win.blit(asset_lib.bush2_surf,asset_lib.bush2_rect)
                  

            #load player
            win.blit(asset_lib.player_surf,player_rect)

            #load npc
            if npc_state == "idle":
                win.blit(asset_lib.baby_surf,asset_lib.baby_rect)
                win.blit(asset_lib.task_baby,(70, 720))

            #if player gets the mic
            if got_obj and player_rect.colliderect(asset_lib.baby_rect) != True and npc_got_obj == False:win.blit(asset_lib.microphone_surf,(0,0))
            elif got_obj == False and player_rect.colliderect(asset_lib.baby_rect) == False:win.blit(asset_lib.microphone_surf,asset_lib.microphone_rect)

            #when player has the mic
            if player_rect.colliderect(asset_lib.microphone_rect) and got_obj == False and npc_got_obj == False:got_obj = True

            #when the baby has the mic
            if player_rect.colliderect(asset_lib.baby_rect) and got_obj == True and npc_got_obj == False:
                win.blit(asset_lib.microphone_surf,(50, 700))
                npc_got_obj = True
            
            if npc_got_obj == True:
                #obstacles
                obstacle_rect_list = obstacle_movement(win,obstacle_rect_list)
                #collision
                game_active = collisions(player_rect,obstacle_rect_list)

                win.blit(asset_lib.microphone_surf,(50, 700))
                asset_lib.npc_state = "crying"
                asset_lib.upd_state()
                win.blit(asset_lib.task_baby,(70, 720))
                win.blit(asset_lib.baby_surf,asset_lib.baby_rect)
                win.blit(asset_lib.gate_surf,asset_lib.gate_rect)
                
                if player_rect.colliderect(asset_lib.gate_rect):
                    finish = True
                    game_active = False



            #if player collides with bush
            if player_rect.colliderect(asset_lib.bush_rect) or player_rect.colliderect(asset_lib.bush2_rect):
                asset_lib.death_by("Bush")
                npc_got_obj = False
                game_active = False
            
            
            

        elif game_active == False and npc_got_obj == False:
            obstacle_rect_list.clear()#deletes obstacles
            player_rect.midbottom = (50,50)#resets position
            win.fill("Black")
            win.blit(asset_lib.x_game_text,(250, 370))#center
            win.blit(asset_lib.deathmessage,(250,500))
        elif game_active == False and finish == True:
            win.fill("Black")
            win.blit(asset_lib.finish_tutorial_txt,(200,370))

        pygame.display.update()
        clock.tick(60)


# """ 
# def prototype_test():
    
#     pygame.init()

#     win = pygame.display.set_mode((800,800))
#     pygame.display.set_caption("Movement Prototype")

#     run = True
    
#     movement(win,run)

#     pygame.quit()

