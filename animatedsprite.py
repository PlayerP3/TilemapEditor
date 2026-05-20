import pygame,os,re,math,random,string
import json
from pygame.math import Vector2
from artist import renderer
from globs import delta
from timer import Timer

GameSprites = {}
TextSprites = {}

class AnimatedSprite():

    def __init__(self,zlayer_drawing:int=0,rect_colour:str='red',object_of_origin:str='Game',rect_width:float=23,rect_height:float=36,
                 hurtbox_width:float=23,hurtbox_height:float=36,sprite_offsetx:float=0,sprite_offsety:float=0,text_colour:str='green',

                 name:str='AnimatedSprite',img_path:str='Sprites/Cards/Hearts/1.png',img_width:int=32,img_width_scale:int=1,img_height:int=32,img_height_scale:int=1,
                 animation_delay:int=1,animation_speed:float=1,alpha:int=255,

                 draw_sine_wave_speed:float=1,draw_sine_wave_amplitude:float=1,

                 starting_direction:int=0,
                 sprite_movement_type:str='none',flip_range:list=[],vertice:str='center',is_text:bool=False):

       

        # set name
        self.name = name

        # dealing with text
        self.is_text = is_text

        # set sprite
        self.sprite = None
        self.image = None
        self.mask = None
        self.mask_img = None
        self.alpha = alpha
        self.alpha_timer = Timer()
        self.sprite_offsetx = sprite_offsetx
        self.sprite_offsety = sprite_offsety
        

        # rect is used for movement and collision
        self.rect = pygame.FRect(0,0,rect_width,rect_height)

        # this rect is used for movement and collision
        self.hurtbox = pygame.FRect(0,0,hurtbox_width,hurtbox_height)

        # hitbox is used for sprite drawing/otherstuff
        # self.hitbox = pygame.FRect(0,0,rect_width,rect_height)
    
        # drawing vars
        self.zlayer_drawing = zlayer_drawing
        self.rect_colour = rect_colour
        self.text_colour = text_colour

        # set activity
        self.is_active = False
        self.is_active_timer = Timer(timer_speed=0,timer_limit=0)

        # get animationt imer
        self.animation_timer = Timer()
        self.alpha_timer = Timer()

        self.object_of_origin = object_of_origin

        # direction variable in json is [start,stop,increment], then we make the list here in the initialising
        self.direction = starting_direction

        self.animation_count = 0
        self.animation_delay = animation_delay
        self.animation_speed = animation_speed

        self.sprite_collection = {}

        self.img_path = img_path
        self.img_width = img_width
        self.img_width_scale = img_width_scale
        self.img_height = img_height
        self.img_height_scale = img_height_scale

        # clearance value
        self.clearance = 1

        # choose if the sprite will be moving/floating like draw_sine or not
        self.sprite_movement_type = sprite_movement_type

        self.draw_sine_wave_timer = 0
        self.draw_sine_wave_speed = draw_sine_wave_speed
        self.draw_sine_wave_amplitude = draw_sine_wave_amplitude

        self.flip_range = flip_range

        # controls whetehr an object is dran on a center, or topleft
        self.vertice = vertice

        # stores the variables of an obj after init
        self.original_vars = None

    # loading sprite sheets
    def load_sprite_sheet(self):
        
        # determine scaled img width and height
        scaled_width = int(self.img_width*self.img_width_scale*1)
        scaled_height = int(self.img_height*self.img_height_scale*1)

        sprite_collection = {}

        for j in range((self.image.get_height()//self.img_height)):

            for i in range((self.image.get_width()//self.img_width)): 

                transimg = pygame.transform.scale(self.image,(scaled_width,scaled_height))
                rotated_surf = pygame.transform.rotate(transimg,angle=-self.direction)
                sprite_collection[i] = rotated_surf

        return sprite_collection
    
    def load_or_update_image(self,SpriteCache:dict=GameSprites):

        # load image from memory if it is in json already
        if self.img_path in SpriteCache:
            if 'loaded_image' in SpriteCache[self.img_path]:
                self.image = SpriteCache[self.img_path]['loaded_image']

           
                self.img_width = self.image.get_width()
                self.img_height = self.image.get_height()

        # load image and store it in json if it does not exist
        elif self.img_path not in SpriteCache:
            
            if not self.is_text:
                SpriteCache[self.img_path] = {'loaded_image':pygame.image.load(self.img_path).convert_alpha()}
                self.image = SpriteCache[self.img_path]['loaded_image']
                self.img_width = self.image.get_width()
                self.img_height = self.image.get_height()

            elif self.is_text:
                self.create_text_image()

    # reinit the sprite and rect 
    def init_sprite(self,SpriteCache:dict=GameSprites):

        # load image, but if it is in memory then just take that
        self.load_or_update_image()
           
        # determine scaled img width and height
        scaled_width = int(self.img_width*self.img_width_scale*1)
        scaled_height = int(self.img_height*self.img_height_scale*1)

        # get dimensions
        dimensions = f"({scaled_width},{scaled_height})"

        # if the class is present but we dont have a sprite for the specific obj
        if self.img_path not in SpriteCache:
            SpriteCache[self.img_path] = {dimensions:{self.direction:{}}}
            SpriteCache[self.img_path][dimensions][self.direction] =  self.load_sprite_sheet()

        # if the specific obj is there but we dont have a class for that specific rect yet
        elif dimensions not in SpriteCache[self.img_path]:
            SpriteCache[self.img_path][dimensions] = {self.direction:{}}
            SpriteCache[self.img_path][dimensions][self.direction] =  self.load_sprite_sheet()

            # print(f' for {self.img_path} adding durection {self.direction}')

        elif self.direction not in SpriteCache[self.img_path][dimensions]:

            SpriteCache[self.img_path][dimensions][self.direction] = {}
            SpriteCache[self.img_path][dimensions][self.direction] = self.load_sprite_sheet()

        self.sprite = SpriteCache[self.img_path][dimensions][self.direction][0]
        self.mask = pygame.mask.from_surface(self.sprite)
        self.mask_img = self.mask.to_surface()

        

    # make damage number
    def create_text_image(self,SpriteCache:dict=GameSprites):

        # load image from memory if it is in json already
        # if self.img_path in SpriteCache:
        #     if 'loaded_image' in SpriteCache[self.img_path]:
        #         self.image =  SpriteCache[self.img_path]['loaded_image']

        #         # set width and heigh to be that of the image
        #         self.img_width = self.image.get_width()
        #         self.img_height = self.image.get_height()


        # load image and store it in json if it does not exist
        # elif self.img_path not in SpriteCache:

        surf = renderer.damage_number_pen.render(f"{self.img_path}",True,self.text_colour)

        GameSprites[self.img_path] = {'loaded_image':surf}

        # set image
        self.image = surf

        # set width and heigh to be that of the image
        self.img_width = self.image.get_width()
        self.img_height = self.image.get_height()

    # update mask and rect based on current sprite
    def update_rect_and_mask(self,SpriteCache:dict=GameSprites):

        # determine scaled img width and height
        scaled_width = int(self.img_width*self.img_width_scale*1)
        scaled_height = int(self.img_height*self.img_height_scale*1)

        # get dimensions
        dimensions = f"({scaled_width},{scaled_height})"

        # if movement type is draw_sine meaning the sprite floats up and down in place
        if self.sprite_movement_type == 'sine':
            self.draw_sine_wave_timer += (delta*self.draw_sine_wave_speed)
            self.rect.centery = self.anchor_pos[1] + math.sin(self.draw_sine_wave_timer)*self.draw_sine_wave_amplitude

            if self.draw_sine_wave_timer >= math.pi*2:
                self.draw_sine_wave_timer = 0

        # update sprite and mask
        self.sprite =  SpriteCache[self.img_path][dimensions][self.direction][0]
        self.mask = pygame.mask.from_surface(self.sprite)
        self.mask_img = self.mask.to_surface()


    

    def update_sprite(self,SpriteCache:dict=GameSprites):

        # dimensions of the sprite
        # dimensions = f"({int(self.img_width*self.img_width_scale)},{int(self.img_height*self.img_height_scale)})"

        # resize or rotate the sprite
        self.resize_and_rotate_sprite()

        # animation_frames = list(self.sprite_collection[self.direction].keys())
        animation_frames = list(SpriteCache[self.img_path][f"({int(self.img_width*self.img_width_scale*1)},{int(self.img_height*self.img_height_scale*1)})"][self.direction].keys())

        # sprite_index = (self.animation_count//self.animation_delay) % len(animation_frames)

        # # self.sprite = self.sprite_collection[self.direction][sprite_index]
        # self.sprite = SpriteCache[self.img_path][dimensions][self.direction][sprite_index]

        # self.animation_count += (delta*self.animation_speed)

        # map index to draw_sine wave timer
        if self.sprite_movement_type == 'sine':
            sprite_index = (self.draw_sine_wave_timer//(math.pi/2)) % len(animation_frames)

        self.update_rect_and_mask()

    

    # for objects that can be rotated in different directions, call this function to rotate them and save it
    # here sprite collection is all the frames/sprites at a given rotation angle 
    def resize_and_rotate_sprite(self,flip_range:list=[],SpriteCache:dict=GameSprites):

        # load or update the image
        self.load_or_update_image()

        # determine scaled img width and height
        scaled_width = int(self.img_width*self.img_width_scale*1)
        scaled_height = int(self.img_height*self.img_height_scale*1)

        

        # get dimensions
        dimensions = f"({scaled_width},{scaled_height})"

        # if the class is present but we dont have a sprite for the specific obj
        if self.img_path not in SpriteCache:

            SpriteCache[self.img_path] = {dimensions:{self.direction:self.load_sprite_sheet()}}

        # if the specific obj is there but we dont have a class for that specific rect yet
        if dimensions not in SpriteCache[self.img_path]:
            SpriteCache[self.img_path][dimensions] = {self.direction:self.load_sprite_sheet()}

        if self.direction not in SpriteCache[self.img_path][dimensions]:
            SpriteCache[self.img_path][dimensions][self.direction] = self.load_sprite_sheet()

        # elif self.direction in SpriteCache[self.img_path][dimensions]:

        #     # update sprite and mask
        #     self.sprite =  SpriteCache[self.img_path][dimensions][self.direction][0]
        #     self.mask = pygame.mask.from_surface(self.sprite)
        #     self.hitbox.width,self.rect.height = self.sprite.get_width(),self.sprite.get_height()
        #     return

        

        # # update sprite and mask
        # self.sprite =  SpriteCache[self.img_path][dimensions][self.direction][0]
        # self.mask = pygame.mask.from_surface(self.sprite)
        # self.hitbox.width,self.hitbox.height = self.sprite.get_width(),self.sprite.get_height()


    def draw_surface(self,asset_type:str='surface',surface_to_draw_on='mainwindow',game_object_origin:str='game',is_animated:bool=False,schedule_deletion:bool=True,
                       animation_length:int=0,position:tuple=(0,0),value:int=0,is_critical:bool=False,initial_width:int=0,initial_height:int=0,
                       zlayer:int=1,ignore_offset:bool=False):

        # update sprite
        self.update_sprite()

        position = (position[0]+self.sprite_offsetx,position[1]+self.sprite_offsety)

        pos_rect = None

        if self.vertice == 'center':

            pos_rect = self.sprite.get_frect(center=position)

        elif self.vertice == 'topleft':

            pos_rect = self.sprite.get_frect(topleft=position)

        random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=12))


        renderer.drawing_queue[random_id] = {'game_object':'obj',
                                        'asset_to_draw':self.sprite,
                                        'asset_type':asset_type,
                                        'z_layer':self.zlayer_drawing,
                                        'surface_to_draw_on':surface_to_draw_on,
                                        'game_object_origin':game_object_origin,
                                        'is_animated':is_animated,
                                        'animation_length':animation_length,
                                        'animation_timer':animation_length,
                                        'position':position,
                                        'position_rect':pos_rect,
                                        'value':value,
                                        'is_critical':is_critical,
                                        'sin_waveY':math.radians(90),
                                        'sin_waveX':0,
                                        'sin_waveX_movement':random.choice(['positive','negative']),
                                        'initial_width':initial_width,
                                        'initial_height':initial_height,
                                        'scale_factor_timer':1,
                                        'alpha':self.alpha,
                                        'ignore_offset':ignore_offset,
                                        'schedule_deletion':schedule_deletion}

    def draw_hitbox(self,asset_type:str='rect',surface_to_draw_on:str='mainwindow',game_object_origin:str='game',
                  is_animated:bool=False,animation_length:int=0,position:tuple=(0,0),value:int=0,is_critical:bool=False,rect_colour:str='blue',
                  zlayer:int=1):

        
        renderer.drawing_queue[f"{id(self)}_rect"] = {'game_object':self,
                                                      'asset_to_draw':self.hitbox,
                                                      'asset_type':asset_type,
                                                      'z_layer':zlayer,
                                                      'surface_to_draw_on':surface_to_draw_on,
                                                      'game_object_origin':game_object_origin,
                                                      'is_animated':is_animated,
                                                      'animation_length':animation_length,
                                                      'animation_timer':animation_length,
                                                      'position':position,
                                                      'position_rect':None,
                                                      'value':value,
                                                      'is_critical':is_critical,
                                                      'sin_waveY':math.radians(90),
                                                      'sin_waveX':0,
                                                      'sin_waveX_movement':random.choice(['positive','negative']),
                                                      'initial_width':None,
                                                      'initial_height':None,
                                                      'scale_factor_timer':1,
                                                      'alpha_value':255,
                                                      'rect_colour':rect_colour,
                                                      'schedule_deletion':True}

    def draw_rect(self,asset_type:str='rect',surface_to_draw_on:str='mainwindow',game_object_origin:str='game',schedule_deletion:bool=True,
                  is_animated:bool=False,animation_length:int=0,position:tuple=(0,0),value:int=0,is_critical:bool=False,rect_colour:str='blue',
                  zlayer:int=1):

        
        renderer.drawing_queue[f"{id(self)}_rect"] = {'game_object':self,
                                                      'asset_to_draw':self.hurtbox,
                                                      'asset_type':asset_type,
                                                      'z_layer':zlayer,
                                                      'surface_to_draw_on':surface_to_draw_on,
                                                      'game_object_origin':game_object_origin,
                                                      'is_animated':is_animated,
                                                      'animation_length':animation_length,
                                                      'animation_timer':animation_length,
                                                      'position':position,
                                                      'position_rect':None,
                                                      'value':value,
                                                      'is_critical':is_critical,
                                                      'sin_waveY':math.radians(90),
                                                      'sin_waveX':0,
                                                      'sin_waveX_movement':random.choice(['positive','negative']),
                                                      'initial_width':None,
                                                      'initial_height':None,
                                                      'scale_factor_timer':1,
                                                      'alpha_value':255,
                                                      'rect_colour':rect_colour,
                                                      'schedule_deletion':schedule_deletion}


class DrawMe():

    def __init__(self):
        
        self.game_object = None

    def init(self):


        pass



