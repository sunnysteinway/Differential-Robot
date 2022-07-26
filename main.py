import pygame

from environment import Environment
from robot import Robot

def main():

    # initialize pygame
    pygame.init()

    # initialization
    start = (200,200)   # the start position
    dims = (1000,1800)
    running = True

    env = Environment(dims)
    rob = Robot(start, 'robot3.png', 30) # the width of the robot is 80 pixels
    # time
    current_time = 0
    previous_time = pygame.time.get_ticks()
    dt = 0  # the elapse time

    while (running):

        for event in pygame.event.get():

            # if the user activate the quit button
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
           
            rob.move_robot(event, dt)
       
        # update the display
        pygame.display.update()
        env.map.fill(env.black) # fill the entire screen with black
        rob.draw_robot(env.map)

        # update the time
        current_time = pygame.time.get_ticks()
        dt = (current_time - previous_time) * 0.001 # convert to second
        previous_time = current_time

        # update the robot
        rob.move_robot(event, dt)
        env.write_info(rob.vl, rob.vr, rob.theta, rob.pedal, rob.steering, rob.x, rob.y)
        env.draw_trail((rob.x, rob.y))
        env.draw_robot_frame((rob.x, rob.y), rob.theta)

if __name__ == "__main__":
    main()
    print("exit")
