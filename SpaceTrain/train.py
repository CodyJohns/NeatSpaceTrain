import pygame
from entity import Entity

class Train(Entity):

    TRAIN_WIDTH = 332
    TRAIN_HEIGHT = 60
    img_size_width = 83
    img_size_height = 15
    max_frames = 3
    frame_update_delay = 10
    shooting_delay = 12

    def __init__(self, screen_width, screen_height, sprite_img):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = (screen_width - self.TRAIN_WIDTH) / 2
        self.y = (screen_height - self.TRAIN_HEIGHT) / 2
        self.movement_vel = 10
        self.image = sprite_img
        self.frame = 0
        self.frame_update_counter = 0
        self.moving_left = False
        self.moving_right = False
        self.shooting = False
        self.shooting_counter = 0

    def draw(self, window):
        sprite = pygame.Surface([self.img_size_width, self.img_size_height])
        sprite.blit(self.image, (0, 0), (0, self.frame * self.img_size_height, self.img_size_width, self.img_size_height))
        sprite.set_colorkey((0, 0, 0))
        sprite = pygame.transform.scale(sprite, (self.TRAIN_WIDTH, self.TRAIN_HEIGHT))
        window.blit(sprite, (self.x, self.y))
    
    def update(self):
        self._updateFrame()

        if self.moving_left:
            if self.x > 100:
                self.x -= self.movement_vel

        if self.moving_right:
            if self.x < self.screen_width - (100 + self.TRAIN_WIDTH):
                self.x += self.movement_vel

        if self.shooting:
            self.shooting_counter += 1

            if self.shooting_counter >= self.shooting_delay:
                self.shooting_counter = 0
                return True

        return False

    def reset(self):
        self.x = (self.screen_width - self.TRAIN_WIDTH) / 2
        self.y = (self.screen_height - self.TRAIN_HEIGHT) / 2
        self.frame_update_counter = 0
        self.shooting_counter = 0

    def _updateFrame(self):
        self.frame_update_counter += 1

        if self.frame_update_counter >= self.frame_update_delay:
            self.frame_update_counter = 0
            self.frame += 1

            if self.frame >= self.max_frames:
                self.frame = 0

    def getDimensions(self):
        pass