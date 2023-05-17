import pygame
import math

class Box(pygame.sprite.Sprite):
    def __init__(self, startPose, imagePath) -> None:
                pygame.sprite.Sprite.__init__(self)
                self.x = startPose[0]
                self.y = startPose[1]
                self.theta = 0
                self.image = pygame.image.load(imagePath)
                self.image = pygame.transform.scale(self.image, (100,100))
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
