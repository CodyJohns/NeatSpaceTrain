import pygame
import math

from entity import Entity

class Train(Entity):

    TRAIN_WIDTH = 332
    TRAIN_HEIGHT = 60
    img_size_width = 83
    img_size_height = 15
    max_frames = 3
    frame_update_delay = 10
    shooting_delay = 24 #change back to 12

    def __init__(self, gameInstance, screen_width, screen_height, sprite_img, turret_img):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = (screen_width - self.TRAIN_WIDTH) / 2
        self.y = (screen_height - self.TRAIN_HEIGHT) / 2
        self.movement_vel = 10
        self.image = sprite_img
        self.turret_img = turret_img
        self.frame = 0
        self.frame_update_counter = 0
        self.moving_left = False
        self.moving_right = False
        self.shooting = False
        self.shooting_counter = 0
        self.top_angle = 180
        self.bottom_angle = 0
        self.health = 100
        self.gameInstance = gameInstance

    def draw(self, window):
        mousePos = self.gameInstance.mousePos if self.gameInstance.ai else pygame.mouse.get_pos()

        sprite = pygame.Surface([self.img_size_width, self.img_size_height])
        sprite.blit(self.image, (0, 0), (0, self.frame * self.img_size_height, self.img_size_width, self.img_size_height))
        sprite.set_colorkey((0, 0, 0))

        sprite = pygame.transform.scale(sprite, (self.TRAIN_WIDTH, self.TRAIN_HEIGHT))

        window.blit(sprite, (self.x, self.y))

        if mousePos[1] < self.y + 30:
            self.top_angle = int(self._turretAngle(self.x, self.y, mousePos))
        else:
            self.bottom_angle = int(self._turretAngle(self.x, self.y + 60, mousePos))

        turret1 = pygame.transform.scale_by(self.turret_img, 3)
        turret1 = pygame.transform.rotate(turret1, self.top_angle - 90)
        turret1.set_colorkey((0, 0, 0))

        tw = turret1.get_width()
        th = turret1.get_height()

        window.blit(turret1, (self.x + (self.TRAIN_WIDTH / 2) - (tw / 2), self.y - (th / 2)))

        turret2 = pygame.transform.scale_by(self.turret_img, 3)
        turret2 = pygame.transform.rotate(turret2, self.bottom_angle - 90)
        turret2.set_colorkey((0, 0, 0))

        tw = turret2.get_width()
        th = turret2.get_height()

        window.blit(turret2, (self.x + (self.TRAIN_WIDTH / 2) - (tw / 2), self.y - (th / 2) + 60))

    def _turretAngle(self, x, y, mousePos):
        return math.atan2(mousePos[0] - (x + (self.TRAIN_WIDTH / 2)), mousePos[1] - y) * (180 / math.pi)
    
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
        self.health = 100

    def _updateFrame(self):
        self.frame_update_counter += 1

        if self.frame_update_counter >= self.frame_update_delay:
            self.frame_update_counter = 0
            self.frame += 1

            if self.frame >= self.max_frames:
                self.frame = 0

    def getDimensions(self):
        pass