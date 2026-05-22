import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from statemachine import State
from eventsystem import eventprocessor
from artist import renderer
from screen import gameScreen
from options import *

class DefiningAttributes(State):

    def __init__(self):

        # current choice is what mouse is colliding with 
        self.current_choice = None

        self.typingFor = False


        # store key value pairs
        self.kvPairs = {}

        # store current phrase
        self.currentPhrase = Option()
        options_attributes["rect_colour"] = 'red'
        options_attributes["img_path"] = ' '
        options_attributes["win_pos"] = [800,300]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "defineattributes"
        self.currentPhrase.penToUse = 'arial20'

        self.currentPhrase.init(attributes=options_attributes)
        self.currentPhrase.img_width_scale = 3
        self.currentPhrase.img_height_scale = 2

        # palette buttons
        self.submitButton = Option()
        options_attributes["rect_colour"] = 'red'
        options_attributes["img_path"] = 'Submit'
        options_attributes["win_pos"] = [300,900]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "defineattributes"

        self.submitButton.init(attributes=options_attributes)

        self.viewJSONButton = Option()
        options_attributes["rect_colour"] = 'blue'
        options_attributes["img_path"] = 'ViewJSON'
        options_attributes["win_pos"] = [800,900]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "defineattributes"
        self.viewJSONButton.init(attributes=options_attributes)

        self.closeButton = Option()
        options_attributes["rect_colour"] = 'blue'
        options_attributes["img_path"] = 'Close'
        options_attributes["win_pos"] = [1300,900]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "defineattributes"
        self.closeButton.init(attributes=options_attributes)


        self.keyText = Option()
        options_attributes["rect_colour"] = 'blue'
        options_attributes["img_path"] = 'Key'
        options_attributes["win_pos"] = [400,125]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "defineattributes"
        self.keyText.init(attributes=options_attributes)

        self.valueText = Option()
        options_attributes["rect_colour"] = 'blue'
        options_attributes["img_path"] = 'Value'
        options_attributes["win_pos"] = [1200,125]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "defineattributes"
        self.valueText.init(attributes=options_attributes)

        self.deleteKeyButton = Option()
        options_attributes["rect_colour"] = 'blue'
        options_attributes["img_path"] = 'Delete'
        options_attributes["win_pos"] = [1600,900]
        options_attributes['is_text'] = True
        options_attributes['surface_to_draw_on'] = "defineattributes"
        self.deleteKeyButton.init(attributes=options_attributes)

        State.__init__(self)

    def enter(self):
        self.current_choice = None
        self.typingFor = None
        self.kvPairs = self.parent_node.tilemap[self.parent_node.states['TILEMAP'].currentLayer][f"{self.parent_node.states['TILEMAP'].currentTilePos}"]
        

    def update(self):
        
        self.submit_event_processing()

        # reset choice
        self.current_choice = None

        # camera tracking
        gameScreen.windows['palette'].track_position()

        mousePos = pygame.mouse.get_pos()
        adjustedmousePos = ((mousePos[0]- gameScreen.windows['defineattributes'].bg_offset_x)/gameScreen.windows['defineattributes'].zoom, (mousePos[1] - gameScreen.windows['defineattributes'].bg_offset_y)/gameScreen.windows['defineattributes'].zoom)


        # fill window
        # self.parent_node.windows.win.fill((200,0,0))
        # gameScreen.windows['mainwindow'].win.fill((200,0,0))


        # fill windows
        gameScreen.windows['defineattributes'].win.fill((200,100,100))

        # draw on windwos
        self.submitButton.update()
        self.viewJSONButton.update()
        self.closeButton.update()
        self.valueText.update()
        self.keyText.update()
        self.deleteKeyButton.update()
        self.currentPhrase.update()
        

        # collision check with buttons
        if self.submitButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Submit'

        if self.viewJSONButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'viewJSON'

        if self.closeButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Close'
            
        if self.valueText.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Value'

        if self.keyText.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Key'

        if self.deleteKeyButton.hurtbox.collidepoint(adjustedmousePos):
            self.current_choice = 'Delete'



        # render everything
        renderer.draw_objects()


        # blit all wins onto screen
        gameScreen.screen.blit(gameScreen.windows['defineattributes'].win,(0,0))
     
        # scale the window, and blit to display
        # pygame.transform.scale(gameScreen.windows['mainwindow'].win,(gameScreen.fullscreen_width,gameScreen.fullscreen_height),gameScreen.screen)

        # update display
        pygame.display.flip()


        # use true mouse pos to check for collision switchj
    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:

                if len(self.currentPhrase.img_path) > 1:

                    self.process_entry()

            elif event.key == pygame.K_BACKSPACE:
                if len(self.currentPhrase.img_path) > 1:
                    self.currentPhrase.img_path = self.currentPhrase.img_path[:-1]

            elif self.typingFor:
                
                self.currentPhrase.img_path += event.unicode

        # handling mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == pygame.BUTTON_LEFT:
                
                if self.current_choice == 'Close':

                    self.emit('TILEMAP')

                if self.current_choice == 'Submit':
                    
                    # update json meta data for tile
                    self.parent_node.tilemap[self.parent_node.states['TILEMAP'].currentLayer][f"{self.parent_node.states['TILEMAP'].currentTilePos}"] = self.kvPairs

                    self.emit('TILEMAP')

                if self.current_choice == 'Key':

                    self.typingFor = True

                # if self.current_choice == 'Value':

                #     self.typingFor = 'Value'

    def process_entry(self):

        # split at the colon
        k,v = self.currentPhrase.img_path.split(':',1)

        # processValue
        processedValue = self.processValue(v.lstrip().rstrip())
       
        self.kvPairs[k.lstrip().rstrip()] = processedValue

        self.currentPhrase.img_path = ' '

        print(self.kvPairs)


    def processValue(self,raw):

         # try int
        try:
            return int(raw)
        except ValueError:
            pass
        
        # try float
        try:
            return float(raw)
        except ValueError:
            pass
        
        # try json (for dicts, lists, bools)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass
        
        # fallback, treat as plain string
        return raw

        