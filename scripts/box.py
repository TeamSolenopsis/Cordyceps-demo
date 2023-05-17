import pygame

class Box(pygame.sprite.Sprite):
    def __init__(self, startPose, imagePath) -> None:
                pygame.sprite.Sprite.__init__(self)
                self.x = startPose[0]
                self.y = startPose[1]
                self.image = pygame.image.load(imagePath)
                self.image = pygame.transform.scale(self.image, (100,100))
                self.rect = self.image.get_rect()
                self.rotated = self.image
                self.rect = self.rotated.get_rect(center = (self.x, self.y))

    def draw(self, map):
        map.map.blit(self.rotated, self.rect)