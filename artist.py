import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
pygame.font.init()
from screen import gameScreen

class Artist():

    def __init__(self):

        self.drawing_queue = {}

        self.pen = pygame.sysfont.SysFont("Arial",10)
        self.damage_number_pen = pygame.sysfont.SysFont("Arial",24)

        pass


    # function that handless all drawing
    def draw_objects(self):

        # Z layer list
        # Zombies - 0
        # Boss - 1
        # Boss Projectile - 2
        # Boss Orbital - 3
        # Player - 4
        # Player Projectile - 5
        # Player Orbital - 6
        # Danage Numbers - 7

        # this allows us to resolve z layers
        # meaning if there are multiple of a game object type on a layer
        # we refer to this to see what gets drawn first
        GameObjectPriority = {'Enemy':0,
                            'Player':0,
                            'Boss':0,
                            'Bullet':1,
                            'Orbital':2,
                            'DamageNumbers':3}
        
        # get all different surfaces that could be drawn on, always put winas the last
        surfs = list(set([drawinstruc['surface_to_draw_on'] for objid,drawinstruc in self.drawing_queue.items()]))

        # if self.windows.win in surfs:
        #     surfs.remove(self.windows.win)
        #     surfs.append(self.windows.win)

        # go through each surface
        for surf in surfs:

            # create dictionary with only items that will be drawn on that surface
            specific_drawing_queue = dict(filter(lambda item: self.drawing_queue[item[0]]['surface_to_draw_on'] == surf, self.drawing_queue.items()))

            # sort drawing queue based on z layer
            # ZlayerSortedDrawingQueue = sorted(Creative_Mode.drawing_queue,key=lambda id:Creative_Mode.drawing_queue[id]['z_layer'],reverse=True)
            ZlayerSortedDrawingQueue = dict(sorted(specific_drawing_queue.items(),key=lambda x:self.drawing_queue[x[0]]['z_layer'],reverse=False))

            # for unique_id in Creative_Mode.drawing_queue:
            for unique_id in ZlayerSortedDrawingQueue:

                # print(ZlayerSortedDrawingQueue['key'])

                # if what we are drawing is going to be a surface
                if ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'surface':

                    adjusted_position = (0,0)

                    if not ZlayerSortedDrawingQueue[unique_id]['ignore_offset']:
                        adjusted_position = (ZlayerSortedDrawingQueue[unique_id]['position_rect'].x + gameScreen.windows[surf].bg_offset_x, ZlayerSortedDrawingQueue[unique_id]['position_rect'].y +  gameScreen.windows[surf].bg_offset_y)

                    elif ZlayerSortedDrawingQueue[unique_id]['ignore_offset']:
                        adjusted_position = (ZlayerSortedDrawingQueue[unique_id]['position_rect'].x +  gameScreen.windows[surf].win.get_width()//2, ZlayerSortedDrawingQueue[unique_id]['position_rect'].y +  gameScreen.windows[surf].win.get_height()//2)



                    if ZlayerSortedDrawingQueue[unique_id]['alpha'] != -1:
                    
                        ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].set_alpha(ZlayerSortedDrawingQueue[unique_id]['alpha'])


                    # print(adjusted_position)
                    # print(surf)
                    # sys.exit()
                    # adjusted_position = (int(adjusted_position[0]),int(adjusted_position[1]))
                    gameScreen.windows[surf].win.blit(ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'],adjusted_position)


                # if what we are drawing is going to be a rect
                elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'rect':

                    adjusted_position_rect = pygame.FRect(ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].x + gameScreen.windows[surf].bg_offset_x,
                    ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].y +  gameScreen.windows[surf].bg_offset_y,
                    ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].width,
                    ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].height)

                    # draw rects
                    pygame.draw.rect(gameScreen.windows[surf].win,ZlayerSortedDrawingQueue[unique_id]['rect_colour'],adjusted_position_rect,1)

                # if what we are drawing is going to be a surface
                elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'circle':

                    # if inactive schedule deletion
                    if not ZlayerSortedDrawingQueue[unique_id]['game_object'].is_active:
                        ZlayerSortedDrawingQueue[unique_id]['schedule_deletion'] = True
                    # draw rects
                    pygame.draw.circle(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],'blue',(ZlayerSortedDrawingQueue[unique_id]['game_object'].centerx+self.bg_offset_x,ZlayerSortedDrawingQueue[unique_id]['game_object'].centery+self.bg_offset_y),ZlayerSortedDrawingQueue[unique_id]['radius'],2)

                # if what we are drawing is going to be a surface
                elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'line':

                    adjusted_start =  (ZlayerSortedDrawingQueue[unique_id]['startpos'][0] +  gameScreen.windows[surf].bg_offset_x,ZlayerSortedDrawingQueue[unique_id]['startpos'][1] +  gameScreen.windows[surf].bg_offset_y)
                    adjusted_end = (ZlayerSortedDrawingQueue[unique_id]['endpos'][0] +  gameScreen.windows[surf].bg_offset_x,ZlayerSortedDrawingQueue[unique_id]['endpos'][1] +  gameScreen.windows[surf].bg_offset_y)

                    pygame.draw.line(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],'blue',adjusted_start,adjusted_end)

                # if what we are drawing is going to be a surface
                elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'lines':

                    points = [(p[0] +  gameScreen.windows[surf].bg_offset_x, p[1] +  gameScreen.windows[surf].bg_offset_y) for p in ZlayerSortedDrawingQueue[unique_id]['points']]

                    pygame.draw.lines(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],color='blue',points=points,closed=False)


                # if what we are drawing is going to be a surface
                elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'polygon':

                    adjusted_endpoints = []

                    if not ZlayerSortedDrawingQueue[unique_id]['ignore_offset']:
                        adjusted_endpoints = [(e[0]+  gameScreen.windows[surf].bg_offset_x,e[1]+  gameScreen.windows[surf].bg_offset_y) for e in ZlayerSortedDrawingQueue[unique_id]['endpoints']]

                    elif ZlayerSortedDrawingQueue[unique_id]['ignore_offset']:
                        adjusted_endpoints = [(e[0]+  gameScreen.windows[surf].win.get_width()//2,e[1]+ +  gameScreen.windows[surf].win.get_height()//2) for e in ZlayerSortedDrawingQueue[unique_id]['endpoints']]


                    pygame.draw.polygon(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],(255,255,255),adjusted_endpoints)



        self.drawing_queue = {k:self.drawing_queue[k] for k in self.drawing_queue if not self.drawing_queue[k]['schedule_deletion']}


renderer = Artist()