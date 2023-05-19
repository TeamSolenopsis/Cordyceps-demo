import pygame
import math
import numpy as np
from constants import *
from box import Box
from robot import Robot
import controller

class Environment(pygame.sprite.Sprite):
    def __init__(self, dimensions, mapImg):
        pygame.sprite.Sprite.__init__(self)
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.green = (0,255,0)
        self.blue = (0,0,255)
        self.red = (255,0,0)
        self.yellow = (255,255,0)
        self.height = dimensions[0]
        self.width = dimensions[1]
        pygame.display.set_caption("env")
        self.map = pygame.display.set_mode((self.width, self.height))

        self.image = pygame.image.load(mapImg)
        self.rect = self.image.get_rect()


        self.mask_image = self.image.convert()
        self.mask_image.set_colorkey((0,0,0))
        self.mask = pygame.mask.from_surface(self.mask_image)
        self.mask.invert()

        self.map.blit(self.image, self.rect)
        self.robots = []
        self.boxes = []
        self.path = []

        self.trails = []
        self.colors = [self.red, self.green,self.blue, self.yellow]
        self.trail_length = 400
        self.trail_draw_interval = 20
        self.trail_point_size = 3

    def addRobot(self, position, imagePath):
        self.robots.append(Robot(position, imagePath))

    def addBox(self, position, imagePath):
        self.boxes.append(Box(position, imagePath))


    def refresh(self):
        pygame.event.get()
        self.map.blit(self.image, self.rect)
        for robot in self.robots:
            robot.draw(self)
        for robot in self.robots:
            robot.scan(self)
        for robot in self.robots:
            robot.drawRays(self)

        for box in self.boxes:
            box.draw(self)

        self.draw_trail(self.trails)



        ## Lines
            # pygame.draw.line(self.map, self.red, (self.robots[0].x,self.robots[0].y), (self.robots[1].x,self.robots[1].y))
            # pygame.draw.line(self.map, self.red, (self.robots[1].x,self.robots[1].y), (self.robots[2].x,self.robots[2].y))
            # pygame.draw.line(self.map, self.red, (self.robots[2].x,self.robots[2].y), (self.robots[3].x,self.robots[3].y))
            # pygame.draw.line(self.map, self.red, (self.robots[0].x,self.robots[0].y), (self.robots[3].x,self.robots[3].y))

    def add_trail(self, trail):
        self.trails.insert(0, trail)
        if(len(self.trails) > self.trail_length):
            self.trails.pop(-1)
    
    def clear_trail(self):
        self.trails = []

    def draw_trail(self, trail):
        for pose_index, poses in enumerate(trail):
            if pose_index % self.trail_draw_interval == 0:
                for i, point in enumerate(poses):
                    pygame.draw.rect(self.map,self.colors[i%4],(point[0], point[1], self.trail_point_size, self.trail_point_size),width=5) 

    def move_box(self, target):
        result = False
        while result != True:
            result = self.boxes[0].move_box_to_position(target)
            self.refresh()
            pygame.display.update()
        return result

    def checkCollision(self):
        collisionrects = []
        index = 0
        for idx, robot in enumerate(self.robots):
            collisionrects.append(robot.rect.inflate(100,100))
            if self.mask.overlap(robot.mask, (robot.x, robot.y)):
                return True

        for i in range(len(collisionrects)):
            for j in range(i+1, len(collisionrects)):
                if collisionrects[i].colliderect(collisionrects[j]):
                    pass
                    return True
        return False      

    def step(self, velocitiesArray):
        counter = 0
        for robot in self.robots:
            robot.move(velocitiesArray[counter][0], velocitiesArray[counter][1], velocitiesArray[counter][2])
            counter += 1
        terminating = self.checkCollision()
        pygame.display.update()
        self.refresh()
        return terminating
    
    def setManualPose(self, pose, box_pose, angle):
        counter = 0
        for robot in self.robots:
            try:
                robot.setPose(pose[counter][0], pose[counter][1], pose[counter][2])
            except:
                pass
            counter += 1

        for box in self.boxes:
            try:
                box.setPose(box_pose[0], box_pose[1], angle)
            except:
                pass

        pygame.display.update()
        self.refresh()

    def setManualPose_robot(self, pose):
        counter = 0
        for robot in self.robots:
            try:
                robot.setPose(pose[counter][0], pose[counter][1], pose[counter][2])
            except:
                pass
            counter += 1

        pygame.display.update()
        self.refresh()

    def setManualPose_robot_individual(self, pose, robot_index):
        
        self.robots[robot_index].setPose(pose[robot_index][0], pose[robot_index][1], pose[robot_index][2])

        pygame.display.update()
        self.refresh()