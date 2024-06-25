import pygame
import time
import neat
import os
import pickle

from game import Game

class MainGame:

    def __init__(self):
        self.width, self.height = 1280, 720

    def start(self):
        window = pygame.display.set_mode((self.width, self.height), vsync=1)
        pygame.display.set_caption("Space Train")
        self.game = Game(window, self.width, self.height)
        
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

    def test(self, nn):
        window = pygame.display.set_mode((self.width, self.height), vsync=1)
        pygame.display.set_caption("Space Train")
        self.game = Game(window, self.width, self.height)
        
        clock = pygame.time.Clock()

        loop = True

        while loop:
            clock.tick(60)

            game_stats = self.game.loop()

            self.game.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                    break

            normMouseX = game_stats["mousePos"][0] / self.width
            normMouseY = game_stats["mousePos"][1] / self.height
            normPosX = game_stats["posX"] / self.width
            normPosY = game_stats["posY"] / self.height
            shooting = 0 if not game_stats["isShooting"] else 1

            input_data = [normPosX, normPosY, shooting, normMouseX, normMouseY]

            #only closest 3 enemies
            for i in range(3 if len(game_stats["enemiesPos"]) >= 3 else len(game_stats["enemiesPos"])):
                input_data.append(game_stats["enemiesPos"][i][0] / self.width)
                input_data.append(game_stats["enemiesPos"][i][1] / self.height)
                input_data.append(abs(game_stats["enemiesPos"][i][2]) / self.width) #velocity
                input_data.append(abs(game_stats["enemiesPos"][i][0] - game_stats["posX"]) / self.width) #relative x pos
                input_data.append(abs(game_stats["enemiesPos"][i][1] - game_stats["posY"]) / self.height) #relative y pos

            #if less than 3 enemies then fill with zeroes
            if len(game_stats["enemiesPos"]) < 3:
                for i in range(3 - len(game_stats["enemiesPos"])):
                    input_data.append(0)
                    input_data.append(0)
                    input_data.append(0)
                    input_data.append(0)
                    input_data.append(0)

            if not len(input_data) == 20:
                print(f"Input Data: {input_data}")
                raise AssertionError(f"Expected 20 inputs, but got {len(input_data)} instead")

            output = nn.activate(input_data)

            move_threshold = 0
            shoot_threshold = 0
            
            self.game.movingLeft(output[0] > move_threshold)
            self.game.movingRight(output[1] > move_threshold)
            self.game.shoot(output[2] > shoot_threshold)

            denormMouseX = int(output[3] * self.width)
            denormMouseY = int(output[4] * self.height)

            self.game.setMousePos(denormMouseX, denormMouseY)

    def train(self, genome, config):

        loop = True
        start_time = time.time()

        nn = neat.nn.FeedForwardNetwork.create(genome, config)

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            game_stats = self.game.loop()

            self.game.draw()

            normMouseX = game_stats["mousePos"][0] / self.width
            normMouseY = game_stats["mousePos"][1] / self.height
            normPosX = game_stats["posX"] / self.width
            normPosY = game_stats["posY"] / self.height
            shooting = 0 if not game_stats["isShooting"] else 1

            input_data = [normPosX, normPosY, shooting, normMouseX, normMouseY]

            #only closest 3 enemies
            for i in range(3 if len(game_stats["enemiesPos"]) >= 3 else len(game_stats["enemiesPos"])):
                input_data.append(game_stats["enemiesPos"][i][0] / self.width)
                input_data.append(game_stats["enemiesPos"][i][1] / self.height)
                input_data.append(abs(game_stats["enemiesPos"][i][2]) / self.width) #velocity
                input_data.append(abs(game_stats["enemiesPos"][i][0] - game_stats["posX"]) / self.width) #relative x pos
                input_data.append(abs(game_stats["enemiesPos"][i][1] - game_stats["posY"]) / self.height) #relative y pos

            #if less than 3 enemies then fill with zeroes
            if len(game_stats["enemiesPos"]) < 3:
                for i in range(3 - len(game_stats["enemiesPos"])):
                    input_data.append(0)
                    input_data.append(0)
                    input_data.append(0)
                    input_data.append(0)
                    input_data.append(0)

            if not len(input_data) == 20:
                print(f"Input Data: {input_data}")
                raise AssertionError(f"Expected 20 inputs, but got {len(input_data)} instead")

            #inputs:
            # (posX, posY, isShooting, mousePosX, mousePosY, enemy data...)

            output = nn.activate(input_data)

            #outputs:
            # 0:movingLeft
            # 1:movingRight
            # 2:shooting
            # 3:mousePosX
            # 4:mousePosY

            move_threshold = 0 #these may change idk
            shoot_threshold = 0

            #discourage staying still
            if (output[0] <= move_threshold and output[1] <= move_threshold) or (output[0] > move_threshold and output[1] > move_threshold):
                genome.fitness -= 0.05

            #punish the genome if there are enemies and it isn't shooting
            if output[2] <= shoot_threshold and len(game_stats["enemiesPos"]) > 0:
                genome.fitness -= 1

            #maybe penalize if they shoot too much?
            
            self.game.movingLeft(output[0] > move_threshold)
            self.game.movingRight(output[1] > move_threshold)
            self.game.shoot(output[2] > shoot_threshold)

            denormMouseX = (output[3] * self.width)
            denormMouseY = (output[4] * self.height)

            #punish the genome if the mouse coords arent valid
            if denormMouseX > self.width or denormMouseY > self.height or denormMouseX < 0 or denormMouseY < 0:
                genome.fitness -= 1

            #maybe penalize the distance of the mouse from the closest enemy?

            self.game.setMousePos(denormMouseX, denormMouseY)

            duration = time.time() - start_time

            if game_stats["score"] > 0 or game_stats["shots"] > 50 or duration > 10:
                #calculate fitness
                genome.fitness += (game_stats["score"] * 100) - duration #add health later
                break

    def evaluate(self, genomes, config):
        window = pygame.display.set_mode((self.width, self.height), vsync=1)
        pygame.display.set_caption("Space Train")

        for i, (genome_id, genome) in enumerate(genomes):
            genome.fitness = 0
            self.game = Game(window, self.width, self.height, ai=True)

            self.train(genome, config)

    def runNeat(self, config):
        #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-49')
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(neat.Checkpointer(1))

        winner = p.run(self.evaluate, 1)
        with open("best_model.pickle", "wb") as f:
            pickle.dump(winner, f)

    def testBest(self, config):
        with open("best_model.pickle", "rb") as f:
            winner = pickle.load(f)
        
        winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
        self.test(winner_net)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    mainGame = MainGame()

    mainGame.runNeat(config)
    #mainGame.start() #play normally
    #mainGame.testBest(config)
