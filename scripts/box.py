import pygame
import math

class Box(pygame.sprite.Sprite):
    def __init__(self, startPose, imagePath) -> None:
                pygame.sprite.Sprite.__init__(self)
                self.x = startPose[0]
                self.y = startPose[1]
                self.theta = 0
                self.image = pygame.image.load(imagePath)
                self.image = pygame.transform.scale(self.image, (110,110))
                self.rect = self.image.get_rect()
                self.rotated = self.image
                self.rect = self.rotated.get_rect(center = (self.x, self.y))

    def draw(self, map):
        map.map.blit(self.rotated, self.rect)

    def setPose(self, X, Y, Theta):
        self.x = X
        self.y = Y
        self.theta = Theta
        self.rotated = pygame.transform.rotozoom(self.image, math.degrees(self.theta), 1)
        self.rect = self.rotated.get_rect(center = (self.x, self.y))


    def move_box_to_position(self, target):
        if int(self.x) < target[0]:
            self.x += 1
        elif int(self.x) > target[0]:
            self.x -= 1

        if int(self.y) < target[1]:  
            self.y += 1
        elif int(self.y) > target[1]:
            self.y -= 1
            
        self.rect = self.rotated.get_rect(center = (self.x, self.y))

        if int(self.x) == int(target[0]) and int(self.y) == int(target[1]):
            return True
