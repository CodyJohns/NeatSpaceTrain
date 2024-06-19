from drawable import Drawable

import pygame

class Shockwave(Drawable):

    FRAME_DELAY = 0
    FRAME_END = 256
    img_size_width = 32
    img_size_height = 32

    def __init__(self, x, y):
        self.isAlive = True
        self.x = x
        self.y = y
        self.frame_size = 0
        self.delay_counter = 0

    def draw(self, window, sheet):
        if not self.isAlive:
            return
        self._update()
        sprite = pygame.Surface([self.img_size_width, self.img_size_height])
        sprite.blit(sheet, (0, 0), (0, 0, self.img_size_width, self.img_size_height))
        sprite.set_colorkey((0, 0, 0))
        sprite = pygame.transform.scale(sprite, (self.img_size_width + self.frame_size, self.img_size_height + self.frame_size))
        window.blit(sprite, (self.x, self.y))

    def _update(self):
        self.delay_counter += 1

        if self.delay_counter > self.FRAME_DELAY:
            self.delay_counter = 0
            self.frame_size += 4

            if self.frame_size >= self.FRAME_END:
                self.isAlive = False