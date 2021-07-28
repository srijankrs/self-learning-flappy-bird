import neat
import pygame
import random
import sys

width = 432
height = 768
base_position = 0
displacement = .2
pipe_distance = 350
pass_distance = 660
pipe_heights = [100, 150, 200, 250, 300]
gravity = .0025
generation = 0
score = 0
max_score = 0

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.font.init()
game_font = pygame.font.SysFont('Comic Sans MS', 30)


class LowerPipe:
    pipe = pygame.image.load('assets/pipe-green.png').convert_alpha()
    pipe_lower = pygame.transform.rotozoom(pipe, 0, 1.5)

    def __init__(self, x, y):
        self.obj = self.pipe_lower.get_rect(midbottom=(x, y))

    def get_pipe_rect(self):
        return self.obj

    def get_pipe(self):
        return self.pipe_lower

    def move(self, delta_time):
        self.obj.centerx -= delta_time * displacement


class UpperPipe:
    pipe = pygame.image.load('assets/pipe-green.png').convert_alpha()
    pipe_upper = pygame.transform.flip(pygame.transform.rotozoom(pipe, 0, 1.5), False, True)

    def __init__(self, x, y):
        self.obj = self.pipe_upper.get_rect(midbottom=(x, y))

    def get_pipe_rect(self):
        return self.obj

    def get_pipe(self):
        return self.pipe_upper

    def move(self, delta_time):
        self.obj.centerx -= delta_time * displacement


class Bird:
    x = 100
    y = height / 2
    bird_speed = 0
    bird = pygame.transform.rotozoom(pygame.image.load('assets/bluebird-midflap.png').convert_alpha(), 0, 1.5)

    def __init__(self, t):
        self.obj = self.bird.get_rect(center=(self.x + t, self.y))

    def jump(self, delta_time):
        # print("bird jumping")
        self.bird_speed = -0.7

    def move(self, delta_time):
        self.bird_speed += gravity * delta_time
        self.obj.centery += self.bird_speed * delta_time

    def get_rect(self):
        return self.obj

    def get_bird(self):
        return self.bird


class GameController:
    bg_surface = pygame.transform.rotozoom(pygame.image.load('assets/background-day.png').convert(), 0, 1.5)
    base = pygame.transform.rotozoom(pygame.image.load('assets/base.png').convert(), 0, 1.5)
    upper_pipes = []
    lower_pipes = []
    running = True

    def collision(self, bird):
        for pipe in self.upper_pipes:
            # for i in range(len(birds)):
            if bird.get_rect().colliderect(pipe.get_pipe_rect()):
                # birds[i] = (birds[i][0], 0)
                return True

        for pipe in self.lower_pipes:
            # for i in range(len(birds)):
            if bird.get_rect().colliderect(pipe.get_pipe_rect()):
                # birds[i] = (birds[i][0], 0)
                return True

            # for i in range(len(birds)):
        if bird.get_rect().top <= 0 or bird.get_rect().bottom >= 605:
            return True

        return False

    def move_elements(self, delta_time, ge, birds):
        global base_position
        self.check_pipe_position(ge)
        for pipe in self.lower_pipes:
            pipe.move(delta_time)
        for pipe in self.upper_pipes:
            pipe.move(delta_time)

        if self.running:
            base_position -= displacement * delta_time
            if base_position <= -width:
                base_position = 0
        for bird in birds:
            bird.move(delta_time)

    def fill_elements(self, birds, generation_text, score_text, max_score_text):
        for pipe in self.lower_pipes:
            screen.blit(pipe.get_pipe(), pipe.get_pipe_rect())
        for pipe in self.upper_pipes:
            screen.blit(pipe.get_pipe(), pipe.get_pipe_rect())

        screen.blit(self.base, (base_position, height - 150))
        screen.blit(self.base, (base_position + width, height - 150))
        for bird in birds:
            screen.blit(bird.get_bird(), bird.get_rect())
        # print("birds fill len = {}", len(birds))
        screen.blit(generation_text, (0, 0))
        screen.blit(score_text, (0, 60))
        screen.blit(max_score_text, (0, 30))

    def check_pipe_position(self, ge):
        global score
        if self.upper_pipes[0].get_pipe_rect().centerx + self.lower_pipes[0].get_pipe_rect().width < 0:
            self.scored = False
            self.upper_pipes.pop(0)
            self.lower_pipes.pop(0)
            ran = random.choice(pipe_heights)
            self.upper_pipes.append(UpperPipe(100 + 5 * pipe_distance - self.lower_pipes[0].get_pipe_rect().width, ran))
            self.lower_pipes.append(LowerPipe(100 + 5 * pipe_distance - self.lower_pipes[0].get_pipe_rect().width, ran + pass_distance))

    def create_pipes(self):
        self.upper_pipes.clear()
        self.lower_pipes.clear()
        for i in range(1, 6):
            ran = random.choice(pipe_heights)
            self.upper_pipes.append(UpperPipe(100 + i * pipe_distance, ran))
            self.lower_pipes.append(LowerPipe(100 + i * pipe_distance, ran + pass_distance))

    def reset(self):
        self.upper_pipes.clear()
        self.lower_pipes.clear()
        self.create_pipes()

    def play(self, genomes, config):
        global generation
        global score
        global max_score
        generation += 1
        score = 0
        nets = []
        birds = []
        ge = []
        self.create_pipes()
        print('genomes ', genomes)
        i = 0
        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            birds.append(Bird(i))
            # i += 1
            ge.append(genome)

        last_time = pygame.time.get_ticks()
        clock = pygame.time.Clock()
        counter = pygame.time.get_ticks()
        self.scored = False
        while True and len(birds) > 0:
            time_now = pygame.time.get_ticks()
            delta_time = time_now - last_time
            last_time = time_now

            generation_text = game_font.render('Generation - ' + str(generation), False, (0, 0, 0))
            score_text = game_font.render('Score - ' + str(score), False, (0, 0, 0))
            max_score_text = game_font.render('Max Score - ' + str(max_score), False, (0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_SPACE:
                #         birds[0].jump(delta_time)
            # print("birds len {}", len(birds))
            ind = 0
            if self.upper_pipes[0].get_pipe_rect().centerx + birds[0].get_rect().width/2 + self.lower_pipes[ind].get_pipe_rect().width/2 < birds[0].x:
                ind = 1

            if ind == 1 and not self.scored:
                score += 1
                # print("score {}", score)
                for genome in ge:
                    genome.fitness += 10
                self.scored = True

            max_score = max(score, max_score)
            for x, bird in enumerate(birds):
                ge[x].fitness += 0.1
                output = nets[birds.index(bird)].activate((bird.get_rect().centery, self.upper_pipes[ind].get_pipe_rect().bottom, self.lower_pipes[ind].get_pipe_rect().top))
                # print("output {}", output[0])
                if output[0] > 0.5:
                    bird.jump(delta_time)

            for bird in birds:
                if self.collision(bird):
                    ge[birds.index(bird)].fitness -= 2
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            screen.blit(self.bg_surface, (0, 0))
            self.move_elements(delta_time, ge, birds)
            self.fill_elements(birds, generation_text, score_text, max_score_text)
            clock.tick(60)
            pygame.display.update()


config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            'config.txt')

p = neat.Population(config)
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
game = GameController()
winner = p.run(game.play, 500)
print('\nBest Bird:\n{!s}'.format(winner))
