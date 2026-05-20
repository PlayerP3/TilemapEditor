import pygame,random,os,string,numpy
from animatedsprite import AnimatedSprite,GameSprites
import copy
    
attributes = {
        "zlayer_drawing":0,
        "rect_colour":"red",
        "object_of_origin":"Tile",
        "hurtbox_width":32,
        "hurtbox_height":32,
        "name":"PauseQuitHUD",

        "img_path":"QUIT",
        "img_width":10,
        "img_height":23,
        "img_width_scale":1,
        "img_height_scale":1,

        "is_text":True,
        "text_colour":"white",

        "vertice":"center",
    
        "win_pos":[0,150]}

class Tile(AnimatedSprite):

    def __init__(self):

        AnimatedSprite.__init__(self)

        # you can give a set of sprite objects to the hud element, and give a zlayer as well, and then it handles how it is drawn by the hud
        # the position is always 
        self.display = True

        # this is the position on the win, not the surface it is drawn on
        self.win_pos = (0,0)

        # acitve
        self.is_active = True

        # list of functions we will execute
        self.extraProcessing = []

    # reinit
    def init(self,attributes:dict={}):

        for att,val in attributes.items():

            setattr(self,att,val)
        
        # init sprite variables
        self.init_sprite(SpriteCache=GameSprites)

        self.hurtbox.width = self.hurtbox_width
        self.hurtbox.height = self.hurtbox_height
        self.hurtbox.topleft = self.win_pos

        self.original_vars = {k:v for k,v in self.__dict__.items()}

    # function to update some preoprty about the hud
    def update(self,surface_to_draw_on):

        if self.is_active:

            self.draw_surface(position=self.win_pos,ignore_offset=False,surface_to_draw_on=surface_to_draw_on,schedule_deletion=True)
            
            # draw rect for debugging 
            self.draw_rect(position=self.win_pos,surface_to_draw_on=surface_to_draw_on,schedule_deletion=True)

  



