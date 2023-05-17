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

def Position(x, y):
    xOffset = env_width / 2
    yOffset = env_height/ 2
    return (x + xOffset, y + yOffset)

def InitEnv():
    pygame.init()
    dims = (env_height, env_width)
    env = Environment(dims, 'images/demo_warehouse.jpg')
    return env

def FourRobotsEnv():
    env = InitEnv()

    env.addRobot(Position(50,50), robotImage)
    env.addRobot(Position(-50,50), robotImage)
    
    env.addRobot(Position(-50,-50), robotImage)
    env.addRobot(Position(50,-50), robotImage)
    running = True
    return running, env


if __name__ == "__main__":
    r = 0
    
    running, env = FourRobotsEnv()    

    while running:
        Poses = Controller()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for i in Poses:
            env.setManualPose(i)
        r += 50
        if r == 1000:
            running = False