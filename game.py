import pygame,random,os,string,numpy,math
from pygame.math import Vector2
from screen import Window
from statemachine import StateMachine
from States.Game.gameplay import Gameplay
from States.Game.quit import Quit
from States.Game.palettebutton import PaletteButton
from States.Game.palette import Palette
from States.Game.tilemap import Tilemap
from States.Game.tilemapbutton import TilemapButton
from States.Game.definingattributes import DefiningAttributes


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

        print(self.tilemap)

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
                       'PALETTE':Palette(),
                       'TILEMAP':Tilemap(),
                       'TILEMAPBUTTON':TilemapButton(),
                       'DEFININGATTRIBUTES':DefiningAttributes()}
        
        # set parent node for player states
        for x in self.states:
            self.states[x].parent_node = self
        
        self.state = self.states['PALETTE']


        self.tile_size = 32

        self.currentSprite = None
        self.currentClass = 'BgTile'
 
        # tilemap config
        self.tilemap = {}
        self.tilemapEntryID = 0


        # so we have a {imgpath,rectwidthheight,zlayer_drawing,position,class}
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


    def draw_tilemap(self):

        if self.tilemap:

            # get all the sprites 
            sprites = []

            for layer,posinfo in self.tilemap.items():

                for pos,spriteinfo in posinfo.items():

                    sprites.append(spriteinfo['AnimatedSprite'])

            for s in sprites:
                s.draw_surface(position=s.hurtbox.topleft)
            

engine = Game()
