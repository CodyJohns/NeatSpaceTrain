from entity import Entity

import pygame

class Bar(Entity):

    BAR_WIDTH = 48
    BAR_MAX_VEL = 48
    BAR_ACC_DELAY = 20

    def __init__(self, screen_width, screen_height, img):
        self.img = img
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = screen_width + self.BAR_WIDTH
        self.bar_vel = 1
        self.bar_acc_counter = 0

    def draw(self, window):
        sprite = pygame.Surface([2, 2])
        sprite.blit(self.img, (0, 0), (0, 0, 2, 2))
        sprite.set_colorkey((0, 0, 0))
        sprite = pygame.transform.scale(sprite, (self.BAR_WIDTH, self.screen_height * 2))
        window.blit(sprite, (self.x, 0))

    def update(self):
        if self.bar_vel < self.BAR_MAX_VEL:
            self.bar_acc_counter += 1

            if self.bar_acc_counter > self.BAR_ACC_DELAY:
                self.bar_vel *= 2
        
        self.x -= self.bar_vel

        if self.x < -self.BAR_WIDTH:
            self.x = self.screen_width + self.BAR_WIDTH
    
    def reset(self):
        self.x = self.screen_width + self.BAR_WIDTH
        self.bar_vel = 1
        self.bar_acc_counter = 0

    def getDimensions(self):
        pass