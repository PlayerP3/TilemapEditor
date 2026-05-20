import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from statemachine import State
from eventsystem import eventprocessor
from artist import renderer
from screen import gameScreen
from options import *

class Palette(State):

    def __init__(self):

        # current choice is what mouse is colliding with 
        self.currentChoice = None

        # currentdir
        self.currentDir = 'Hearts'

        # what we are displaying currently
        self.currentDisplay = 'Dirs'

        # palette choices
        myDirs = '/Users/Player3/Desktop/Zombies/Sprites'
        potentialDirsPath = [x[0].replace("\\",'/') for x in os.walk(myDirs)]
        myDirsPath = []

        # filter dirs path to only contain dirs with pngs
        for d in potentialDirsPath:
            if '.png' in ''.join(os.listdir(d)):
                myDirsPath.append(d)

        self.myDirsOptions = []
        self.spriteOptions = {}

        for i in range(len(myDirsPath)):

            x = gameScreen.windows['palette'].win.get_width() //2
            y = (i*100) + 50

            optionsobj = Option()
            options_attributes['img_path'] = myDirsPath[i].split('/')[-1]
            options_attributes['win_pos'] = [x,y]
            options_attributes['name'] = myDirsPath[i]

            optionsobj.init(attributes=options_attributes)

            self.myDirsOptions.append(optionsobj)

            # ceate entry in duct
            self.spriteOptions[myDirsPath[i].split('/')[-1]] = []

            sprites = os.listdir(myDirsPath[i])

            yChange = 0

            # get all sprites in dir 
            for j in range(len(sprites)):

                spritePath = f"{myDirsPath[i]}/{sprites[j]}"

                spriteObj = Option()

                options_attributes['img_path'] = spritePath
                options_attributes['win_pos'] = [0 + (100*j) , 30 + (yChange*40)]
                options_attributes['name'] = sprites[j]

                # spriteObj.init(attributes=options_attributes)
                self.spriteOptions[myDirsPath[i].split('/')[-1]].append(spriteObj)

                # if we have six elements on the line then start drawing on the next one
                if j%6 == 0:
                    yChange += 1

        gameScreen.windows['palette'].focus = (gameScreen.windows['palette'].win.get_width()//2,gameScreen.windows['palette'].win.get_height()//2)

        State.__init__(self)

    def enter(self):

        pass
        # 

    def update(self):
        
        self.submit_event_processing()

        # reset choice
        self.currentChoice = None

        # camera tracking
        gameScreen.windows['palette'].track_position()

        mousePos = pygame.mouse.get_pos()

        adjustedmousePos = (mousePos[0] - (gameScreen.fullscreen_width - gameScreen.windows['palette'].hurtbox.width) - gameScreen.windows['palette'].bg_offset_x, mousePos[1] -gameScreen.windows['palette'].bg_offset_y) 

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

        # if current display is dirs
        if self.currentDisplay == 'Dirs':
    
            for opt in self.myDirsOptions:
                opt.update(surface_to_draw_on='palette')

                if opt.hurtbox.collidepoint(adjustedmousePos):
                    self.currentChoice = opt.name

                    print(opt.name)
                    print(adjustedmousePos)
                    print(opt.hurtbox.center)
                    sys.exit()
                    

        # if current display is dirs
        elif self.currentDisplay == 'Sprites':
    
            for opt in self.spritesOptions:
                opt.update(surface_to_draw_on='palette')

                if opt.hurtbox.collidepoint(adjustedmousePos):
                    self.currentChoice = opt.name


        # render everything
        renderer.draw_objects()


        # blit all wins onto screen
        gameScreen.screen.blit(gameScreen.windows['tilemap'].win,(0,0))
        gameScreen.screen.blit(gameScreen.windows['palette'].win,(1000,0))
        gameScreen.screen.blit(gameScreen.windows['tilemapbuttons'].win,(0,600))
        gameScreen.screen.blit(gameScreen.windows['palettebuttons'].win,(1000,800))

        # update display
        pygame.display.flip()

        # if in palette button window
        if gameScreen.windows['palettebuttons'].hurtbox.collidepoint(mousePos):
            self.emit('PALETTEBUTTON')


        # use true mouse pos to check for collision switchj
    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.emit('QUIT')



        # handling mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == pygame.BUTTON_LEFT:

                if self.currentChoice:
                
                    if self.currentDisplay == 'Dirs':

                        print(self.currentChoice)
                        sys.exit()
