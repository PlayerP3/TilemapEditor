import pygame,random,os,string,numpy,json,sys
from pygame.math import Vector2

# load files in
class Screen():

    def __init__(self):
        
        # the final display which the window is drawn onto
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

        # get exact width and height of the full screen once the window has been made full screen, this is needed for centering the player
        self.fullscreen_width = pygame.display.Info().current_w
        self.fullscreen_height = pygame.display.Info().current_h

        # set windows var
        self.windows = {}

    # function to add window
    def add_window(self,winName:str,width:int,height:int):

        self.windows[winName] = Window(width=width,height=height)
        

class Window():
    
    def __init__(self,width:int=1200,height:int=800):

        # get the actual size we want the window to be
        self.width = width
        self.height = height

        # create window, everything is first drawn onto this surface
        self.win = pygame.Surface((self.width,self.height),pygame.SRCALPHA)

        self.rect = None
        self.bg_offset_x = 0
        self.bg_offset_y = 0

        self.extra_offset_x = 0
        self.extra_offset_y = 0

        self.zoomOffsetX = 0
        self.zoomOffsetY = 0

        self.pos = (0,0)
        self.focus = (0,0)
        self.movement = Vector2(0,0)
        self.damping = 0.9 # takes values between 0 and 1, loweer values = dampeningn spring/friction so object doesnt overshoot
        self.spring_stiffness = 0.01 # the inverse of smoothness, higher values is less smooth, loiwer vlaue sis more smooth
        self.zoom = 1

        
    # change camera view based on what is being shown
    def track_position(self):
        self.bg_offset_x = self.win.get_width()//2 - self.focus[0]*self.zoom + self.extra_offset_x
        self.bg_offset_y = self.win.get_height()//2 - self.focus[1]*self.zoom + self.extra_offset_y

        # self.zoomOffsetX = self.win.get_width()//2 * (1 - self.zoom)
        # self.zoomOffsetY = self.win.get_width()//2 * (1 - self.zoom)

    # change camera based on obj
    def track_object(self,focus):
        
        self.bg_offset_x = self.win.get_width()/2 - focus.hurtbox.centerx
        self.bg_offset_y = self.win.get_height()/2 - focus.hurtbox.centery

    # change camera based on obj
    def track_object_spring(self):

        if (Vector2(self.focus) - Vector2(self.pos)).length() <= 0.01:
            self.movement = Vector2(0,0)
        
        # Direction toward target
        acceleration = (Vector2(self.focus) - Vector2(self.pos)) * self.spring_stiffness

        # Add force to velocity
        self.movement += acceleration

        # Damping slows it down over time
        self.movement *= self.damping

        # Move object
        self.pos += self.movement

        self.bg_offset_x = self.win.get_width()//2 - self.pos[0] + self.extra_offset_x
        self.bg_offset_y = self.win.get_height()//2 - self.pos[1] + self.extra_offset_y

        

gameScreen = Screen()

# add main game window
# gameScreen.add_window('mainwindow',1200,800)
gameScreen.add_window('palette',707,800)
gameScreen.add_window('tilemap',1000,600)
gameScreen.add_window('tilemapbuttons',1000,467)
gameScreen.add_window('palettebuttons',707,267)

# set rects
gameScreen.windows['tilemap'].hurtbox = pygame.Rect(0,0,1000,600)
gameScreen.windows['palette'].hurtbox = pygame.Rect(1000,0,707,800)
gameScreen.windows['tilemapbuttons'].hurtbox = pygame.Rect(0,600,1000,467)
gameScreen.windows['palettebuttons'].hurtbox = pygame.Rect(1000,800,707,267)