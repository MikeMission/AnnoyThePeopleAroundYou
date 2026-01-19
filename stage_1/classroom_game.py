__author__ = 'Mike Mission'
__status__ = "ALPHA"
__license__ = "MIT"

import pygame
import core_tools.tools as tools
from core_tools.tools import play_player_animation,collision_with_static,time_determiner,noise_meter
from core_tools.minigames import bar_minigame,spam_minigame
import stage_1.classroom_image_loader as asset_lib
from stage_1.classroom_image_loader import (
    enemies,
    instruments,
    electric_guitar,
    bass_guitar,
    drum_kit,
    mic,
    cat
)

pygame.init()

player_direction = "idle"

actual_timer = pygame.USEREVENT + 1 
pygame.time.set_timer(actual_timer, 1000)

enemy_animate_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animate_timer, 150)

cat_animate_timer = pygame.USEREVENT + 3
pygame.time.set_timer(cat_animate_timer, 1000)

player_animate_timer = pygame.USEREVENT + 4
pygame.time.set_timer(player_animate_timer, 150)

def game(win,run,game_active,**kwargs):
    '''
        ===Classroom game===
        interactive objects:
        - guitar
        - drumkit
        - bass guitar
        - microphone
        
        4 enemies belonging to these instruments, appear when all tempered

        minigames for instruments:
        - bar minigame (guitar, bassguitar)
        - spam minigame (drumkit, microphone)
    '''
    global player_direction
    global secs
    #default values
    vel = 2.5
    x = 170
    y = 50
    clock = pygame.time.Clock()
    state = 1
    event = None
    movement = True 
    died = False
    player_died_to = ''
    difficulty = 1
    secs,mins = 0,0
    finish = False
    noise = 0
    player_surf = asset_lib.player_idle 
    timer_text = asset_lib.time_font.render("00:00",True,(255,0,0),(0,0,0))
    #optional kwargs
    if 'vel' in kwargs:
        vel = kwargs['vel']
    #main loop
    while run:
        pygame.time.delay(2)
        #game_active is re-assigned to true after the player has read the text in task_text
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            #displays the text for the user to read
            if state in (1,2):
                game_active = task_text(win,event,state)
                
            #gets event so can set direction for player animation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:player_direction = "left"
                elif event.key == pygame.K_d:player_direction = "right"
                elif event.key == pygame.K_w:player_direction = "up"
                elif event.key == pygame.K_s:player_direction = "down"
                
            elif event.type == pygame.KEYUP:
                player_direction = "idle"
                player_surf = asset_lib.player_idle

            if state == 1:
                if event.type == actual_timer:
                    secs += 1

                if secs == 60:
                    mins += 1 
                    secs = 0 #resets seconds

                timer_text = time_determiner(secs,mins,asset_lib.time_font)

            elif state == 2:
                for entity in enemies:
                    if entity.rect.colliderect(player_rect):
                        player_died_to = entity
                        game_active = False 
                        died = True
                    #inc entity difficulty according to noise_meter algorithim
                    if event.type == pygame.KEYDOWN:
                        noise += 15
                    entity.difficulty = noise_meter(event,difficulty)

                #every 300ms the enemy will animate!!!!!!!!!!!
                if event.type == enemy_animate_timer:
                    for entity in enemies:
                        if entity.direction == "left":
                            if (entity.gpli == 0):entity.gpli = 1
                            else:entity.gpli = 0
                            entity.frame = entity.left_frames[entity.gpli]
                            
                        elif entity.direction == "right":
                            if (entity.gpri == 0):entity.gpri = 1
                            else:entity.gpri = 0
                            entity.frame = entity.right_frames[entity.gpri]
                        elif entity.direction == "idle":
                            entity.frame = entity.idle_frame
                #every second
                if event.type == cat_animate_timer:
                    if cat.gpri + 1 > len(cat.right_frames):
                            cat.gpri = -1 
                    else:
                        cat.frame = cat.right_frames[cat.gpri]
                        cat.gpri += 1


            elif state == 3:
                finish = task_text(win,event,state)

            #animate the player
            if event.type == player_animate_timer:
                player_surf = play_player_animation(player_direction,asset_lib)


        #main loop
        if game_active:
            if state == 1:

                win.blit(asset_lib.bg,(0,0))

                player_rect = player_surf.get_rect(midbottom = (x,y))

                keys = pygame.key.get_pressed()
                for rect in asset_lib.collidable_rects:
                    if player_rect.colliderect(rect):
                        movement = collision_with_static(player_rect,rect)

                if movement:
                    if keys[pygame.K_a] and x > vel + 30:
                        x -= vel
                    elif keys[pygame.K_d] and x < 775 - vel - 10:
                        x += vel
                    elif keys[pygame.K_w] and y > vel :
                        y -= vel
                    elif keys[pygame.K_s] and y < 775 - vel :
                        y += vel
                    
                win.blit(player_surf,player_rect)
                win.blit(timer_text,(650,700))
                win.blit(asset_lib.Helvetica_font.render("You have 45s to detune all these instruments",True,(255,0,0),(0,0,0)),(320,700))
                #print(player_direction)
                #print(player_rect.x,player_rect.y)

                detune_instrument(win,player_rect,event = event)
                
                #due_puzzle - list containing the instruments due for a puzzle
                #if due_puzzle has been tempered with then it will trigger the last phase of the stage
                if (
                    (due_puzzle in ([False,False,True,True],[False,True,True,True],[True,False,True,True],[True,True,True,True]))
                    or (secs == 45)
                    ):
                    for won in due_puzzle:
                        if won == False:
                            difficulty += 1
                    state = 2
                
            elif state == 2:
                # game_active = task_text(win,event,state=2)
                player_rect = player_surf.get_rect(midbottom = (x,y))
                end_rect = pygame.draw.rect(asset_lib.bg,(0,255,0),(101,0,149,10))
                win.blit(asset_lib.bg,(0,0))
                win.blit(player_surf,player_rect)


                for instrument in instruments:
                    win.blit(instrument.surf,instrument.rect)
                
                win.blit(tools.noise_text,(100,620))
                win.blit(tools.noise_block,(100,650))

                keys = pygame.key.get_pressed()
                for rect in asset_lib.collidable_rects:
                    if player_rect.colliderect(rect):
                        movement = collision_with_static(player_rect,rect)

                if movement:
                    if keys[pygame.K_a] and x > vel + 30:
                        x -= vel
                    if keys[pygame.K_d] and x < 775 - vel - 10:
                        x += vel
                    if keys[pygame.K_w] and y > vel :
                        y -= vel
                    if keys[pygame.K_s] and y < 775 - vel :
                        y += vel

                #spawn enemies and finish gate
                for entity in enemies:
                    entity.move()
                    win.blit(entity.frame,entity.rect)
                win.blit(cat.frame,cat.rect)

                if player_rect.colliderect(end_rect):
                    game_active = False 
                
        elif game_active == False and died == True:
            win.fill("black")
            # print("died")
            win.blit(player_died_to.death_msg(),(300,400))
            win.blit(asset_lib.Helvetica_font_small.render("'r to restart'",True,(255,255,255)),(300,420))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                x = 400
                y = 690
                movement = True
                died = False
                game_active = True
                died = False 


        elif game_active == False:
            state = 3 
            if finish == True:
                return secs 
            
        pygame.display.update()
        clock.tick(60)

'''
Bar minigame vars
'''
direction = "left"  
def detune_instrument(win,player_rect,**kwargs) -> None:
    '''
    Detects if the player is touching an instrument and what one
    Input: win,player_rect
    Output: str(instrument)
    '''
    global due_puzzle

    if "event" in kwargs:
        event = kwargs["event"]

    #display instruments
    
    for instrument in instruments:
        win.blit(instrument.surf,instrument.rect)

        if player_rect.colliderect(instrument.rect):
            if instrument.minigame == "spam":
                instrument.won = spam_minigame(win,instrument,asset_lib,event)

                if instrument.won:
                    instrument.surf = instrument.complete_surf
                    
            elif instrument.minigame == "bar":
                instrument.won = bar_minigame(win,instrument,asset_lib)

                if instrument.won:
                    instrument.surf = instrument.complete_surf
                
                elif not(instrument.won) and (instrument.won):
                    failed_text = asset_lib.Helvetica_font.render("failed to detune...",True,(255,0,0))
                    win.blit(failed_text,instrument.rect)
            
    due_puzzle = [electric_guitar.won,bass_guitar.won,drum_kit.won,mic.won]
def task_text(win,event,state) -> bool:
    '''
    Displays text for the task
    '''    
    global secs 
    win.fill("black")
    
    if state == 1:

        if (asset_lib.st1_line + 1) > len(asset_lib.st_1_txt_list):return True 

        text = asset_lib.Helvetica_font.render(asset_lib.st_1_txt_list[asset_lib.st1_line],True, (255,255,255))
        confirmation_text = asset_lib.Helvetica_font_small.render("'space to continue'",True,(255,255,255))
        
        win.blit(text,(160,440))
        win.blit(confirmation_text,(160,500))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                asset_lib.st1_line += 1
    
    if state == 2:

        if (asset_lib.st2_line + 1) > len(asset_lib.st_2_txt_list):return True 

        enemy_dialougue = asset_lib.Helvetica_font.render(asset_lib.st_2_txt_list[asset_lib.st2_line],True,(255,0,0))
        confirmation_text = asset_lib.Helvetica_font_small.render("'space to continue'",True,(255,255,255))
        win.blit(enemy_dialougue,(160,440))
        win.blit(confirmation_text,(160,500))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                asset_lib.st2_line += 1

    
    if state == 3:

        if (asset_lib.st3_line + 1) > len(asset_lib.st_3_txt_list):return True

        win.blit(asset_lib.Helvetica_font.render(asset_lib.st_3_txt_list[asset_lib.st3_line],True,(255,255,255)),(300,400))
        win.blit(asset_lib.Helvetica_font_small.render("'space to continue'",True,(255,255,255)),(300,450))
        win.blit(asset_lib.Helvetica_font_small.render(f"your time: {secs} seconds, best time: null seconds",True,(255,0,0)),(300,500))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                asset_lib.st3_line += 1
due_puzzle = [electric_guitar.won,bass_guitar.won,drum_kit.won,mic.won]