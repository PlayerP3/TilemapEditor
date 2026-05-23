import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from statemachine import State


class Quit(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        self.parent_node.save_tilemap()



    def update(self):

        self.parent_node.drawing = False


