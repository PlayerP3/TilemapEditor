import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from statemachine import State
from eventsystem import eventprocessor
from artist import renderer
from screen import gameScreen
from options import *

class Start(State):

    def __init__(self):

        # current choice is what mouse is colliding with 
        self.current_choice = None
        self.currentAction = 'loadJSON'

        # palette buttons
        self.newButton = Option()
        options_attributes["rect_colour"] = 'red'
        options_attributes["img_path"] = 'New Tilemap'
        options_attributes["win_pos"] = [200,200]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "start"
        self.newButton.init(attributes=options_attributes)

        self.loadButton = Option()
        options_attributes["rect_colour"] = 'red'
        options_attributes["img_path"] = 'Load Tilemap'
        options_attributes["win_pos"] = [200,400]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "start"
        self.loadButton.init(attributes=options_attributes)

        self.closeButton = Option()
        options_attributes["rect_colour"] = 'red'
        options_attributes["img_path"] = 'Close'
        options_attributes["win_pos"] = [200,600]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "start"
        self.closeButton.init(attributes=options_attributes)

        # store current phrase
        self.currentPhrase = Option()
        options_attributes["rect_colour"] = 'red'
        options_attributes["img_path"] = ' '
        options_attributes["win_pos"] = [800,200]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "start"
        self.currentPhrase.penToUse = 'arial20'

        self.currentPhrase.init(attributes=options_attributes)
        self.currentPhrase.img_width_scale = 3
        self.currentPhrase.img_height_scale = 2


        # palette buttons
        self.currentActionText = AnimatedSprite()
        self.currentActionText.img_path = f'Select New Tilemap or Load Tilemap'
        self.currentActionText.hurtbox.center = [800,600]
        self.currentActionText.is_text = True
        self.currentActionText.text_colour = 'blue'
        self.currentActionText.surface_to_draw_on = 'start'
        self.currentActionText.init_sprite()

        # store all json
        self.allJSONS = os.listdir('tilemaps')


        State.__init__(self)

    def enter(self):

        self.currentAction = 'loadJSON'
        self.parent_node.tilemap_name = 'tilemap.json'
        self.parent_node.tilemap = {}
       

    def update(self):
        
        self.submit_event_processing()

        mousePos = pygame.mouse.get_pos()
        adjustedmousePos = ((mousePos[0]- gameScreen.windows['start'].bg_offset_x)/gameScreen.windows['start'].zoom, (mousePos[1] - gameScreen.windows['start'].bg_offset_y)/gameScreen.windows['start'].zoom)

        gameScreen.windows['start'].win.fill((233,10,200))

        # update buttons
        self.loadButton.update()
        self.newButton.update()
        self.closeButton.update()
        self.currentPhrase.update()
        self.draw_current_action()

        

        if self.newButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'New'
            
        if self.loadButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Load'

        if self.closeButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Close'

        # render everything
        renderer.draw_objects()


        # blit all wins onto screen
        gameScreen.screen.blit(gameScreen.windows['start'].win,(0,0))
        
        # update display
        pygame.display.flip()

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            # when hit enter do smth diff dpeending on typing or deleting
            if event.key == pygame.K_RETURN:

                if len(self.currentPhrase.img_path) > 1 and self.currentPhrase.img_path.endswith('.json'):

                    self.process_entry()

            elif event.key == pygame.K_BACKSPACE:
                if len(self.currentPhrase.img_path) > 1:
                    self.currentPhrase.img_path = self.currentPhrase.img_path[:-1]

            else:
                
                self.currentPhrase.img_path += event.unicode


         # handling mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == pygame.BUTTON_LEFT:
                
                if self.current_choice == 'Close':

                    self.emit('QUIT')

                if self.current_choice == 'New':

                    self.currentAction = 'newJSON'

                    # self.emit('TILEMAP')

                if self.current_choice == 'Load':

                    self.currentAction = 'loadJSON'


    
    def process_entry(self): 

        if self.currentAction == 'newJSON':

            self.parent_node.tilemap_name = self.currentPhrase.img_path.lstrip().rstrip() 

            self.currentPhrase.img_path = ' '

            self.emit('TILEMAP')

        elif self.currentAction == 'loadJSON':

            if self.currentPhrase.img_path.lstrip().rstrip() in self.allJSONS:

                self.parent_node.tilemap_name = self.currentPhrase.img_path.lstrip().rstrip() 
                self.currentPhrase.img_path = ' '
                self.parent_node.load_tilemap()
                self.emit('TILEMAP')

    def draw_current_action(self):

        if self.currentAction == 'loadJSON':
            self.currentActionText.img_path = f'You are loading a json'

        if self.currentAction == 'newJSON':
            self.currentActionText.img_path = f'You are creating a new json'

        if not self.currentAction:
            self.currentActionText.img_path = f'You are doing nothing'



        self.currentActionText.init_sprite()
        self.currentActionText.draw_surface(position=self.currentActionText.hurtbox.center)