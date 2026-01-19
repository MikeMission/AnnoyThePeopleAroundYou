''' holds code for minigames '''
__authour__ = "Mike Mission"
__status__ = "ALPHA"
__license__ = "MIT"

import pygame 
from random import randint 
pygame.init()

direction = "left"
spam_text_image = pygame.image.load("core_tools/minigame_sprites/spam/spam_text.xcf")

bar_success_area = pygame.image.load("core_tools/minigame_sprites/bar/bar_success_area.xcf")
bar_success_rect = bar_success_area.get_rect(midbottom = (randint(300,500),592))

bar_bg = pygame.image.load("core_tools/minigame_sprites/bar/bar_bg.xcf")
bar_bg_rect = bar_bg.get_rect(midbottom = (400,600))

bar_player = pygame.image.load("core_tools/minigame_sprites/bar/bar_player.xcf")
bp_rect = bar_player.get_rect(midbottom = (400,592))


def bar_minigame(win,i_object,asset_lib,bar_speed = randint(3,10)) -> bool:
    '''
    displays a bar with 4 colours,black, white, green, orange
    border colour = black
    border fill = white
    success colour = green
    player colur = orange
    '''
    global direction
    global bar_success_area,bar_success_rect
    global bp_rect,bar_player
    global bar_bg,bar_bg_rect

    if i_object.won:
        return True
    elif i_object.won is False and i_object.stopped:
        return False
    #prevent running again if object is won.
    
    win.blit(bar_bg,bar_bg_rect)
    win.blit(bar_player,bp_rect)
    win.blit(bar_success_area,bar_success_rect)
    win.blit(asset_lib.Helvetica_font.render("[press space to stop]",True,(255,0,0)),(300,520))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        i_object.stopped = True
        #stop the user's bar

    #change direction
    if bp_rect.x < 203 + bar_speed:direction = "right"
    elif bp_rect.x > 595 - bar_speed:direction = "left"

    if not(i_object.stopped):
        #move bar
        if direction == "left":bp_rect.x -= bar_speed
        elif direction == "right":bp_rect.x += bar_speed

    elif i_object.stopped:
        if bp_rect.colliderect(bar_success_rect):
            i_object.won = True
            return True
        else:
            i_object.won = False
            return False

    win.blit(bar_player,bp_rect)   

def spam_minigame(win,i_object,asset_lib,event) -> bool:
    '''
    --spam minigame--
    displays text to tell player to spam.
    text will scale with how much space bar clicks occur
    have to reach a certain number in a 15 seconds
    takes: win(screen)
    returns a boolean 
    '''    
    global spam_text_image
    spam_text_image_rect = spam_text_image.get_rect(midbottom = (400,500))
    spam_text_image_ = spam_text_image

    space_requirement_text = i_object.space_requirement - i_object.space_amount 
    
    if i_object.won == True:
        return True
    
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
            space_requirement_text -= 1
            i_object.space_amount += 1
            spam_text_image_ = pygame.transform.scale(spam_text_image,(199+i_object.space_amount,49+i_object.space_amount))

    if i_object.space_amount >= i_object.space_requirement:
        return True 
    
    space_requirement_surf = asset_lib.Helvetica_font.render(str(space_requirement_text),True,(255,255,255))
    
    win.blit(space_requirement_surf,(400,600))
    win.blit(spam_text_image_,spam_text_image_rect)

def click_drag_minigame(win,asset_lib,clicked = False) -> bool:
    ''' click drag minigame for trash dragging (not optimised for general use tbh) '''

    #actual minigame bins 
    r_bin = pygame.transform.scale(asset_lib.r_bin.surf,(150,150))
    r_bin_rect = r_bin.get_rect(topleft = (428,490))  
    bin = pygame.transform.scale(asset_lib.bin.surf,(150,150))
    bin_rect = bin.get_rect(topleft = (228,490))

    #first two are for recycle bin, next two are for regular bin

    for i_object in asset_lib.interactive_objects: 
        if i_object.name in ("toys","fridge","tv"):i_object.disabled = not((
        r_bin_rect.contains(asset_lib.click_drag_objects[0][0]) and
        r_bin_rect.contains(asset_lib.click_drag_objects[1][0]) and 
        bin_rect.contains(asset_lib.click_drag_objects[2][0]) and 
        bin_rect.contains(asset_lib.click_drag_objects[3][0])
        ))
        
    if (
        r_bin_rect.contains(asset_lib.click_drag_objects[0][0]) and
        r_bin_rect.contains(asset_lib.click_drag_objects[1][0]) and 
        bin_rect.contains(asset_lib.click_drag_objects[2][0]) and 
        bin_rect.contains(asset_lib.click_drag_objects[3][0])
        ):


        return True 

    #blit
    win.blit(asset_lib.trash_bg,(200,200))
    win.blit(asset_lib.Helvetica_font.render("Move the trash to the wrong bin",True,(0,0,0),(255,255,255)),(222,163))

    win.blit(r_bin,r_bin_rect)
    win.blit(bin,bin_rect)

    pos = pygame.mouse.get_pos()
    #print(pos)

    #clickable objects is a 2d list with objects rect and surfaces combined together [[rect,surf],[rect,surf]] etc.
    for obj in asset_lib.click_drag_objects:
        win.blit(obj[1],obj[0])
        if not(clicked): #if the mouse is not clicked
            if obj[0].collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    obj[0] = obj[1].get_rect(center=pos)
                    clicked = True 

def click_minigame(win,asset_lib,clicked = False) -> bool:
    ''' a minigame where the player clickes sprites '''

    pos = pygame.mouse.get_pos()
    #print(pos)
    clicked_list = [x[2] for x in asset_lib.clickable_objects]
    #if all is clicked

    for i_object in asset_lib.interactive_objects: 
            if i_object.name in ("toys","fridge","tv"):i_object.disabled = not(all(clicked_list))
    
    if all(clicked_list):
        return True

    win.blit(asset_lib.fridge_bg,(100,100))
    win.blit(asset_lib.Helvetica_font.render("Click to eat food",True,(255,255,255),(0,0,0)),(340,66))

    for i_object in asset_lib.interactive_objects: #prevent displaying stupid objects 👋
        if i_object.name in ("toys","fridge","tv"):i_object.disabled = not(all(clicked_list))


    for obj in asset_lib.clickable_objects:
        win.blit(obj[1],obj[0])
        if not(clicked):
            if obj[0].collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    obj[0] = obj[1].get_rect(topleft = (900,900)) #gets rid of the obj
                    obj[2] = True #self.click = True
                    clicked = True 
