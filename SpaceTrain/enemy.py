from entity import Entity

import pygame

class Enemy(Entity):

    ENEMY_TYPE_A = 0
    ENEMY_TYPE_B = 1
    ENEMY_A_SHOOT_DELAY = 20
    ENEMY_B_SHOOT_DELAY = 10
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
        self.shoot_counter = 0

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
        self.shoot_counter += 1

        shoot_delay = self.ENEMY_A_SHOOT_DELAY if self.enemy_type == self.ENEMY_TYPE_A else self.ENEMY_B_SHOOT_DELAY

        if self.shoot_counter > shoot_delay:
            self.shoot_counter = 0
            return True
        else:
            return False
    
    def reset(self):
        pass

    def getDimensions(self):
        return self.x, self.y, self.SPRITE_WIDTH, self.SPRITE_HEIGHT