from entity import Entity

import pygame

class Bullet(Entity):

    img_size_width = 2
    img_size_height = 2
    BULLET_WIDTH = 12
    BULLET_HEIGHT = 12
    BULLET_SPEED = 10

    def __init__(self, x, y, dirX, dirY):
        self.isAlive = True
        self.x = x
        self.y = y
        self.velX = dirX * self.BULLET_SPEED
        self.velY = dirY * self.BULLET_SPEED

    def draw(self, window, img):
        if not self.isAlive:
            return
        sprite = pygame.Surface([self.img_size_width, self.img_size_height])
        sprite.blit(img, (0, 0), (0, 0, self.img_size_width, self.img_size_height))
        sprite.set_colorkey((0, 0, 0))
        sprite = pygame.transform.scale(sprite, (self.BULLET_WIDTH, self.BULLET_HEIGHT))
        window.blit(sprite, (self.x, self.y))
    
    def update(self):
        self.x += self.velX
        self.y += self.velY
    
    def reset(self):
        pass

    def getDimensions(self):
        return self.x, self.y, self.BULLET_WIDTH, self.BULLET_HEIGHT
    