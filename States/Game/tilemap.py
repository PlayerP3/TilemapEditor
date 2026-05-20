import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from statemachine import State
from eventsystem import eventprocessor
from artist import renderer
from screen import gameScreen
from options import *
from tiles import Tile,attributes

class Tilemap(State):

    def __init__(self):

        # current choice is what mouse is colliding with 
        self.current_choice = None

        # focus on 0 0
        gameScreen.windows['tilemap'].focus = (0,0)
        gameScreen.windows['tilemap'].track_position()

        self.tiles = []

        # create tiles
        view_rect = pygame.Rect(0,0,3200,3200)
        view_rect.center = (0,0)

        for x in range(view_rect.left,view_rect.right,32):
            for y in range(view_rect.top,view_rect.bottom,32):

                pos = (x,y)

                mytile = Tile()

                attributes['win_pos'] = pos
                attributes["img_path"] = f'({pos[0]},{pos[1]})'
                attributes['sprite_offsetx'] = 16
                attributes['sprite_offsety'] = 16
                mytile.init(attributes=attributes)

                mytile.update(surface_to_draw_on='tilemap')

                self.tiles.append(mytile)

        State.__init__(self)

    def enter(self):
        pass

    def update(self):
        
        self.submit_event_processing()

        # reset choice
        self.current_choice = None

        # camera tracking
        gameScreen.windows['tilemap'].track_position()

        mousePos = pygame.mouse.get_pos()

        adjustedmousePos = (mousePos[0] - gameScreen.windows['tilemap'].bg_offset_x, mousePos[1] - gameScreen.windows['tilemap'].bg_offset_y)

        # fill windows
        gameScreen.windows['tilemap'].win.fill((200,100,100))
        gameScreen.windows['palette'].win.fill((0,100,100))
        gameScreen.windows['tilemapbuttons'].win.fill((150,222,10))
        gameScreen.windows['palettebuttons'].win.fill((233,10,200))

        # draw on windwos
        self.parent_node.states['PALETTEBUTTON'].paletteUpButton.update(surface_to_draw_on='palettebuttons')
        self.parent_node.states['PALETTEBUTTON'].paletteDownButton.update(surface_to_draw_on='palettebuttons')
        self.parent_node.states['PALETTEBUTTON'].paletteDirButton.update(surface_to_draw_on='palettebuttons')
        self.parent_node.states['PALETTEBUTTON'].paletteSpritesButton.update(surface_to_draw_on='palettebuttons')
        
        # draw palette based on what we are showing
        # if current display is dirs
        if self.parent_node.states['PALETTE'].currentDisplay == 'Dirs': 
            for opt in self.parent_node.states['PALETTE'].myDirsOptions:
                opt.update(surface_to_draw_on='palette')
     
        elif self.parent_node.states['PALETTE'].currentDisplay == 'Sprites':
            for opt in self.parent_node.states['PALETTE'].spriteOptions[self.parent_node.states['PALETTE'].currentDir]:
                opt.update(surface_to_draw_on='palette')

        # draw rects on tilemap
        for tile in self.tiles:
            tile.update(surface_to_draw_on='tilemap')

        # draw tilemap buttons
        self.parent_node.states['TILEMAPBUTTON'].UpButton.update(surface_to_draw_on='tilemapbuttons')
        self.parent_node.states['TILEMAPBUTTON'].DownButton.update(surface_to_draw_on='tilemapbuttons')
        self.parent_node.states['TILEMAPBUTTON'].LeftButton.update(surface_to_draw_on='tilemapbuttons')
        self.parent_node.states['TILEMAPBUTTON'].RightButton.update(surface_to_draw_on='tilemapbuttons')

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

            if event.key == pygame.K_ESCAPE:
                self.emit('QUIT')



        # handling mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == pygame.BUTTON_LEFT:
                
                if self.current_choice == 'Down':

                    gameScreen.windows['palette'].focus = (gameScreen.windows['palette'].focus[0],gameScreen.windows['palette'].focus[1]+200)


                elif self.current_choice == 'Up':

                    gameScreen.windows['palette'].focus = (gameScreen.windows['palette'].focus[0],gameScreen.windows['palette'].focus[1]-200)         


                elif self.current_choice == 'Dir':

                    self.parent_node.states['PALETTE'].currentDisplay = 'Dirs'

                    gameScreen.windows['palette'].focus = (gameScreen.windows['palette'].win.get_width()//2,gameScreen.windows['palette'].win.get_height()//2)

                elif self.current_choice == 'Sprites':

                    self.parent_node.states['PALETTE'].currentDisplay = 'Sprites'         

                    gameScreen.windows['palette'].focus = (gameScreen.windows['palette'].win.get_width()//2,gameScreen.windows['palette'].win.get_height()//2)
