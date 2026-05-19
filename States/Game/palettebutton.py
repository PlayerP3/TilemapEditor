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
        options_attributes["win_pos"] = [200,125]
        self.paletteUpButton.init(attributes=options_attributes)

        self.paletteDownButton = Option()
        options_attributes["rect_colour"] = 'blue'
        options_attributes["img_path"] = 'Down'
        options_attributes["win_pos"] = [400,125]
        self.paletteDownButton.init(attributes=options_attributes)


        # actual palette options
        # palette choices
        sprites = '/Users/Player3/Desktop/Zombies/Sprites'
        spritesPath = [x[0].replace("\\",'/') for x in os.walk(sprites)]
        self.spritesOptions = []

        for i in range(len(spritesPath)):

            x = gameScreen.windows['palette'].win.get_width() //2
            y = (i*100) + 50

            optionsobj = Option()
            options_attributes['img_path'] = spritesPath[i].split('/')[-1]
            options_attributes['win_pos'] = [x,y]
            options_attributes['name'] = spritesPath[i]

            optionsobj.init(attributes=options_attributes)

            self.spritesOptions.append(optionsobj)


        State.__init__(self)

    def enter(self):

        gameScreen.windows['palette'].focus = (gameScreen.windows['palette'].win.get_width()//2,gameScreen.windows['palette'].win.get_height()//2)

    def update(self):
        
        self.submit_event_processing()

        # camera tracking
        gameScreen.windows['palette'].track_position()

        mousePos = pygame.mouse.get_pos()

        adjustedmousePos = (mousePos[0] - (gameScreen.fullscreen_width - gameScreen.windows['palettebuttons'].hurtbox.width), mousePos[1] - (gameScreen.fullscreen_height -gameScreen.windows['palettebuttons'].hurtbox.height)) 

        # fill window
        # self.parent_node.windows.win.fill((200,0,0))
        # gameScreen.windows['mainwindow'].win.fill((200,0,0))

        # draw tilemap
        gameScreen.windows['tilemap'].win.fill((200,100,100))

        # draw palette
        gameScreen.windows['palette'].win.fill((0,100,100))
        for opt in self.spritesOptions:
            opt.update(surface_to_draw_on='palette')

        # draw tilemap buttons
        gameScreen.windows['tilemapbuttons'].win.fill((150,222,10))

        # draw palette buttons
        gameScreen.windows['palettebuttons'].win.fill((233,10,200))
        self.paletteUpButton.update(surface_to_draw_on='palettebuttons')
        self.paletteDownButton.update(surface_to_draw_on='palettebuttons')
        

        # collision check with buttons
        if self.paletteUpButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Up'

        if self.paletteDownButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Down'
            
        # check which window the mouse is colliding with
        # use that windows offset value for a new mouse position

        # # engine.camera.track_position(window=engine.windows.win)
        # # self.parent_node.camera.focus = self.parent_node.player.hurtbox.center
        # # self.parent_node.camera.track_object_spring(window=self.parent_node.windows.win)

        # # run game object behaviour
        # self.parent_node.update_game_objects()

        # # draw all objects onto the window
        # self.parent_node.draw_objects()

        # find new mouse pos
        

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


         # handling mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == pygame.BUTTON_LEFT:
                
                if self.current_choice == 'Up':

                    gameScreen.windows['palette'].focus = (gameScreen.windows['palette'].focus[0],gameScreen.windows['palette'].focus[1]-200)                  

