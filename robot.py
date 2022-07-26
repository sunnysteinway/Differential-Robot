import pygame
import math

CONSTANT = 3779.52

class Robot:

    def __init__(self, start_pos, robot_img, width) -> None:

        # conversion constant from meter per second to pixel per second
        self.m2p = 3779.52

        # the configuration of the robot
        self.w = width
        self.pedal = 0
        self.MAX_PEDAL = 100
        self.steering = 0
        self.vl = 0.0005 * self.m2p   # the velocity of the left wheel
        self.vr = 0.0005 * self.m2p   # the velocity of the right wheel

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

    def __engine(self):

        MAX_SPEED = 20
        MIN_SPEED = -15

        if self.vl >= MAX_SPEED:
            self.vl = MAX_SPEED
        elif self.vl < MIN_SPEED:
            self.vl = MIN_SPEED

        if self.vr >= MAX_SPEED:
            self.vr = MAX_SPEED
        elif self.vr < MIN_SPEED:
            self.vr = MIN_SPEED

    def __kinematics(self, dt):
        '''
        Update the kinematics of the robot
        '''
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
                    self.pedal = min(self.pedal, 10)
                    self.vl += 0.1 * self.pedal
                    self.vr += 0.1 * self.pedal

                elif event.key == pygame.K_s:
                    self.pedal -= 1
                    self.pedal = max(self.pedal, 0)
                    self.vl -= 0.1 * self.pedal
                    self.vr -= 0.1 * self.pedal

                elif event.key == pygame.K_a:
                    self.vr += 0.05
                    self.vl -= 0.05
                elif event.key == pygame.K_d:
                    self.vr -= 0.05
                    self.vl += 0.05

                elif event.key == pygame.K_SPACE:
                    self.vl = self.vr = self.pedal = 0

                elif event.key == pygame.K_KP4:
                    self.vl += 0.0005 * CONSTANT # '4' on the keypad
                elif event.key == pygame.K_KP1:
                    self.vl -= 0.0005 * CONSTANT # '1' on the keypad
                elif event.key == pygame.K_KP6:
                    self.vr += 0.0005 * CONSTANT # '6' on the keypad
                elif event.key == pygame.K_KP3:
                    self.vr -= 0.0005 * CONSTANT # '3' on the keypad

        self.__engine()

        # update the position of the robot
        self.__kinematics(dt)

        # update the image of the robot
        self.rotated = pygame.transform.rotozoom(self.img, math.degrees(self.theta), scale=1)

        # update the center point of the robot
        self.rect = self.rotated.get_rect(center=(self.x, self.y))
