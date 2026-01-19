'''
    Menu module that runs the menu
'''
__author__ = "Mike Mission"
__status__ = "ALPHA"
__license__ = "MIT"
import pygame

pygame.init()
pygame.display.set_mode(size=(800,800))

title_surf = pygame.image.load("main_menu/menu_images/title.xcf")
bg_surf = pygame.image.load("main_menu/menu_images/bg.xcf")

start_surf  = pygame.image.load("main_menu/menu_images/start_img.xcf")
tutorial_surf = pygame.image.load("main_menu/menu_images/tutorial_img.xcf")

settings_surf = pygame.image.load("main_menu/menu_images/settings_img.xcf")
settings_bg = pygame.image.load("main_menu/menu_images/settings_bg.xcf")
settings_quit_surf = pygame.image.load("main_menu/menu_images/settings_quit_img.xcf")
settings_quit_rect = settings_quit_surf.get_rect(topleft = (665,405))

custom_chr_bg = pygame.image.load("main_menu/menu_images/customise_chr_bg.xcf")
custom_chr_bg = pygame.transform.scale(custom_chr_bg,(350,100))
custom_chr_bg_rect = custom_chr_bg.get_rect(topleft = (250,550))

custom_quit_surf = pygame.image.load("main_menu/menu_images/settings_quit_img.xcf")
custom_quit_surf = pygame.transform.scale(custom_quit_surf,(25,25))
custom_quit_rect = custom_quit_surf.get_rect(topleft = (570,555))

edit_ava_surf = pygame.image.load("main_menu/menu_images/edit_avatar_img.xcf")
edit_ava_rect = edit_ava_surf.get_rect(topleft = (150,600))


title_res = (600,300)
bg_res = (800,800)

animation_timer = pygame.USEREVENT + 1
pygame.time.set_timer(animation_timer,100)

bg_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(bg_animation_timer,1000)

def menu_display(win,run):
    clock = pygame.time.Clock()
    inc = 1
    sized = True
    bg_inc = 1
    bg_sized = True
    activate_setting_tab = False
    while run: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == animation_timer:
                if inc < 20 and sized:
                    inc += 1
                if inc == 20:
                    sized = False
                if not(sized):
                    inc -= 1
                if inc == -20:
                    sized = True
                

            if event.type == bg_animation_timer:
                if bg_inc < 5 and bg_sized:
                    bg_inc += 1
                if bg_inc == 5:
                    bg_sized = False
                if not(sized):
                    bg_inc -= 1
                if bg_inc == -5:
                    bg_sized = True
        
        win.blit(animation(bg_surf,bg_inc,bg_res[0],bg_res[1]),(0,0))
        win.blit(animation(title_surf,inc,title_res[0],title_res[1]),(110,10))
        play_button.draw(win)
        settings_button.draw(win)
        tutorial_button.draw(win)
    
        if play_button.clicked():
            run = False
            pygame.QUIT
            return False

        if settings_button.clicked():
            activate_setting_tab = True

        if tutorial_button.clicked():
            run = False 
            pygame.QUIT 
            return True
        
        if activate_setting_tab:
            if settings_tab(win) == False:
                activate_setting_tab = False 


        pygame.display.update()
        clock.tick(60)

def animation(surf,inc,x,y):
    surf = pygame.transform.scale(surf,(x+inc,y+inc))
    return surf

class button():
    def __init__(self,x,y,image,isclicked,disabled):
        self.image = image 
        self.rect = self.image.get_rect() 
        self.rect.topleft = (x,y) 
        self.isclicked = isclicked
        self.disabled = disabled

    def draw(self,win):
        '''Draws the button'''
        win.blit(self.image, (self.rect.x, self .rect.y))

    def clicked(self) -> bool:
        ''' detects if the player has interacted with it'''
    
        if self.disabled == False:
            pos = pygame.mouse.get_pos()
            
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.isclicked == False:
                    self.isclicked = True
            
            if pygame.mouse.get_pressed()[0] == 0:
                self.isclicked = False
            
            return self.isclicked
        elif self.disabled == True:
            return False

display_custom = False
player_gender = "male" #default (don't mind me)

male = pygame.image.load("main_menu/menu_images/male_img.xcf")
female = pygame.image.load("main_menu/menu_images/female_img.xcf")

def settings_tab(win):
    '''tab for settings'''
    global display_custom
    global player_gender
    global male,female
    #POLYMORPHISM AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH.🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮🤮

    male_rect = male.get_rect(topleft = (290,570))
    female_rect = female.get_rect(topleft = (400,570))

    for button in buttons:
        button.disabled = True

    win.blit(settings_bg,(75,400))
    win.blit(settings_quit_surf,settings_quit_rect)
    win.blit(edit_ava_surf,edit_ava_rect)

    pos = pygame.mouse.get_pos()

    if settings_quit_rect.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] == 1:
            for button in buttons:button.disabled = False
            return False

    if edit_ava_rect.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] == 1:
            display_custom = True
    
    if display_custom == True:
        win.blit(custom_chr_bg,custom_chr_bg_rect)
        win.blit(male,male_rect)
        win.blit(female,female_rect)
        win.blit(custom_quit_surf,custom_quit_rect)

        if custom_quit_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                display_custom = False

        if male_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                player_gender = "male"

        if female_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                player_gender = "female"
    
    if player_gender == "male":
        male = pygame.transform.scale(male,(120,70))
        female = pygame.transform.scale(female,(100,50))
    elif player_gender == "female":
        female = pygame.transform.scale(female,(120,70))
        male = pygame.transform.scale(male,(100,50))

play_button = button(250,350, start_surf,False,False)
settings_button = button(250,450, settings_surf,False,False)
tutorial_button = button(250,550, tutorial_surf,False,False)
buttons = [play_button,tutorial_button]

