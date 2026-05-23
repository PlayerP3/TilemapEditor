import pygame,random,os,string,numpy,math,json,copy,ast
from pygame.math import Vector2
from screen import Window
from statemachine import StateMachine
from States.Game.start import Start
from States.Game.quit import Quit
from States.Game.palettebutton import PaletteButton
from States.Game.palette import Palette
from States.Game.tilemap import Tilemap
from States.Game.tilemapbutton import TilemapButton
from States.Game.definingattributes import DefiningAttributes
from animatedsprite import AnimatedSprite

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

        # have tilemap name
        self.tilemap_name = 'tilemap.json'


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
        self.states = {'START':Start(),
                       'QUIT':Quit(),
                       'PALETTEBUTTON':PaletteButton(),
                       'PALETTE':Palette(),
                       'TILEMAP':Tilemap(),
                       'TILEMAPBUTTON':TilemapButton(),
                       'DEFININGATTRIBUTES':DefiningAttributes()}
        
        # set parent node for player states
        for x in self.states:
            self.states[x].parent_node = self
        
        self.state = self.states['START']


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

    def save_tilemap(self):

        with open(f'tilemaps/{self.tilemap_name}', 'w') as f:

            # mycopy = copy.deepcopy(self.tilemap)

            # print(mycopy)
            myCopy = {}


            # store all pos and layers
            layerPos = []

            # store layer and pos as kv pair
            for layer,layerData in self.tilemap.items():

                for pos,metadata in layerData.items():

                    layerPos.append((layer,pos))


            # go through kv pair and remove animated sprite class and ad vars you want
            for lp in layerPos:

                updateJSON = {}

                layer = lp[0]
                pos = lp[1]

                # get sprite obj
                sprite = self.tilemap[layer][pos]['AnimatedSprite']

                # add variables of interest from the animated sprite class, can actuall use getattr to be more efficient and have a list of vars you want
                updateJSON['hurtbox_width'] = sprite.hurtbox.width
                updateJSON['hurtbox_height'] = sprite.hurtbox.height
                updateJSON['direction'] = sprite.direction
                updateJSON['img_path'] = sprite.img_path

                 # start building copy
                if layer not in myCopy:
                    myCopy[layer] = {} 
                
                if pos not in myCopy[layer]:
                    myCopy[layer][pos] = {}

                # add animated sprite info to myCopy
                myCopy[layer][pos]['AnimatedSprite'] = updateJSON

                # add other info from tilemap
                for k,v in self.tilemap[layer][pos].items():

                    if k == 'AnimatedSprite':
                        continue

                    myCopy[layer][pos][k] = v

            json.dump(myCopy, f,indent=4)

    def load_tilemap(self):

        with open(f'tilemaps/{self.tilemap_name}', 'r') as f:
            
            params = json.load(f)
        

        self.tilemap = {}


        # store all pos and layers
        layerPos = []

        # store layer and pos as kv pair
        for layer,layerData in params.items():

            for pos,metadata in layerData.items():

                layerPos.append((layer,pos))

        # go through kv pair and remove animated sprite class and ad vars you want
        for lp in layerPos:

            updateJSON = {}

            layer = lp[0]
            pos = lp[1]

            # get sprite obj
            spriteinit = params[layer][pos]['AnimatedSprite']

            # add variables of interest from the animated sprite class, can actuall use getattr to be more efficient and have a list of vars you want
            sprite = AnimatedSprite()
            for att,val in spriteinit.items():
                setattr(sprite,att,val)

            sprite.surface_to_draw_on = 'tilemap'
            sprite.vertice = 'topleft'
            sprite.hurtbox.topleft = ast.literal_eval(pos)
            sprite.zlayer_drawing = int(layer)

            # start building copy
            if layer not in self.tilemap:
                self.tilemap[layer] = {} 
            
            if pos not in self.tilemap[layer]:
                self.tilemap[layer][pos] = {}


            # now we can delete Animated sprite key val
            del params[layer][pos]['AnimatedSprite']

            # add animated sprite info to myCopy
            self.tilemap[layer][pos] = params[layer][pos]

            self.tilemap[layer][pos]['AnimatedSprite'] = sprite

        
            

engine = Game()
