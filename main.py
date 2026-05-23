
import pygame,random,json,os
from animatedsprite import AnimatedSprite
pygame.init()
# screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
# win =  pygame.Surface((2400,2200),pygame.SRCALPHA)
import cProfile
import pstats
from game import engine

# set random seed
random.seed()

def run():

    engine.currentSprite = AnimatedSprite()
    engine.currentSprite.vertice = 'topleft'
    engine.currentSprite.surface_to_draw_on = 'tilemap'

    # set random image to current sprite to stop tilemap error before you pick a sprite for the first time
    engine.currentSprite.img_path = engine.states['PALETTE'].spriteOptions[engine.states['PALETTE'].myDirsOptions[0].img_path][0].img_path
    engine.states['PALETTE'].current_choice =  engine.currentSprite.img_path

    while engine.drawing:

        engine.update()
       
      
if __name__ == '__main__':

    run()
