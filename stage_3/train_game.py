__authour__ = "Mike Mission"
__status__ = "ALPHA"
__license__ = "MIT"

import pygame 
from core_tools.tools import play_player_animation,collision_with_static,time_determiner
import stage_3.train_image_lib as asset_lib
from stage_3.train_image_lib import seats
from random import choice

pygame.init()
actual_timer = pygame.USEREVENT + 1 
pygame.time.set_timer(actual_timer, 1000)

drunk_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(drunk_animation_timer,1200)

projectile_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(projectile_animation_timer,800)

player_animation_timer = pygame.USEREVENT + 4
pygame.time.set_timer(player_animation_timer, 150)

basic_move_animation_timer = pygame.USEREVENT + 5
pygame.time.set_timer(basic_move_animation_timer,200)

basic_projectile_generation_timer = pygame.USEREVENT + 6
pygame.time.set_timer(basic_projectile_generation_timer,2300)

complex_projectile_generation_timer = pygame.USEREVENT + 7
pygame.time.set_timer(complex_projectile_generation_timer,7500)

fist_animation_timer = pygame.USEREVENT + 8
pygame.time.set_timer(fist_animation_timer,469) # 469 each frame cause length of 8

drink_animation_timer = pygame.USEREVENT + 9
pygame.time.set_timer(drink_animation_timer,1500) # 1000 each frame cause length of 5

font = pygame.font.SysFont("Helvetica", 20, bold=True, italic=False)

def game(win,run,game_active,**kwargs):
    vel = 2.5  
    x = y = 400
    secs = mins = 0
    trash_text = death_message = ""
    timer_text = font.render("{}:{}".format(mins,secs),True,(255,0,0),(0,0,0))
    clock = pygame.time.Clock()
    movement = True
    died = False
    player_direction = "idle"
    if "vel" in kwargs:
        vel = kwargs["vel"]
    state = 1
    complex_attack = False
    attack = None
    finish = False
    attack_type = "up to down" # default attack, may wanna randomiseee,,,,
        
    player_surf = asset_lib.player_idle
    drunk_surf = asset_lib.drunk_frames[asset_lib.drunk_index]
    pygame.time.delay(2)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                pygame.quit()

            keys = pygame.key.get_pressed()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:player_direction = "left"
                elif event.key == pygame.K_d:player_direction = "right"
                elif event.key == pygame.K_w:player_direction = "up"
                elif event.key == pygame.K_s:player_direction = "down"

            elif event.type == pygame.KEYUP and not((keys[pygame.K_a] or keys[pygame.K_d])):
                player_direction = "idle"
                player_surf = asset_lib.player_idle
            elif event.type == pygame.KEYUP and (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_s] or keys[pygame.K_w]):
                if keys[pygame.K_a]:player_direction = "left"
                elif keys[pygame.K_d]:player_direction = "right"
                elif keys[pygame.K_w]:player_direction = "up"
                elif keys[pygame.K_s]:player_direction = "down"

            if event.type == player_animation_timer:
                player_surf = play_player_animation(player_direction,asset_lib)

            if state == 0:
                temp = cutscene_text(win,state,death_message,event)
                #reset values
                asset_lib.enemy_index = 0  
                asset_lib.drunk_animate = True    
                asset_lib.bottles = [] 
                secs = mins = 0
                attack = None 
                complex_attack = False
                attack_type = "up to down"
                asset_lib.box = pygame.image.load("stage_3/train_images/drunk/box.xcf")

                if temp is not None:
                    game_active = temp[0]
                    state = temp[1]    
                    died = False        
            
            if state == 1:

                if event.type == drunk_animation_timer and asset_lib.drunk_animate:
                    drunk_surf = play_drunk_animation()

                if not(asset_lib.drunk_animate): 
                    if event.type == (pygame.KEYDOWN) and (keys[pygame.K_SPACE]):
                        asset_lib.enemy_index += 1
                    elif asset_lib.enemy_index is len(asset_lib.enemy_dialogue):#prevent enemy index == len(dialoughe)
                        asset_lib.enemy_index -= 1
                        y,x = 640,400 # player has new position
                        state = 2 
        
            if state == 2:
                if event.type == actual_timer:
                    secs += 1

                    if secs == 60:
                        mins += 1 
                        secs = 0 #resets seconds

                    timer_text = time_determiner(secs,mins,font)

                if event.type == drunk_animation_timer:
                    asset_lib.drunk_frames = [asset_lib.drunk_idle,asset_lib.drunk_idle1] 
                    drunk_surf = play_drunk_animation()
                    trash_text = choice(asset_lib.trashes)

                if event.type == basic_projectile_generation_timer:
                    if secs < 60: # phase 1
                        asset_lib.generate_bottle(2,attack_type) # will generate 1 every 2300ms

                    if mins == 1 and not complex_attack: # phase 2
                        asset_lib.bottles = []
                        if secs > 10 and attack_type != "overwhelm":
                            asset_lib.generate_bottle(3,attack_type)


                if event.type == complex_projectile_generation_timer:
                    if complex_attack:
                        asset_lib.bottles = []
                        attack_type = "overwhelm" + choice(("up","down","left","right")) # should only access once per 5 s
                        # generate a instance of complex class, and then..

                        attack = asset_lib.complex_projectile(attack_type[9:])
                        # print(attack.direction)
                
                    #animate the attack.

                if complex_attack and attack is not None:
                    if event.type == drink_animation_timer and attack.direction in ("up","down"):
                        attack.animate()
                        

                    if event.type == fist_animation_timer and attack.direction in ("left","right"):
                        attack.animate()
                        




                if event.type == projectile_animation_timer:
                    for bottle in asset_lib.bottles:
                        bottle.surf = play_projectile_animation(bottle)
                
                if event.type == basic_move_animation_timer:
                    for bottle in asset_lib.bottles:
                        bottle.move()

            if state == 3:
                finish = cutscene_text(win,state,None,event)
                

        if game_active:
            win.blit(asset_lib.bg,(0,0))

            player_rect = player_surf.get_rect(midbottom = (x,y))

            for rect in asset_lib.collidable_rects:
                if player_rect.colliderect(rect):
                    movement = collision_with_static(player_rect,rect)

            keys = pygame.key.get_pressed()

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

            if state == 1:
                map_1(win,drunk_surf)
                if player_rect.colliderect(asset_lib.drunk_rect):
                    #drunk person talks
                    drunk_surf = asset_lib.drunk_talk
                    asset_lib.drunk_animate = False 
                    win.blit(asset_lib.drunk_font.render(asset_lib.enemy_dialogue[asset_lib.enemy_index],True,(255,255,255),(0,0,0)),(225,10))
                    
                else:
                    asset_lib.drunk_animate = True 
            
            elif state == 2:


                if secs in (15,30,45) and mins == 0:
                    attack_type = choice(asset_lib.attack_types)

                # phase 2
                if secs in (15,50) and mins == 1:
                    attack_type = choice(asset_lib.attack_types)

                if mins == 1 and secs == 20: # animation 5 seconds.
                    complex_attack = True # should trigger event 

                if mins == 1 and secs < 15: 
                    asset_lib.trashes = ("time to crank it up","not to shabby...","but can you handle THIS?","this is only the begginning","Im not finished with you yet")
                elif mins == 1 and secs > 15:
                    asset_lib.trashes = ("you are no match for me","go to sleep","feeling tired yet?","*glug *glug","*cough")
                
                if mins == 2:
                    asset_lib.box = asset_lib.box = pygame.image.load("stage_3/train_images/drunk/box.xcf")
                    complex_attack = False 
                    asset_lib.bottles = []
                    state = 3 # trigger cutscene text 
                    game_active = False


                asset_lib.collidable_rects = [] #empty so new rects can be generated

                map_2(win,drunk_surf,trash_text)

                #box for the player
                win.blit(asset_lib.box,(150,500))
                
                if attack is not None and attack.collision_rect is not None:
                    if player_rect.colliderect(attack.collision_rect):
                        death_message = "Try to stay near the center of the box"
                        game_active = False 
                        died = True 

                if not(complex_attack):

                    #blit indicator arrow
                    temp = asset_lib.generate_caution(attack_type)
                    if temp is not None:
                        win.blit(temp[0],temp[1])

                    #blit bottles
                    for bottle in asset_lib.bottles:
                        if bottle.type != attack_type:asset_lib.bottles.remove(bottle)
                        win.blit(bottle.surf,bottle.rect)
                        if bottle.collision(player_rect):
                            death_message = "Try to avoid the bottles."
                            game_active = False
                            died = True
                        for wall in asset_lib.box_walls:
                            if bottle.collision(wall):
                                bottle.generate() #reset pos..
                                asset_lib.bottles.remove(bottle)

        
                for rect in asset_lib.box_walls:
                    if player_rect.colliderect(rect):
                        movement = collision_with_static(player_rect,rect)

                win.blit(font.render("survive for 2 mins",True,(255,0,0),(0,0,0)),(600,450))
                win.blit(timer_text,(700,600))

                win.blit(player_surf,player_rect)
               
        if died:
            state = 0

        if finish:
            return 120

        # pos = pygame.mouse.get_pos()
        # print(pos)

        pygame.display.update()
        clock.tick(60)

def map_1(win,drunk_surf):
    ''' blits all the assets for map 1 '''
    win.blit(asset_lib.train_window_1,asset_lib.window_rect)
    win.blit(asset_lib.train_window_2,asset_lib.windown_rect_2)
    for seat in seats:
        win.blit(seat[0],seat[1])
    win.blit(pygame.transform.scale(drunk_surf,(100,75)),asset_lib.drunk_rect)

def map_2(win,drunk_surf,text):
    ''' blits all the assets for bossfight '''
    win.blit(asset_lib.bg_2,(0,0))
    win.blit(pygame.transform.scale(drunk_surf,(800,775)),(15,150))
    win.blit(asset_lib.big_font.render(text,True,(255,255,255),(0,0,0)),(400,100))


def play_drunk_animation()-> pygame.surface:
    ''' plays drunk animation (switches frames) '''
    if asset_lib.drunk_index == 1:asset_lib.drunk_index = 0
    else:asset_lib.drunk_index = 1
    return asset_lib.drunk_frames[asset_lib.drunk_index]

def play_projectile_animation(projectile)-> pygame.surface:
    ''' plays projectile animation '''
    if projectile.index == 1:projectile.index = 0
    else:projectile.index = 1
    return projectile.frames[projectile.index]

def cutscene_text(win,state,death_message,event,end = False):
    if state == 0:
        win.fill("black")
        win.blit(font.render(death_message,True,(255,0,0)),(400,300))
        win.blit(font.render("'r to respawn'",True,(255,255,255)),(400,350))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return (True,1)
    elif state == 3:
        if asset_lib.end_index > len(asset_lib.end_dialogue)-1:
            end = True
        else:
            win.blit(asset_lib.bg_2,(0,0))
            win.blit(pygame.transform.scale(asset_lib.drunk_talk,(800,775)),(15,150))
            win.blit(asset_lib.box,(150,500))
            win.blit(asset_lib.big_font.render(asset_lib.end_dialogue[asset_lib.end_index],True,(255,255,255),(0,0,0)),(200,600))
            win.blit(asset_lib.font.render("'space to continue'",True,(255,255,255),(0,0,0)),(350,655))


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    asset_lib.end_index += 1

        if end:
            win.fill("black")
            win.blit(asset_lib.big_font.render("GG",True,(255,255,255),(0,0,0)),(350,200))
            win.blit(asset_lib.big_font.render("sprites: Mike Mission",True,(255,255,255),(0,0,0)),(350,450))
            win.blit(asset_lib.big_font.render("developer: Mike Mission",True,(255,255,255),(0,0,0)),(350,500))
            win.blit(asset_lib.big_font.render("story: Mike Mission",True,(255,255,255),(0,0,0)),(350,550))
            win.blit(asset_lib.font.render("'space to continue'",True,(255,255,255),(0,0,0)),(350,625))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    asset_lib.end = True
        
        if asset_lib.end:
            return True
    