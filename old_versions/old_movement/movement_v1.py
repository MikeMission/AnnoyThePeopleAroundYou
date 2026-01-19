#https://www.youtube.com/watch?v=i6xMBig-pP4&
#tutorials 1&3
__author__ = "Mike Mission"
__version__ = "1"

import pygame
'''program to demonstrate basic movement'''

def movement(win,width,height,run,**kwargs):
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
    vel = 20
    x = 50
    y = 50
    while run == True:
        pygame.time.delay(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:run = False
            
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:x -= vel
            if keys[pygame.K_d]:x += vel
            if keys[pygame.K_w]:y -= vel
            if keys[pygame.K_s]:y += vel

        
            win.fill((0,0,0))
            pygame.draw.rect(win, (225, 0, 0), (x, y, width, height))
            pygame.display.update()
        

def prototype_test():
    
    pygame.init()
    win = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Movement Prototype")

    width = 40
    height = 60
    
    run = True
    
    movement(win,width,height,run)

    pygame.quit()


prototype_test()
