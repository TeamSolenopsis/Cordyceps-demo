#export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
import pygame
import math
import numpy as np
from constants import *
from environment import Environment
from controller import Controller
import time

robotImage = 'images/robot.png'
metersToPixels = 3779.52
robotwidthPixels = 50
robotWidth = robotwidthPixels / metersToPixels
R = robotWidth
env_width = 1920
env_height = 1080
vs_origin_x = -580
vs_origin_y = 390


def Position(x, y):
    xOffset = env_width / 2
    yOffset = env_height/ 2
    return (x + xOffset, y + yOffset)

def InitEnv():
    pygame.init()
    dims = (env_height, env_width)
    env = Environment(dims, 'images/demo_warehouse_2d.jpg')

    return env

def FourRobotsEnv():
    env = InitEnv()

    env.addRobot(Position(vs_origin_x + 50, vs_origin_y + 50), robotImage)
    env.addRobot(Position(vs_origin_x - 50, vs_origin_y + 50), robotImage)
    
    env.addRobot(Position(vs_origin_x - 50, vs_origin_y - 50), robotImage)
    env.addRobot(Position(vs_origin_x + 50, vs_origin_y - 50), robotImage)

    env.addBox(Position(-1000,vs_origin_y), 'images/box_1.png')

    return env


def main():
    r = 0
    load = True
    running = True
    vs_origin_x = -580
    vs_origin_y = 390
    env = FourRobotsEnv()      
  

    if load == True:
        target = Position(vs_origin_x, vs_origin_y)
        result = env.move_box(target)

    if result == True:
        load = False

        Poses, x, y, angle, vs_origin_x, vs_origin_y = Controller()  
        for i,Pose in enumerate(Poses):
            env.setManualPose(Pose, (x[i] + vs_origin_x, y[i] + vs_origin_y), angle[i])

        unload = True
        result = False
    
    if unload == True:
        target = Position(1200, -390)
        result = env.move_box(target)

        if result == True:
            unload = False

    for i in np.flip(Poses, 0):
        env.setManualPose_robot(i)
        
    time.sleep(2)

if __name__ == "__main__":
    running = True
    while (running):
        main()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        