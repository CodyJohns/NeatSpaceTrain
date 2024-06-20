import pygame

from game import Game

class MainGame:

    def __init__(self):
        width, height = 1280, 720
        window = pygame.display.set_mode((width, height), vsync=1)
        pygame.display.set_caption("Space Train")
        self.game = Game(window, width, height)

    def start(self):
        clock = pygame.time.Clock()

        loop = True

        while loop:
            clock.tick(60)

            game_stats = self.game.loop()

            self.game.draw()

            #handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.game.movingLeft(True)
                    if event.key == pygame.K_d:
                        self.game.movingRight(True)
                    if event.key == pygame.K_r:
                        self.game.resetGame()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.game.movingLeft(False)
                    if event.key == pygame.K_d:
                        self.game.movingRight(False)
                    if event.key == pygame.K_SPACE:
                        self.game.shoot(False)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.game.shoot(True)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.game.shoot(False)

    def train(self):
        

mainGame = MainGame()

mainGame.start()