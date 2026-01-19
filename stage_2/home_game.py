__authour__ = "Mike Mission"
__status__ = "ALPHA"
__license__ = "MIT"
'''
prototype of second stage 'home'
'''
import pygame
import stage_2.home_image_lib as asset_lib
import core_tools.tools as tools
from core_tools.tools import collision_with_static,play_player_animation,time_determiner,noise_meter
from core_tools.minigames import spam_minigame,bar_minigame,click_drag_minigame,click_minigame
from stage_2.home_image_lib import interactive_objects,enemies


pygame.init()

player_direction = "idle"

actual_timer = pygame.USEREVENT + 2
pygame.time.set_timer(actual_timer, 1000) #every second

player_animation_timer = pygame.USEREVENT + 4 
pygame.time.set_timer(player_animation_timer,150)

enemy_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(enemy_animation_timer,150)

def game(win,run,game_active,**kwargs):
    '''
    --Home game--
    contains multiple interactive objects:
    - bin
    - recycle bin
    - alarm clock
    - fridge
    - toys
    All with different mini tasks to do (different from minigames like previously)
    '''
    global player_direction
    global finish
    clock = pygame.time.Clock()
    x,y = 105,115
    vel = 2.5
    movement = True
    interacted = [False,False]
    state = 1
    finish = False
    died_to = ""
    tools.noise = mins = secs = 0 #💅
    difficulty = 2
    timer_text = asset_lib.time_font.render("00:00",True,(255,0,0),(0,0,0))

    if "vel" in kwargs:vel = kwargs["vel"]
    
    player_surf = asset_lib.player_idle
    while run:
        pygame.time.delay(2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:player_direction = "left"
                elif event.key == pygame.K_d:player_direction = "right"
                elif event.key == pygame.K_w:player_direction = "up"
                elif event.key == pygame.K_s:player_direction = "down"

            elif event.type == pygame.KEYUP:
                player_direction = "idle"
                player_surf = asset_lib.player_idle

            #play player_animation every 150 ms
            if event.type == player_animation_timer:
                player_surf = play_player_animation(player_direction,asset_lib)

            if event.type == enemy_animation_timer:
                if all(interacted) or interacted == [True,True,False,True,True]: #only bar minigame is failable...
                    for enemy in enemies:
                        enemy.animate()

            #state exclusive events
            if state == 2:
                game_active = state_text(win,event,state,secs)
                difficulty = noise_meter(event,difficulty)
            elif state == 1:
                if event.type == actual_timer:
                    secs += 1

                if secs == 60:
                    mins += 1 
                    secs = 0 #resets seconds

                timer_text = (time_determiner(secs,mins,asset_lib.time_font))
            elif state == 3:
                state_text(win,event,state,secs)

        
        #game loop
        if game_active:

            win.blit(asset_lib.bg,(0,0))

            keys = pygame.key.get_pressed()

            player_rect = player_surf.get_rect(midbottom = (x,y))

            #check if player has collided with any of these rectangles!!!
            for rect in asset_lib.collidable_rects:
                if player_rect.colliderect(rect):
                    movement = collision_with_static(player_rect,rect)
            #loop through these rects

            if movement:
                if keys[pygame.K_a]:
                    x -= vel
                elif keys[pygame.K_d]:
                    x += vel
                elif keys[pygame.K_w]:
                    y -= vel
                elif keys[pygame.K_s]:
                    y += vel

            win.blit(player_surf,player_rect)

            if state == 1:
                win.blit(timer_text,(650,700))
                win.blit(asset_lib.Helvetica_font.render("you have 30s to Interact with objects",True,(255,0,0),(0,0,0)),(250,700))
                #mouthwatering polymorphism 🤤
                for i_object in interactive_objects:

                    if player_rect.colliderect(i_object.rect):
                        win.blit(i_object.text,i_object.interaction_text())
                        if keys[pygame.K_e]:
                            i_object.interaction_tab = True 

                    if i_object.interaction_tab:
                        i_object.text = asset_lib.interact_font.render("'interacted'",True,(0,0,0))
                        if i_object.minigame == "spam":
                            i_object.won = spam_minigame(win,i_object,asset_lib,event)
                        elif i_object.minigame == "bar":
                            i_object.won = bar_minigame(win,i_object,asset_lib)
                        elif i_object.minigame == "click&drag":
                            i_object.won = click_drag_minigame(win,asset_lib)
                        elif i_object.minigame == "click":
                            i_object.won = click_minigame(win,asset_lib)

                        if i_object.won:
                            i_object.interaction_tab = False
        
                    if i_object.disabled is not True:
                        win.blit(i_object.surf,i_object.rect)
                        #bin is not an interactable object 🤐
                        win.blit(asset_lib.bin.surf,asset_lib.bin.rect)
                        
                #display enemies (idle for now)
                for enemy in enemies:
                        if asset_lib.fridge.disabled is not True:
                            win.blit(enemy.surf,enemy.rect)
                
                        if player_rect.colliderect(enemy.rect):
                            enemy.talk(win)
                        else:
                            enemy.idle()
                            
                interacted = [x.won for x in interactive_objects]
                
                if all(interacted) or interacted == [True,True,False,True,True]: #only bar minigame is failable...
                    state = 2 
                elif secs == 30:
                    state = 2 

            
            if state == 2:
                win.blit(asset_lib.bg,(0,0))
                win.blit(player_surf,player_rect)
                win.blit(tools.noise_text,(100,620))
                win.blit(tools.noise_block,(100,650))

                for i_object in interactive_objects:
                    win.blit(i_object.surf,i_object.rect)

                for enemy in enemies:
                    win.blit(enemy.surf,enemy.rect)
                    enemy.move(difficulty)
                    if player_rect.colliderect(enemy.rect):
                        finish = False 
                        game_active = False
                        died_to = enemy

                end_rect = pygame.draw.rect(asset_lib.bg,(120,100,255),(0,120,10,10))
                if player_rect.colliderect(end_rect):
                    state = 3
                    game_active = False

        if game_active is False and state == 2:
            win.fill("black")
            win.blit(asset_lib.Helvetica_font.render(f"you died to {died_to.name}",True,(255,0,0),(0,0,0)),(300,300))
            win.blit(asset_lib.interact_font.render(f"'press r to restart'",True,(255,255,255)),(300,400))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_r]:
                x,y = 455,133
                state = 2
                movement = True
                game_active = True 
        # pos = pygame.mouse.get_pos()
        # print(pos)
        if game_active is False and state == 3 and finish:
            return secs 


        pygame.display.update()
        clock.tick(60)

def state_text(win,event,state,secs):
    global finish
    ''' displays text depending on the state '''
    if state == 3:
        
        win.fill("black")
        win.blit(asset_lib.Helvetica_font.render("stage 2 complete",True,(255,0,0),(0,0,0)),(300,400))
        win.blit(asset_lib.interact_font.render("'space to continue'",True,(255,255,255),(0,0,0)),(300,450))
        win.blit(asset_lib.interact_font.render(f"your time: {secs} seconds, best time: null seconds",True,(255,0,0)),(200,500))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                finish = True

        
    if state == 2:
        if asset_lib.state_2_txt_index > 1:
            return True 
    
        win.blit(asset_lib.Helvetica_font.render(asset_lib.state_2_txt[asset_lib.state_2_txt_index],True,(255,0,0),(0,0,0)),(300,400))
        win.blit(asset_lib.interact_font.render("'space to continue'",True,(255,255,255),(0,0,0)),(300,450))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                asset_lib.state_2_txt_index += 1

        