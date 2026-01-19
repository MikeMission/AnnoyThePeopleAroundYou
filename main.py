#https://docs.python.org/3/library/sqlite3.html

'''
The main program that runs everything MUHAHAHAAAA 😈😈😈😈😈
'''
__author__ = "Mike Mission"
__status__ = "ALPHA"
__license__ = "MIT"

#res 800,800
import pygame
import sqlite3
import main_menu.menu as menu
import stage_0.tutorial_game as tutorial_game
import stage_1.classroom_game as classroom_game
import stage_2.home_game as home_game
import stage_3.train_game as train_game
import datetime

'''
Create table for the database for the player wwwwwwwewww
'''

class user_db():
    def __init__(self):
        self.conn = sqlite3.connect('Player_database.db')
        self.cur = self.conn.cursor()
        self.player_id = None 
        self.capacity = self.biggest_id() # used for overall database to clean if too big.

    def new_user(self):
        ''' creates a new user '''
        Stage1_Time = Stage2_Time = Stage3_Time = 0 # initially the times for a new user is 0
        self.player_id = int(self.biggest_id()) + 1 # increments the user id
        date = datetime.date.today() 

        with self.conn:
            self.cur.execute("INSERT INTO Players VALUES"
            + f"({self.player_id},'{date}',{Stage1_Time},{Stage2_Time},{Stage3_Time})")
            print("conn1")
        

    def update_time(self,time,stage):
        ''' 
        inserts a time into the database table
        will be accesed in order of stages: 1,2,3
        '''
        with self.conn:
            self.cur.execute("UPDATE Players SET " + f"{stage}_time = {time} WHERE Player_ID = {self.player_id}")
        print("conn2")
    
    def biggest_id(self):
        ''' 
        fetches the next biggest id 
        '''
        with self.conn:
            self.player_id = self.cur.execute("SELECT MAX(player_ID) FROM players")
            self.player_id = self.player_id.fetchone()
        return self.player_id[0]
    

#main loops

pygame.init()

game_active = True #determines game over screen
run = True #determines actual loop running

win = pygame.display.set_mode((800,800))
pygame.display.set_caption("game")
#oo look fancy 💅
stage_0 = stage_1 = stage_2 = stage_3 = True
time_1 = time_2 = time_3 = 0


db = user_db() #instance of db

while run:
    db.new_user()
    stage_0 = menu.menu_display(win,run) 

    while stage_0 is True:
        print("tutorial")
        tutorial_game.tutorial(win,run,game_active)
        if tutorial_game.finish is True:
            stage_0 = False 
        stage_0 = menu.menu_display(win,run)
    
    if stage_1 is True: 
        print("classroom")
        time_1 = classroom_game.game(win,run,game_active) or 0
    db.update_time(time_1,"Stage1")

    if stage_2 is True:
        print("home") 
        time_2 = home_game.game(win,run,game_active) or 0
    db.update_time(time_2,"Stage2")
    
    if stage_3 is True:
        print("train")
        time_3 = train_game.game(win,run,game_active) or 0
    db.update_time(time_3,"Stage3")
    #prevent runtime error
    run = False

pygame.quit()

