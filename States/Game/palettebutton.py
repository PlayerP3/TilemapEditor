import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from statemachine import State
from eventsystem import eventprocessor
from artist import renderer
from screen import gameScreen
from options import *

class PaletteButton(State):

    def __init__(self):

        # current choice is what mouse is colliding with 
        self.current_choice = None

        # palette buttons
        self.paletteUpButton = Option()
        options_attributes["rect_colour"] = 'red'
        options_attributes["img_path"] = 'Up'
        options_attributes["win_pos"] = [50,125]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "palettebuttons"

        self.paletteUpButton.init(attributes=options_attributes)

        self.paletteDownButton = Option()
        options_attributes["rect_colour"] = 'blue'
        options_attributes["img_path"] = 'Down'
        options_attributes["win_pos"] = [250,125]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "palettebuttons"
        self.paletteDownButton.init(attributes=options_attributes)

        self.paletteDirButton = Option()
        options_attributes["rect_colour"] = 'blue'
        options_attributes["img_path"] = 'Dir'
        options_attributes["win_pos"] = [450,125]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "palettebuttons"
        self.paletteDirButton.init(attributes=options_attributes)


        self.paletteSpritesButton = Option()
        options_attributes["rect_colour"] = 'blue'
        options_attributes["img_path"] = 'Sprites'
        options_attributes["win_pos"] = [650,125]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "palettebuttons"
        self.paletteSpritesButton.init(attributes=options_attributes)



        State.__init__(self)

    def enter(self):
        pass

    def update(self):
        
        self.submit_event_processing()

        # reset choice
        self.current_choice = None

        # camera tracking
        gameScreen.windows['palette'].track_position()

        mousePos = pygame.mouse.get_pos()

        adjustedmousePos = (mousePos[0] - (gameScreen.fullscreen_width - gameScreen.windows['palettebuttons'].hurtbox.width), mousePos[1] - (gameScreen.fullscreen_height -gameScreen.windows['palettebuttons'].hurtbox.height)) 

        # fill window
        # self.parent_node.windows.win.fill((200,0,0))
        # gameScreen.windows['mainwindow'].win.fill((200,0,0))


        # fill windows
        gameScreen.windows['tilemap'].win.fill((200,100,100))
        gameScreen.windows['palette'].win.fill((0,100,100))
        gameScreen.windows['tilemapbuttons'].win.fill((150,222,10))
        gameScreen.windows['palettebuttons'].win.fill((233,10,200))

        # draw on windwos
        self.paletteUpButton.update()
        self.paletteDownButton.update()
        self.paletteDirButton.update()
        self.paletteSpritesButton.update()
        

        # draw palette based on what we are showing
        # if current display is dirs
        if self.parent_node.states['PALETTE'].currentDisplay == 'Dirs':
    
            for opt in self.parent_node.states['PALETTE'].myDirsOptions:
                opt.update()
        
        elif self.parent_node.states['PALETTE'].currentDisplay == 'Sprites':
    
            for opt in self.parent_node.states['PALETTE'].spriteOptions[self.parent_node.states['PALETTE'].currentDir]:
                opt.update()


        # collision check with buttons
        if self.paletteUpButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Up'

        if self.paletteDownButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Down'

        if self.paletteDirButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Dir'
            
        if self.paletteSpritesButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Sprites'


        # draw tilemap buttons
        self.parent_node.states['TILEMAPBUTTON'].UpButton.update()
        self.parent_node.states['TILEMAPBUTTON'].DownButton.update()
        self.parent_node.states['TILEMAPBUTTON'].LeftButton.update()
        self.parent_node.states['TILEMAPBUTTON'].RightButton.update()
        self.parent_node.states['TILEMAPBUTTON'].SaveButton.update()
        self.parent_node.states['TILEMAPBUTTON'].BackButton.update()

        # draw tilempa rects
        for tile in self.parent_node.states['TILEMAP'].tiles:
            tile.update()

        # draw tilemap so fat
        self.parent_node.draw_tilemap()
        
        self.parent_node.states['TILEMAP'].draw_layer_number()

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

        elif gameScreen.windows['tilemap'].hurtbox.collidepoint(mousePos) and self.parent_node.currentSprite:
            self.emit('TILEMAP')

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
