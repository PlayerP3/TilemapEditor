import pygame,random,os,string,numpy
from pygame.math import Vector2

class Camera():

    def __init__(self):
        
        self.bg_offset_x = 0
        self.bg_offset_y = 0
        self.pos = (0,0)
        self.focus = (0,0)
        self.movement = Vector2(0,0)
        self.damping = 0.9 # takes values between 0 and 1, loweer values = dampeningn spring/friction so object doesnt overshoot
        self.spring_stiffness = 0.01 # the inverse of smoothness, higher values is less smooth, loiwer vlaue sis more smooth
        self.zoom = 1

    # change camera view based on what is being shown
    def track_position(self,window):
        self.bg_offset_x = window.get_width()//2 - self.focus[0]
        self.bg_offset_y = window.get_height()//2 - self.focus[1]

    # change camera based on obj
    def track_object(self,focus,window):
        
        self.bg_offset_x = window.get_width()/2 - focus.hurtbox.centerx
        self.bg_offset_y = window.get_height()/2 - focus.hurtbox.centery

    # change camera based on obj
    def track_object_spring(self,window):

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

        self.bg_offset_x = window.get_width()//2 - self.pos[0]
        self.bg_offset_y = window.get_height()//2 - self.pos[1]

        # print(self.vel,(Vector2(focus.hurtbox.center) - Vector2(self.focus)).length())