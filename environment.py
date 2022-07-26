import pygame
import math

CONSTANT = 3779.52

class Environment:
    def __init__(self, dimensions) -> None:

        # colours
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.lime = (0,255,0)
        self.blue = (0,0,255)
        self.yellow = (255,255,0)
        self.orange = (255,69,0)
        self.sky = (0,191,255)
        self.peru = (205,133,63)
        self.steel = (176,196,222)
       
        # the dimensions of the map
        self.height = dimensions[0]
        self.width = dimensions[1]

        # pygame windows settings
        pygame.display.set_caption("Differential Drive Car")
        self.map = pygame.display.set_mode((self.width, self.height))

        self.font = pygame.font.Font('freesansbold.ttf', 20)

        self.txt = self.font.render('default', True, self.white, self.lime)
        self.text_rect = self.txt.get_rect()
        self.text_rect.center = (dimensions[1] - 600, dimensions[0] - 100)

        self.dashboard = self.font.render('defualt', True, self.orange, self.sky)
        self.dashboard_rect = self.dashboard.get_rect()
        self.dashboard_rect.center = (dimensions[1] - 600, dimensions[0] - 200)

        self.gps = self.font.render('defualt', True, self.steel, self.peru)
        self.gps_rect = self.gps.get_rect()
        self.gps_rect.center = (dimensions[1] - 600, dimensions[0] - 300)

        # a list that holds the trail of the robot
        self.trail_list = []
   
    def write_info(self, vl, vr, theta, pedal, steering, x, y):
        '''
        Write the info of the robot
        '''
        txt = f"VL: {vl:.1f}  VR: {vr:.1f}  theta: {math.degrees(theta):.1f}"
        self.txt = self.font.render(txt, True, self.white, self.lime)
        self.map.blit(self.txt, self.text_rect)

        dashboard_info = f"pedal: {pedal}  steering: {steering}"
        self.dashboard = self.font.render(dashboard_info, True, self.orange, self.sky)
        self.map.blit(self.dashboard, self.dashboard_rect)

        gps_info = f"x: {x:.2f}  y: {y:.2f}"
        self.gps = self.font.render(gps_info, True, self.steel, self.peru)
        self.map.blit(self.gps, self.gps_rect)

    def draw_trail(self, pos):
        '''
        Draw the trail of the robot
        '''

        # draw the line of the trail from the list
        for i in range(0, len(self.trail_list) - 1):
            pygame.draw.line(self.map, self.yellow, (self.trail_list[i][0], self.trail_list[i][1]),
            (self.trail_list[i + 1][0], self.trail_list[i + 1][1]))

        # check if the size excess
        if self.trail_list.__sizeof__() > 15000:
            self.trail_list.pop(0)
       
        # update the trail set with the new position
        self.trail_list.append(pos)
   
    def draw_robot_frame(self, pos, rotation):
        '''
        Draw the frame of the robot
        '''

        # the length of the lines
        n = 35

        # the center of the robot
        centerX, centerY = pos

        # calculate the endpoints of the axes
        axisX = centerX + n * math.cos(-rotation), centerY + n * math.sin(-rotation)
        axisY = centerX + n * math.cos(-rotation + math.pi / 2), centerY + n * math.sin(-rotation + math.pi / 2)

        pygame.draw.line(self.map, self.red, (centerX, centerY), axisX, width=3)
        pygame.draw.line(self.map, self.lime, (centerX, centerY), axisY, width=3)
