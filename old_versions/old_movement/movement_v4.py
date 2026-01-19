#https://www.youtube.com/watch?v=i6xMBig-pP4&
#tutorials 1&3
__author__ = "Mike Mission"
__version__ = "4"

'''
Trying to incorperate rectangular surfaces into the sprites
'''

x = 50
y = 50

import pygame
import asset_lib_v4 as asset_lib
'''program to demonstrate basic movement'''

def movement(win,run,**kwargs):
    global x
    global y
    '''
        Makes a pixel move via 'wasd'
        parameters:win,width,height,run,kwargs
        kwargs:{vel:1,x:1,y:1}
        output:None
    '''    
    if "vel" in kwargs:vel = kwargs["vel"]
    elif "x" in kwargs:x = kwargs["x"]
    elif "y" in kwargs:y = kwargs["y"]
    #Default values for vel,x,y, for change:look^^^
    #function doesn't work properly if vars aren't definied in it
    vel = 7.5
    clock = pygame.time.Clock()

    player_rect = asset_lib.player_surface.get_rect(midbottom = (x,y))

    x = 50
    y = 50
    #^ future reference for hitboxes, but will not be used for literal size (sprite usage)

    while run == True:
        pygame.time.delay(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:run = False

            player_rect = asset_lib.player_surface.get_rect(midbottom = (x,y))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a] and x > vel:x -= vel
            if keys[pygame.K_d] and x < 775 - vel:x += vel
            if keys[pygame.K_w] and y > vel :y -= vel
            if keys[pygame.K_s] and y < 775 - vel :y += vel

            print(player_rect.midbottom)

        #load background
        win.blit(asset_lib.test_surface,(0,0))
        win.blit(asset_lib.text_surface,(0,0))#text has to be loaded within win
        win.blit(asset_lib.bush_surface,asset_lib.bush_rect)

        #load player
        win.blit(asset_lib.player_surface,player_rect)

        #load npc
        #asset_lib.baby_rect.x += 3
        #print(asset_lib.baby_rect)
        win.blit(asset_lib.baby_surface,asset_lib.baby_rect)
        pygame.display.update()
        clock.tick(60)
        


# def npcMovement(win,npc,run)
#     if npc == "baby":
#         x += randint(2,5)
#         y += randint(2,5)
#         win.blit(asset_lib.baby,(x,y))




def prototype_test():
    
    pygame.init()

    win = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Movement Prototype")

    run = True
    
    movement(win,run)

    pygame.quit()



