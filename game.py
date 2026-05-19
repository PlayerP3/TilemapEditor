import pygame,random,os,string,numpy,math
from pygame.math import Vector2
from screen import Window
from camera import Camera
from statemachine import StateMachine
from States.Game.gameplay import Gameplay
from States.Game.quit import Quit
from States.Game.palettebutton import PaletteButton

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

        self.drawing_queue = {}
 
        # set camera
        self.camera = Camera()

        # set window
        self.windows = Window()

        # set palette
        self.palette = None

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
                       'PALETTEBUTTON':PaletteButton()}
        
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

    # # function that handless all drawing
    # def draw_objects(self):

    #     # Z layer list
    #     # Zombies - 0
    #     # Boss - 1
    #     # Boss Projectile - 2
    #     # Boss Orbital - 3
    #     # Player - 4
    #     # Player Projectile - 5
    #     # Player Orbital - 6
    #     # Danage Numbers - 7

    #     # this allows us to resolve z layers
    #     # meaning if there are multiple of a game object type on a layer
    #     # we refer to this to see what gets drawn first
    #     GameObjectPriority = {'Enemy':0,
    #                         'Player':0,
    #                         'Boss':0,
    #                         'Bullet':1,
    #                         'Orbital':2,
    #                         'DamageNumbers':3}
        
    #     # get all different surfaces that could be drawn on, always put winas the last
    #     surfs = list(set([drawinstruc['surface_to_draw_on'] for objid,drawinstruc in self.drawing_queue.items()]))

    #     if self.windows.win in surfs:
    #         surfs.remove(self.windows.win)
    #         surfs.append(self.windows.win)

    #     # go through each surface
    #     for surf in surfs:

    #         # create dictionary with only items that will be drawn on that surface
    #         specific_drawing_queue = dict(filter(lambda item: self.drawing_queue[item[0]]['surface_to_draw_on'] == surf, self.drawing_queue.items()))

    #         # sort drawing queue based on z layer
    #         # ZlayerSortedDrawingQueue = sorted(Creative_Mode.drawing_queue,key=lambda id:Creative_Mode.drawing_queue[id]['z_layer'],reverse=True)
    #         ZlayerSortedDrawingQueue = dict(sorted(specific_drawing_queue.items(),key=lambda x:self.drawing_queue[x[0]]['z_layer'],reverse=False))

    #         # for unique_id in Creative_Mode.drawing_queue:
    #         for unique_id in ZlayerSortedDrawingQueue:

    #             # print(ZlayerSortedDrawingQueue['key'])

    #             # if what we are drawing is going to be a surface
    #             if ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'surface':

    #                 adjusted_position = (0,0)

    #                 if not ZlayerSortedDrawingQueue[unique_id]['ignore_offset']:
    #                     adjusted_position = (ZlayerSortedDrawingQueue[unique_id]['position_rect'].x + self.camera.bg_offset_x, ZlayerSortedDrawingQueue[unique_id]['position_rect'].y + self.camera.bg_offset_y)

    #                 elif ZlayerSortedDrawingQueue[unique_id]['ignore_offset']:
    #                     adjusted_position = (ZlayerSortedDrawingQueue[unique_id]['position_rect'].x + self.windows.win.get_width()//2, ZlayerSortedDrawingQueue[unique_id]['position_rect'].y + self.windows.win.get_height()//2)



    #                 if ZlayerSortedDrawingQueue[unique_id]['alpha'] != -1:
                    
    #                     ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].set_alpha(ZlayerSortedDrawingQueue[unique_id]['alpha'])


    #                 # adjusted_position = (int(adjusted_position[0]),int(adjusted_position[1]))
    #                 ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'].blit(ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'],adjusted_position)


    #             # if what we are drawing is going to be a rect
    #             elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'rect':

    #                 adjusted_position_rect = pygame.FRect(ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].x + self.camera.bg_offset_x,
    #                 ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].y + self.camera.bg_offset_y,
    #                 ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].width,
    #                 ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].height)

    #                 # draw rects
    #                 pygame.draw.rect(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],ZlayerSortedDrawingQueue[unique_id]['rect_colour'],adjusted_position_rect,1)

    #             # if what we are drawing is going to be a surface
    #             elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'circle':

    #                 # if inactive schedule deletion
    #                 if not ZlayerSortedDrawingQueue[unique_id]['game_object'].is_active:
    #                     ZlayerSortedDrawingQueue[unique_id]['schedule_deletion'] = True
    #                 # draw rects
    #                 pygame.draw.circle(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],'blue',(ZlayerSortedDrawingQueue[unique_id]['game_object'].centerx+self.bg_offset_x,ZlayerSortedDrawingQueue[unique_id]['game_object'].centery+self.bg_offset_y),ZlayerSortedDrawingQueue[unique_id]['radius'],2)

    #             # if what we are drawing is going to be a surface
    #             elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'line':

    #                 adjusted_start =  (ZlayerSortedDrawingQueue[unique_id]['startpos'][0] + self.camera.bg_offset_x,ZlayerSortedDrawingQueue[unique_id]['startpos'][1] + self.camera.bg_offset_y)
    #                 adjusted_end = (ZlayerSortedDrawingQueue[unique_id]['endpos'][0] + self.camera.bg_offset_x,ZlayerSortedDrawingQueue[unique_id]['endpos'][1] + self.camera.bg_offset_y)

    #                 pygame.draw.line(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],'blue',adjusted_start,adjusted_end)

    #             # if what we are drawing is going to be a surface
    #             elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'lines':

    #                 points = [(p[0] + self.camera.bg_offset_x, p[1] + self.camera.bg_offset_y) for p in ZlayerSortedDrawingQueue[unique_id]['points']]

    #                 pygame.draw.lines(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],color='blue',points=points,closed=False)


    #             # if what we are drawing is going to be a surface
    #             elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'polygon':

    #                 adjusted_endpoints = []

    #                 if not ZlayerSortedDrawingQueue[unique_id]['ignore_offset']:
    #                     adjusted_endpoints = [(e[0]+ self.camera.bg_offset_x,e[1]+ self.camera.bg_offset_y) for e in ZlayerSortedDrawingQueue[unique_id]['endpoints']]

    #                 elif ZlayerSortedDrawingQueue[unique_id]['ignore_offset']:
    #                     adjusted_endpoints = [(e[0]+ self.windows.win.get_width()//2,e[1]+ + self.windows.win.get_height()//2) for e in ZlayerSortedDrawingQueue[unique_id]['endpoints']]


    #                 pygame.draw.polygon(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],(255,255,255),adjusted_endpoints)



    #     self.drawing_queue = {k:self.drawing_queue[k] for k in self.drawing_queue if not self.drawing_queue[k]['schedule_deletion']}



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
