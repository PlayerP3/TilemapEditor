import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from statemachine import State
from eventsystem import eventprocessor
from artist import renderer
from screen import gameScreen
from options import *
from tiles import Tile,attributes

class TilemapButton(State):

    def __init__(self):

        # current choice is what mouse is colliding with 
        self.current_choice = None

        # palette buttons
        self.LeftButton = Option()
        options_attributes["rect_colour"] = 'red'
        options_attributes["img_path"] = 'Left'
        options_attributes["win_pos"] = [50,50]
        options_attributes['is_text'] = True
        self.LeftButton.init(attributes=options_attributes)

        self.RightButton = Option()
        options_attributes["rect_colour"] = 'blue'
        options_attributes["img_path"] = 'Right'
        options_attributes["win_pos"] = [50,150]
        options_attributes['is_text'] = True
        self.RightButton.init(attributes=options_attributes)


        self.UpButton = Option()
        options_attributes["rect_colour"] = 'red'
        options_attributes["img_path"] = 'Up'
        options_attributes["win_pos"] = [50,250]
        options_attributes['is_text'] = True
        self.UpButton.init(attributes=options_attributes)

        self.DownButton = Option()
        options_attributes["rect_colour"] = 'blue'
        options_attributes["img_path"] = 'Down'
        options_attributes["win_pos"] = [50,350]
        options_attributes['is_text'] = True
        self.DownButton.init(attributes=options_attributes)


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

        adjustedmousePos = (mousePos[0], mousePos[1] - (gameScreen.fullscreen_height -gameScreen.windows['tilemapbuttons'].hurtbox.height)) 

        # fill window
        # self.parent_node.windows.win.fill((200,0,0))
        # gameScreen.windows['mainwindow'].win.fill((200,0,0))


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


        # draw tilemap buttons
        self.UpButton.update(surface_to_draw_on='tilemapbuttons')
        self.DownButton.update(surface_to_draw_on='tilemapbuttons')
        self.LeftButton.update(surface_to_draw_on='tilemapbuttons')
        self.RightButton.update(surface_to_draw_on='tilemapbuttons')


         # collision check with buttons
        if self.UpButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Up'

        elif self.DownButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Down'

        elif self.LeftButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Left'
            
        elif self.RightButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Right'


        # draw tilempa rects
        for tile in self.parent_node.states['TILEMAP'].tiles:
            tile.update(surface_to_draw_on='tilemap')

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

        elif gameScreen.windows['tilemap'].hurtbox.collidepoint(mousePos):
            self.emit('TILEMAP')


        # use true mouse pos to check for collision switchj
    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.emit('QUIT')



        # handling mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == pygame.BUTTON_LEFT:
                
                if self.current_choice == 'Left':

                    gameScreen.windows['tilemap'].focus = (gameScreen.windows['tilemap'].focus[0] - 160,gameScreen.windows['tilemap'].focus[1])


                elif self.current_choice == 'Right':

                    gameScreen.windows['tilemap'].focus = (gameScreen.windows['tilemap'].focus[0] + 160,gameScreen.windows['tilemap'].focus[1])   


                if self.current_choice == 'Up':

                    gameScreen.windows['tilemap'].focus = (gameScreen.windows['tilemap'].focus[0],gameScreen.windows['tilemap'].focus[1] - 160)


                elif self.current_choice == 'Down':

                    gameScreen.windows['tilemap'].focus = (gameScreen.windows['tilemap'].focus[0],gameScreen.windows['tilemap'].focus[1] + 160)      


               