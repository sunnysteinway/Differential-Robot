from tkinter import LEFT
import pygame
import math

CONSTANT = 3779.52
# the maximum and the minimum speed of the robot
MAX_SPEED = 30
MIN_SPEED = -10

# the left and the right limit of the steering wheel of the robot
LEFT_LIMIT = -270
RIGHT_LIMIT = 270

class Robot:

    def __init__(self, start_pos, robot_img, width) -> None:

        # conversion constant from meter per second to pixel per second
        self.m2p = 3779.52

        # the configuration of the robot
        self.w = width
        self.pedal = 0
        self.steering = 0
        self.vl = 0   # the velocity of the left wheel
        self.vr = 0   # the velocity of the right wheel

        # initialization
        self.x, self.y = start_pos
        self.theta = 0
        self.img = pygame.image.load(robot_img) # the original image
        self.rotated = self.img    # we do not want to tamper the original image when we rotate the image, thus we always use the copy of the original
        self.rect = self.rotated.get_rect(center=(self.x, self.y))

    def draw_robot(self, map):
        '''
        Draw the robot to the screen
        '''
        map.blit(self.rotated, self.rect)

    def __steering_wheel(self):

        last_steering = 0

        if self.steering == 0:
            self.vl = (self.vr + self.vl) / 2
            self.vr = self.vl
        elif self.steering == last_steering:
            self.vl += self.steering * 0.0007
            self.vr += self.steering * 0.0007
        else:
            if self.steering > RIGHT_LIMIT:
                self.steering = RIGHT_LIMIT
            
            elif self.steering < LEFT_LIMIT:
                self.steering = LEFT_LIMIT
            
            # adjust the speed of the right and left wheel based on the steering wheel
            self.vl += self.steering * 0.0001
            self.vr -= self.steering * 0.0001

        last_steering = self.steering

    def __engine(self, dt):
        '''
        The physics of the engine
        '''
        # adjust the speed based on the pedal
        self.vl += self.pedal * dt * 0.5
        self.vr += self.pedal * dt * 0.5

        if self.vl > MAX_SPEED:
            self.vl = MAX_SPEED
        elif self.vl < MIN_SPEED:
            self.vl = MIN_SPEED

        if self.vr > MAX_SPEED:
            self.vr = MAX_SPEED
        elif self.vr < MIN_SPEED:
            self.vr = MIN_SPEED

    def __kinematics(self, dt):
        '''
        Update the kinematics of the robot
        '''
        # the speed may be slow down due to the friction
        if self.vr > 0 and self.vl > 0:
            self.vl -= 0.23 * self.vl * dt
            self.vr -= 0.23 * self.vr * dt
        elif self.pedal >= 0:
            self.vl = self.vr = 0

        # update the position (world frame)
        self.x += ((self.vl + self.vr) / 2) * math.cos(self.theta) * dt
        self.y -= ((self.vl + self.vr) / 2) * math.sin(self.theta) * dt
        self.theta += (-self.vl + self.vr) / self.w * dt
        self.theta %= 2 * math.pi   # we only want the value of the theta lies between 0 and 360

    def move_robot(self, event=None, dt=0):

        if event is not None:

            if event.type == pygame.KEYDOWN:

                # find which key is pressed
                if event.key == pygame.K_w:
                    self.pedal += 1
                    self.pedal = min(self.pedal, 15)

                elif event.key == pygame.K_s:
                    self.pedal -= 1
                    self.pedal = max(self.pedal, -1)

                elif event.key == pygame.K_a:
                    self.steering -= 30
                elif event.key == pygame.K_d:
                    self.steering += 30
                elif event.key == pygame.K_SPACE:
                    self.pedal = 0
                    self.vl -= 0.1
                    self.vr -= 0.1
                    
                elif event.key == pygame.K_KP4:
                    self.vl += 0.0005 * CONSTANT # '4' on the keypad
                elif event.key == pygame.K_KP1:
                    self.vl -= 0.0005 * CONSTANT # '1' on the keypad
                elif event.key == pygame.K_KP6:
                    self.vr += 0.0005 * CONSTANT # '6' on the keypad
                elif event.key == pygame.K_KP3:
                    self.vr -= 0.0005 * CONSTANT # '3' on the keypad

        self.__steering_wheel()

        self.__engine(dt)

        # update the position of the robot
        self.__kinematics(dt)

        # update the image of the robot
        self.rotated = pygame.transform.rotozoom(self.img, math.degrees(self.theta), scale=1)

        # update the center point of the robot
        self.rect = self.rotated.get_rect(center=(self.x, self.y))
