import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from statemachine import State
from eventsystem import eventprocessor
from artist import renderer
from screen import gameScreen
from options import *
from tiles import Tile,attributes
from animatedsprite import AnimatedSprite

class Tilemap(State):

    def __init__(self):

        # current choice is what mouse is colliding with 
        self.currentTilePos = None
        self.currentLayer = 0

        # showing view grid or not
        self.showTileGrid = 1


        # palette buttons
        self.currentLayerText = AnimatedSprite()
        self.currentLayerText.img_path = f'Current Layer = {self.currentLayer}'
        self.currentLayerText.hurtbox.center = [150,125]
        self.currentLayerText.is_text = True
        self.currentLayerText.text_colour = 'blue'
        self.currentLayerText.surface_to_draw_on = 'tilemapbuttons'
        self.currentLayerText.init_sprite()
        

        
        # focus on 0 0
        gameScreen.windows['tilemap'].focus = (0,0)
        gameScreen.windows['tilemap'].track_position()

        self.tiles = []

        # create tiles
        view_rect = pygame.Rect(0,0,1600,1600)
        view_rect.center = (0,0)

        for x in range(view_rect.left,view_rect.right,32):
            for y in range(view_rect.top,view_rect.bottom,32):

                pos = (x,y)

                mytile = Tile()

                attributes['win_pos'] = pos
                attributes["img_path"] = f'({pos[0]},{pos[1]})'
                attributes['sprite_offsetx'] = 16
                attributes['sprite_offsety'] = 16
                attributes['surface_to_draw_on'] = "tilemap"
                mytile.init(attributes=attributes)

                # mytile.update()

                self.tiles.append(mytile)

        State.__init__(self)

    def enter(self):
        self.currentTilePos = None
        pass

    def update(self):
        
        self.submit_event_processing()

        # camera tracking
        gameScreen.windows['tilemap'].track_position()

        mousePos = pygame.mouse.get_pos()
        adjustedmousePos = ((mousePos[0]- gameScreen.windows['tilemap'].bg_offset_x)/gameScreen.windows['tilemap'].zoom, (mousePos[1] - gameScreen.windows['tilemap'].bg_offset_y)/gameScreen.windows['tilemap'].zoom)


        # set currentile pos
        self.currentTilePos = ((adjustedmousePos[0]//32)*32,(adjustedmousePos[1]//32)*32)


        # print(self.currentTilePos)

        # fill windows
        gameScreen.windows['tilemap'].win.fill((200,100,100))
        gameScreen.windows['palette'].win.fill((0,100,100))
        gameScreen.windows['tilemapbuttons'].win.fill((150,222,10))
        gameScreen.windows['palettebuttons'].win.fill((233,10,200))

        # draw on windwos
        self.parent_node.states['PALETTEBUTTON'].paletteUpButton.update()
        self.parent_node.states['PALETTEBUTTON'].paletteDownButton.update()
        self.parent_node.states['PALETTEBUTTON'].paletteDirButton.update()
        self.parent_node.states['PALETTEBUTTON'].paletteSpritesButton.update()
        
        # draw palette based on what we are showing
        # if current display is dirs
        if self.parent_node.states['PALETTE'].currentDisplay == 'Dirs': 
            for opt in self.parent_node.states['PALETTE'].myDirsOptions:
                opt.update()
     
        elif self.parent_node.states['PALETTE'].currentDisplay == 'Sprites':
            for opt in self.parent_node.states['PALETTE'].spriteOptions[self.parent_node.states['PALETTE'].currentDir]:
                opt.update()


        # TILEMAP

        if self.showTileGrid == 1:
            # draw rects on tilemap
            for tile in self.tiles:
                tile.update()

        # draw tilemap so fat
        self.parent_node.draw_tilemap()
   
        # draw current sprite
        self.parent_node.currentSprite.hurtbox.topleft = ((adjustedmousePos[0]//32)*32,(adjustedmousePos[1]//32)*32)
        self.parent_node.currentSprite.draw_surface(position=self.parent_node.currentSprite.hurtbox.topleft)
        


        self.draw_layer_number()
        
        

        # draw tilemap buttons
        self.parent_node.states['TILEMAPBUTTON'].UpButton.update()
        self.parent_node.states['TILEMAPBUTTON'].DownButton.update()
        self.parent_node.states['TILEMAPBUTTON'].LeftButton.update()
        self.parent_node.states['TILEMAPBUTTON'].RightButton.update()

        # render everything
        renderer.draw_objects()


        # blit all wins onto screen
        gameScreen.screen.blit(gameScreen.windows['tilemap'].win,(0,0))
        gameScreen.screen.blit(gameScreen.windows['palette'].win,(1000,0))
        gameScreen.screen.blit(gameScreen.windows['tilemapbuttons'].win,(0,600))
        gameScreen.screen.blit(gameScreen.windows['palettebuttons'].win,(1000,800))

        # scale the window, and blit to display
        # pygame.transform.scale(gameScreen.windows['mainwindow'].win,(gameScreen.fullscreen_width,gameScreen.fullscreen_height),gameScreen.screen)

        # update display
        pygame.display.flip()

        # if in palette button window
        if gameScreen.windows['palette'].hurtbox.collidepoint(mousePos):
            self.emit('PALETTE')

        elif gameScreen.windows['palettebuttons'].hurtbox.collidepoint(mousePos):
            self.emit('PALETTEBUTTON')

        elif gameScreen.windows['tilemapbuttons'].hurtbox.collidepoint(mousePos):
            self.emit('TILEMAPBUTTON')


        # use true mouse pos to check for collision switchj
    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            print(f'Just Pressed {event.unicode}')

            if event.key == pygame.K_ESCAPE:
                self.emit('QUIT')

            if event.key == pygame.K_UP:
                self.currentLayer += 1

            if event.key == pygame.K_DOWN:
                self.currentLayer -= 1

            if event.key == pygame.K_0:
                self.showTileGrid *= -1

            if event.key == pygame.K_r:
                self.parent_node.currentSprite.direction += 90

            if event.key == pygame.K_z:
                gameScreen.windows['tilemap'].zoom += 1

            if event.key == pygame.K_x:
                
                gameScreen.windows['tilemap'].zoom -= 1
                gameScreen.windows['tilemap'].zoom = max(1,gameScreen.windows['tilemap'].zoom)

            if event.key == pygame.K_SPACE:

                # givne layer and pos, if tile placed there 
                if self.currentLayer in self.parent_node.tilemap:

                    if f"{self.currentTilePos}" in self.parent_node.tilemap[self.currentLayer]:

                        self.emit('DEFININGATTRIBUTES')


        # handling mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == pygame.BUTTON_LEFT:
                
                self.add_tile()

            if event.button == pygame.BUTTON_RIGHT:
                
                self.remove_tile()


    
    def add_tile(self):

        if self.currentLayer not in self.parent_node.tilemap:
            self.parent_node.tilemap[self.currentLayer] = {}

        if f"{self.currentTilePos}" not in self.parent_node.tilemap[self.currentLayer]:

            self.parent_node.tilemap[self.currentLayer][f"{self.currentTilePos}"] = {}

        # if there is already a tile at that location
        if self.parent_node.tilemap[self.currentLayer][f"{self.currentTilePos}"]:
            return
        

        # create new obj
        newSprite = AnimatedSprite()

        newSprite.img_path = self.parent_node.currentSprite.img_path
        newSprite.zlayer_drawing = self.currentLayer
        newSprite.vertice = 'topleft'
        newSprite.hurtbox.topleft = self.currentTilePos
        newSprite.direction = self.parent_node.currentSprite.direction
        newSprite.surface_to_draw_on = 'tilemap'

        # add tile and its stats 
        self.parent_node.tilemap[self.currentLayer][f"{self.currentTilePos}"] = {'AnimatedSprite':newSprite,'class':'BgTile'}

    def remove_tile(self):

        if self.currentLayer in self.parent_node.tilemap:
           
            if f"{self.currentTilePos}" in self.parent_node.tilemap[self.currentLayer]:

                # if there is already a tile at that location
                del self.parent_node.tilemap[self.currentLayer][f"{self.currentTilePos}"]
                
            if not self.parent_node.tilemap[self.currentLayer]:
                del self.parent_node.tilemap[self.currentLayer]

    def draw_layer_number(self):
        self.currentLayerText.img_path = f'Current Layer = {self.currentLayer}'
        self.currentLayerText.init_sprite()
        self.currentLayerText.draw_surface(position=self.currentLayerText.hurtbox.center)


    