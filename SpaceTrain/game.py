import pygame
import math
import random

from train import Train
from bullet import Bullet
from bar import Bar
from enemy import Enemy
from explosion import Explosion
from shockwave import Shockwave
from fontDrawer import FontDrawer

pygame.init()

class Game:

    def __init__(self, window, window_width, window_height):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height

        train_sprite = pygame.image.load("SpaceTrain/res/train.png").convert_alpha()
        self.bullet_sprite = pygame.image.load("SpaceTrain/res/bullet.png").convert_alpha()
        self.rail_sprite = pygame.image.load("SpaceTrain/res/rail.png").convert_alpha()
        self.bar_sprite = pygame.image.load("SpaceTrain/res/bar.png").convert_alpha()
        self.enemyA_sprite = pygame.image.load("SpaceTrain/res/ship.png").convert_alpha()
        self.enemyB_sprite = pygame.image.load("SpaceTrain/res/ship2.png").convert_alpha()
        self.explosion = pygame.image.load("SpaceTrain/res/explosion.png").convert_alpha()
        turret = pygame.image.load("SpaceTrain/res/turret.png").convert_alpha()
        font_sheet = pygame.image.load("SpaceTrain/res/font_sheet.png").convert_alpha()

        self.fontDrawer = FontDrawer(font_sheet)
        self.train = Train(self.window_width, self.window_height, train_sprite, turret)
        self.bar = Bar(self.window_width, self.window_height, self.bar_sprite)
        self.enemies = []
        self.bullets = []
        self.explosions = []
        self.score = 0

    def draw(self):

        self.window.fill((0, 0, 0))

        self.bar.draw(self.window)

        self._drawRail()

        for entity in self.enemies:
            entity.draw(self.window, self.enemyA_sprite if entity.enemy_type == entity.ENEMY_TYPE_A else self.enemyB_sprite)

        for entity in self.bullets:
            entity.draw(self.window, self.bullet_sprite)

        for exp in self.explosions:
            exp.draw(self.window, self.explosion)

        self.train.draw(self.window)

        self.fontDrawer.draw(self.window, f"Score: {self.score}", 10, 10, 20)
        self.fontDrawer.draw(self.window, f"Health: {self.train.health}", 10, 40, 20)

        pygame.display.update()

    def loop(self):
        shooting = self.train.update()

        self.bar.update()

        if shooting:
            mousePos = pygame.mouse.get_pos()
            
            if mousePos[1] < self.train.y + 30:
                b1x = (self.train.x + (self.train.TRAIN_WIDTH / 2))
                b1y = self.train.y
                angle = math.atan2(mousePos[1] - b1y, mousePos[0] - b1x)
                dirX = math.cos(angle)
                dirY = math.sin(angle)
                self.bullets.append(Bullet(b1x - 6, b1y - 6, dirX, dirY))
            else:
                b2x = (self.train.x + (self.train.TRAIN_WIDTH / 2))
                b2y = self.train.y + 60
                angle = math.atan2(mousePos[1] - b2y, mousePos[0] - b2x)
                dirX = math.cos(angle)
                dirY = math.sin(angle)
                self.bullets.append(Bullet(b2x - 6, b2y - 6, dirX, dirY))

        for enemy in self.enemies:
            isShooting = enemy.update()
            #if isShooting:
            if enemy.x < -100:
                enemy.vel /= 3
                enemy.vel *= -1
                enemy.x += 50
            if enemy.x > self.window_width + 100:
                enemy.vel *= 3
                enemy.vel *= -1
                enemy.x -= 50

        for bullet in self.bullets:
            bullet.update()

        self._checkCollisions()

        self._spawnIfNeeded()

        return {
            "score": self.score,
            "posX": self.train.x,
            #"enemies": self.enemies
            "health": self.train.health
        }
    
    def _spawnIfNeeded(self):
        enemies_alive = 0

        for enemy in self.enemies:
            if enemy.isAlive:
                enemies_alive += 1

        if enemies_alive == 0:
            quan = random.randint(1, 6)
            for i in range(quan):
                type = random.randint(0, 2)
                speed = random.randint(-30, -12)
                y = random.randint(32, self.window_height - 32)
                self.enemies.append(Enemy(self.window_width, y, speed, type))
    
    def _checkCollisions(self):
        
        for entity in self.bullets:
            if entity.isAlive:
                if entity.x > self.window_width + 100 or entity.x < -100 or entity.y > self.window_height + 100 or self.window_height < -100:
                    entity.isAlive = False
                    
        for enemy in self.enemies:
            if not enemy.isAlive:
                continue
            for bullet in self.bullets:
                if not bullet.isAlive:
                    continue
                if enemy.collides(bullet.x, bullet.y, bullet.BULLET_WIDTH, bullet.BULLET_HEIGHT):
                    enemy.isAlive = False
                    bullet.isAlive = False
                    self.explosions.append(Explosion(bullet.x, bullet.y))
                    self.score += 10 + (enemy.enemy_type * 10)

    def _drawRail(self):
        sprite = pygame.Surface([2, 2])
        sprite.blit(self.rail_sprite, (0, 0), (0, 0, 2, 2))
        sprite.set_colorkey((0, 0, 0))
        sprite = pygame.transform.scale(sprite, (self.window_width * 2, 8))
        self.window.blit(sprite, (0, (self.window_height - 4) / 2))

    def resetGame(self):
        self.train.reset()
        self.bar.reset()

        self.enemies = []
        self.bullets = []
        self.explosions = []
        self.score = 0
        
    def movingLeft(self, value):
        self.train.moving_left = value

    def movingRight(self, value):
        self.train.moving_right = value

    def shoot(self, value):
        self.train.shooting = value
        self.train.shooting_counter = self.train.shooting_delay

