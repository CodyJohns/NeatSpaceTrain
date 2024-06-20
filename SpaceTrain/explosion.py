from drawable import Drawable

import pygame

class Explosion(Drawable):

    MAX_FRAMES = 7
    FRAME_DELAY = 2
    img_size_width = 32
    img_size_height = 32
    SPRITE_WIDTH = 64
    SPRITE_HEIGHT = 64

    def __init__(self, x, y):
        self.isAlive = True
        self.x = x
        self.y = y
        self.frame = 0
        self.frame_delay_counter = 0

    def draw(self, window, sheet):
        if not self.isAlive:
            return
        self._update()
        sprite = pygame.Surface([self.img_size_width, self.img_size_height])
        sprite.blit(sheet, (0, 0), (self.frame * self.img_size_width, 0, self.img_size_width, self.img_size_height))
        sprite.set_colorkey((0, 0, 0))
        sprite = pygame.transform.scale(sprite, (self.SPRITE_WIDTH, self.SPRITE_HEIGHT))
        window.blit(sprite, (self.x - (self.SPRITE_WIDTH / 2), self.y - (self.SPRITE_HEIGHT / 2)))

    def _update(self):
        self.frame_delay_counter += 1

        if self.frame_delay_counter > self.FRAME_DELAY:
            self.frame_delay_counter = 0
            self.frame += 1

            if self.frame >= self.MAX_FRAMES:
                self.isAlive = False