import pygame,random,os,string,numpy,math
from pygame.math import Vector2
from screen import Window
from camera import Camera
from statemachine import StateMachine
from States.Game.gameplay import Gameplay
from States.Game.quit import Quit
from States.Game.palettebutton import PaletteButton
from States.Game.palette import Palette

# from States.Game import gameover
from eventsystem import eventprocessor
import sys
pygame.font.init()


class GameStateMachine(StateMachine):

    def __init__(self):

        StateMachine.__init__(self)

    def update(self):

        # get all events
        eventprocessor.events = pygame.event.get()

        # handle events
        eventprocessor.process_base_events()


        self.state.update()

        if self.state.done:
            self.transition_to_next_state()

class Game(GameStateMachine):

    def __init__(self):

        # vars for running the game
        self.playing = True
        self.drawing = True
        self.clock = None
       
        self.FPS = 60
        self.delta = 1/self.FPS


        # set palette
        self.palette_state = 'dir'
        self.palette_dir = None
        self.palette_sprites = []

        # position of game objects
        self.object_positions = {}

        # get events
        self.events = None

        # get extra event processing
        self.extra_event_processing = []

        # get active pools
        self.active_pool = []
        self.inactive_pool = {}

        # set player
        self.player = None

        # create hud
        self.hud = None

        # init state machine
        self.states = {'GAMEPLAY':Gameplay(),
                       'QUIT':Quit(),
                       'PALETTEBUTTON':PaletteButton(),
                       'PALETTE':Palette()}
        
        # set parent node for player states
        for x in self.states:
            self.states[x].parent_node = self
        
        self.state = self.states['GAMEPLAY']

        # for creating dmg numbers
        self.display_dmg_num = -1

        # astar graph,coors are key, and Node object is value
        self.astar_graph = {}

        # path cache
        self.path_cache = {}
        self.tile_size = 32
        self.tiles = {}
        self.accessible_tiles = []

        
        # tile display
        self.display_tiles = -1

        # sine wave testing
        self.sinrect = pygame.FRect(-120,0,10,10)
        self.sinrect.center = (-120,0)
        self.sintime = 0

 
        # pen 
        self.pen = pygame.sysfont.SysFont("Arial",10)
        self.damage_number_pen = pygame.sysfont.SysFont("Arial",24)


        
        
    # run update function for all game objects
    def update_game_objects(self):

        if self.active_pool:

            to_remove = []

            for gameobj in self.active_pool:
                gameobj.update()
                if not gameobj.is_active:
                    to_remove.append(gameobj)

            if to_remove:
                for gameobj in to_remove:

                    gameobj.kill(self.active_pool,self.inactive_pool[gameobj.__class__.__name__])

    
    # update positions of all objects in the game
    def update_object_positions(self,coors:tuple,object_to_add:object):

        # check if the coors are in the object position dict already
        if coors not in self.object_positions:

            # add the coors and add the object
            self.object_positions[coors] = [object_to_add]

        # if the coors are already present we just want to add to the list that is already there
        elif coors in self.object_positions:

            if object_to_add not in self.object_positions[coors]:

                self.object_positions[coors].append(object_to_add)


    def display_game_tiles(self,tile_size:int=32):

        
        if self.display_tiles == 1:

            # first we need the width and height of the screen
            # then we need ot know where the center is , in future the center can change depending on which room in the map we are in 
            view_rect = self.windows.win.get_rect(center = (0,0))

            for x in range(view_rect.left,view_rect.right,tile_size):
                for y in range(view_rect.top,view_rect.bottom,tile_size):

                    pos = (x,y)
                
                    rect = pygame.FRect(*pos,32,32)


                    self.drawing_queue[f"{id(rect)}_rect"] = {'game_object':None,
                                                        'asset_to_draw':rect,
                                                        'asset_type':'rect',
                                                        'z_layer':2,
                                                        'surface_to_draw_on':self.windows.win,
                                                        'game_object_origin':'game',
                                                        'is_animated':False,
                                                        'animation_length':0,
                                                        'animation_timer':0,
                                                        'position':pos,
                                                        'position_rect':None,
                                                        'value':0,
                                                        'is_critical':False,
                                                        'sin_waveY':math.radians(90),
                                                        'sin_waveX':0,
                                                        'sin_waveX_movement':random.choice(['positive','negative']),
                                                        'initial_width':2,
                                                        'initial_height':2,
                                                        'scale_factor_timer':1,
                                                        'alpha_value':255,
                                                        'rect_colour':'blue',
                                                        'schedule_deletion':True}
                    
                    # add text
                    # # txt2 = player_Weapon.pen.render(f'Score: {player.score}',True,'blue')
                    txt = self.pen.render(f'({pos[0]},{pos[1]})',True,'blue')

                    txt_rect = txt.get_frect(center=(pos[0]+(tile_size//2),pos[1]+(tile_size//2)))
            
                    self.drawing_queue[f"{id(txt_rect)}_rect"] = {'game_object':None,
                                                        'asset_to_draw':txt,
                                                        'asset_type':'surface',
                                                        'z_layer':2,
                                                        'surface_to_draw_on':self.windows.win,
                                                        'game_object_origin':'game',
                                                        'is_animated':False,
                                                        'animation_length':0,
                                                        'animation_timer':0,
                                                        'position':txt_rect.center,
                                                        'position_rect':txt_rect,
                                                        'value':0,
                                                        'is_critical':False,
                                                        'sin_waveY':math.radians(90),
                                                        'sin_waveX':0,
                                                        'sin_waveX_movement':random.choice(['positive','negative']),
                                                        'initial_width':2,
                                                        'initial_height':2,
                                                        'scale_factor_timer':1,
                                                        'alpha_value':255,
                                                        'rect_colour':'blue',
                                                        'schedule_deletion':True,
                                                        'ignore_offset':False,
                                                        'alpha':255}
    
            

engine = Game()
