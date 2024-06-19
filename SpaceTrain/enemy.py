from entity import Entity

import pygame

class Enemy(Entity):

    ENEMY_TYPE_A = 0
    ENEMY_TYPE_B = 1
    SPRITE_WIDTH = 48
    SPRITE_HEIGHT = 48
    ENEMY_MIN_VEL = 6
    ENEMY_MAX_VEL = 20

    img_size_width = 16
    img_size_height = 16

    def __init__(self, x, y, vel, enemy_type = 0):
        self.isAlive = True
        self.enemy_type = enemy_type
        self.x = x
        self.y = y
        self.vel = vel

    def draw(self, window, img):
        if not self.isAlive:
            return
        sprite = pygame.Surface([self.img_size_width, self.img_size_height])
        sprite.blit(img, (0, 0), (0, 0, self.img_size_width, self.img_size_height))
        sprite.set_colorkey((0, 0, 0))
        sprite = pygame.transform.scale(sprite, (self.SPRITE_WIDTH, self.SPRITE_HEIGHT))
        #depending on velocity direction rotate image
        if self.vel < 0:
            sprite = pygame.transform.rotate(sprite, 180)
        window.blit(sprite, (self.x, self.y))
    
    def update(self):
        self.x += self.vel
    
    def reset(self):
        pass

    def getDimensions(self):
        return self.x, self.y, self.SPRITE_WIDTH, self.SPRITE_HEIGHT