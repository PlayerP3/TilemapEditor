
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

    while engine.drawing:

        engine.update()
       
      
if __name__ == '__main__':

    run()
