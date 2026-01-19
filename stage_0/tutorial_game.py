#https://www.youtube.com/watch?v=AY9MnQ4x3zk&
#tutorials 1&3
__author__ = "Mike Mission"
__status__ = "development"
__license__ = "MIT"

'''
file imported from movement versions, will serve as a tutorial now.
condensing code into more useful forms
'''
finish = False
npc_state = "idle"
x = 50
y = 50

import pygame
import stage_0.tutorial_image_lib as asset_lib
from random import randint

pygame.init()#initialise pygame

#timers
left_obstacle_rect_list = []
right_obstacle_rect_list = []
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,3500)#time in milliseconds

enemy_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animation_timer,100)

tutorial_text_timer = pygame.USEREVENT + 3
pygame.time.set_timer(tutorial_text_timer,1000)

def obstacle_movement(win,obstacle_list,direction):
    '''
        Using the event timer, allows enemies to move
        and displays them
    '''
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if direction == "left":
                obstacle_rect.x -= 1
            elif direction == "right":
                obstacle_rect.x += 1
            asset_lib.enemy_surf = pygame.transform.scale(asset_lib.enemy_surf,(50,50))
            win.blit(asset_lib.enemy_surf,obstacle_rect)
        if direction == "left":
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -1]
        elif direction == "right":
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > 1]
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

def tutorial(win,run,game_active,**kwargs):
    '''
        Makes a sprite move via 'wasd'
        parameters:win,width,height,run,kwargs
        kwargs:{vel:1,x:1,y:1}
        output:None

        Displays Enemies,player,npc
    '''    
    global x
    global y
    global npc_state
    global left_obstacle_rect_list,right_obstacle_rect_list
    global finish
    #default values
    vel = 2.5
    x = 50
    y = 50
    npc_got_obj = False
    got_obj = False
    left_obstacle_rect_list.clear()
    right_obstacle_rect_list.clear()
    finish = False
    npc_state = "idle"
    asset_lib.npc_state = npc_state
    asset_lib.upd_state()
    game_active = True
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
    quitting = False

    while run == True:
        pygame.time.delay(2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
                game_active = False

            if game_active:
                if event.type == obstacle_timer:
                    left_obstacle_rect_list.append(asset_lib.enemy_surf.get_rect(midbottom = (randint(600,700),(randint(500,700)))))
                    right_obstacle_rect_list.append(asset_lib.enemy_surf.get_rect(midbottom = (500,(randint(100,400)))))
                
                if event.type == enemy_animation_timer:
                    if asset_lib.enemy_index == 0: asset_lib.enemy_index = 1
                    else: asset_lib.enemy_index = 0
                    
                    asset_lib.enemy_surf = asset_lib.enemy_frames[asset_lib.enemy_index]
                
                if event.type == tutorial_text_timer:
                    if asset_lib.text_index == 0:asset_lib.text_index = 1
                    else: asset_lib.text_index = 0
            
        #player_rect has to be initialised here as it is constantly adjusted
        if game_active:

            player_rect = asset_lib.player_surf.get_rect(midbottom = (x,y))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a] and x > vel:x -= vel
            if keys[pygame.K_d] and x < 775 - vel:x += vel
            if keys[pygame.K_w] and y > vel :y -= vel
            if keys[pygame.K_s] and y < 775 - vel :y += vel

            #print(player_rect.midbottom)#get player's midbottom position

            #load background - since background has to be updated for each move the player does
            win.blit(asset_lib.background,(0,0))

            #load the text
            if not(npc_got_obj):
                win.blit(asset_lib.tutorial_texts[asset_lib.text_index],(600,50))
        
            win.blit(asset_lib.bush_surf,asset_lib.bush_rect)
            win.blit(asset_lib.bush2_surf,asset_lib.bush2_rect)
                  

            #load player
            win.blit(asset_lib.player_surf,player_rect)

            #load npc
            if npc_state == "idle":
                win.blit(asset_lib.baby_surf,asset_lib.baby_rect)
                win.blit(asset_lib.task_baby,(70, 720))

            #if player gets the mic
            if got_obj and player_rect.colliderect(asset_lib.baby_rect) != True and npc_got_obj == False:win.blit(asset_lib.microphone_surf,(-100,0))
            elif got_obj == False and player_rect.colliderect(asset_lib.baby_rect) == False:win.blit(asset_lib.microphone_surf,asset_lib.microphone_rect)

            #when player has the mic
            if player_rect.colliderect(asset_lib.microphone_rect) and got_obj == False and npc_got_obj == False:got_obj = True

            #when the baby has the mic
            if player_rect.colliderect(asset_lib.baby_rect) and got_obj == True and npc_got_obj == False:
                win.blit(asset_lib.microphone_surf,(50, 700))
                npc_got_obj = True
            
            if npc_got_obj == True:
                #People rushing out of the bush event
                #obstacles
                left_obstacle_rect_list = obstacle_movement(win,left_obstacle_rect_list,"left")
                right_obstacle_rect_list = obstacle_movement(win,right_obstacle_rect_list,"right")
                
                #collision
                npc_got_obj = collisions(player_rect,left_obstacle_rect_list)
                game_active = collisions(player_rect,left_obstacle_rect_list) 

                npc_got_obj = collisions(player_rect,right_obstacle_rect_list)
                game_active = collisions(player_rect,right_obstacle_rect_list)

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
        
        
        elif quitting:
            print("hit")
            game_active = False
            win.fill("black")
            win.blit((asset_lib.Helvetica_font.render("Are you sure? (y/n)",True,(255,255,255))),(200,370))
            pygame.display.update()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_y]:
                finish = False
                run = False
                return True
                
                
            elif keys[pygame.K_n]:
                run = True
                game_active = True


        elif game_active == False and npc_got_obj == False:

            win.fill("black")
            win.blit(asset_lib.x_game_text,(250, 370))#center
            win.blit(asset_lib.deathmessage,(250,500))
            win.blit(asset_lib.restart_q,(250,600))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_r]:
                #reset the game
                npc_got_obj = False
                got_obj = False
                left_obstacle_rect_list.clear()
                right_obstacle_rect_list.clear()
                player_rect.midbottom = (50,50)
                finish = False
                npc_state = "idle"
                x = 50
                y = 50
                asset_lib.npc_state = npc_state
                asset_lib.upd_state()
                game_active = True
                
        elif game_active == False and finish == True:
            win.fill("black")
            win.blit(asset_lib.finish_tutorial_txt,(200,370))
            win.blit(asset_lib.finish_q,(200,300))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_r]: 
                run = False
                game_active = False
                return True

        if not(quitting):
            pygame.display.update()
            clock.tick(60)


