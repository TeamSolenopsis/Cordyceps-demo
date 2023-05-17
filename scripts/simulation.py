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

def Position(x, y):
    xOffset = 960
    yOffset = 540
    return (x + xOffset, y + yOffset)

def InitEnv():
    pygame.init()
    dims = (1080, 1920)
    env = Environment(dims, 'images/gradient_background.jpeg')
    return env

def FourRobotsEnv():
    env = InitEnv()

    env.addRobot(Position(50,50), robotImage)
    env.addRobot(Position(-50,50), robotImage)
    
    env.addRobot(Position(-50,-50), robotImage)
    env.addRobot(Position(50,-50), robotImage)
    env.addBox(Position(0,0), 'images/box_1.png')
    running = True
    return running, env


if __name__ == "__main__":
    r = 300
    target = Position(300, 0)
    running, env = FourRobotsEnv()    

    while running:
        Poses,x,y,angle= Controller()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        for i,Pose in enumerate(Poses):
            env.setManualPose(Pose,Position(x[i] + 190,y[i]),angle[i])
            env.move_box(target)

        r += 50
        if r == 500:
            running = False