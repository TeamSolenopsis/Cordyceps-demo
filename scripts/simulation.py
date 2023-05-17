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
    env = Environment(dims, 'images\demo_warehouse_2d.jpg')
    return env

def FourRobotsEnv():
    env = InitEnv()

    env.addRobot(Position(50,50), robotImage)
    env.addRobot(Position(-50,50), robotImage)
    
    env.addRobot(Position(-50,-50), robotImage)
    env.addRobot(Position(50,-50), robotImage)
    env.addBox(Position(-1000,380), 'images/box_1.png')
    running = True
    return running, env


if __name__ == "__main__":
    r = 300
    load = True
    running, env = FourRobotsEnv()    

    while running:
        if load == True:
            target = Position(-600, 380)
            result = env.move_box(target)


        if result == True:
            load = False
            Poses,x,y,angle= Controller()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            for i,Pose in enumerate(Poses):
                env.setManualPose(Pose,Position(x[i] + 190,y[i]),angle[i])

            unload = True
            result = False
        
        if unload == True:
            target = Position(1000, -380)
            result = env.move_box(target)

        r += 50
        if r == 500:
            running = False