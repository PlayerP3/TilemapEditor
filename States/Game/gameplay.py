import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from statemachine import State
from eventsystem import eventprocessor
from artist import renderer
from screen import gameScreen
from options import *

class Gameplay(State):

    def __init__(self):

        
        State.__init__(self)

    def enter(self):

       pass

    def update(self):
        
        self.submit_event_processing()

        mousePos = pygame.mouse.get_pos()

        # fill window
        # self.parent_node.windows.win.fill((200,0,0))
        # gameScreen.windows['mainwindow'].win.fill((200,0,0))

        # draw tilemap
        


        # if in palette button window
        if gameScreen.windows['palettebuttons'].hurtbox.collidepoint(mousePos):
            self.emit('PALETTEBUTTON')

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.emit('QUIT')