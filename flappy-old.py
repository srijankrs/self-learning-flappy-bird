import pygame
import random
import sys

width = 432
height = 768
base_position = 0
displacement = .2
pipe_distance = 350
pass_distance = 200
pipe_heights = [100, 150, 200, 250, 300]
gravity = .0025


def handle_bird(delta_time):
    global bird_speed
    global bird_position
    global birds
    val = 0
    if running:
        bird_speed += gravity * delta_time
        val = bird_speed * delta_time
    # bird_rect = bird_midflap.get_rect(center = (100,bird_position))
    for i in range(len(birds)):
        allow = birds[i][1]
        # print("allow = {}", allow)
        if allow == 1:
            birds[i][0].centery += val
            screen.blit(bird_mid_flap, birds[i][0])
    # else:
    # 	screen.blit(bird_midflap, birds[i][0])


def handle_base(delta_time):
    global base_position
    if running:
        base_position -= displacement * delta_time
        if base_position <= -width:
            base_position = 0
    screen.blit(base, (base_position, height - 150))
    screen.blit(base, (base_position + width, height - 150))


def handle_pipe(delta_time):
    global upper_pipes
    global lower_pipes
    global running
    if running and upper_pipes[0].centerx < 0:
        upper_pipes.pop(0)
        lower_pipes.pop(0)
        ran = random.choice(pipe_heights)
        upper_pipes.append(pipe_upper.get_rect(midbottom=(100 + 5 * pipe_distance, ran)))
        lower_pipes.append(pipe_lower.get_rect(midtop=(100 + 5 * pipe_distance, ran + pass_distance)))
    for i in range(len(upper_pipes)):
        # print(upper_pipes[i].centerx)
        if running:
            upper_pipes[i].centerx -= delta_time * displacement
            lower_pipes[i].centerx -= delta_time * displacement
        screen.blit(pipe_upper, upper_pipes[i])
        screen.blit(pipe_lower, lower_pipes[i])


def check_collision():
    global birds
    global upper_pipes
    global lower_pipes
    for pipe in upper_pipes:
        for i in range(len(birds)):
            if birds[i][0].colliderect(pipe):
                birds[i] = (birds[i][0], 0)
                return False

    for pipe in lower_pipes:
        for i in range(len(birds)):
            if birds[i][0].colliderect(pipe):
                birds[i] = (birds[i][0], 0)
                return False
    # print(bird_rect.top)
    last = 0
    for i in range(len(birds)):
        if birds[i][0].top <= 0 or birds[i][0].bottom >= 605:
            birds[i] = (birds[i][0], 0)
        if birds[i][1] == 1:
            last = 1
    if last == 0:
        return True

    return False


def refresh_game():
    global running
    global bird_position
    global bird_speed
    global bird_rect
    global upper_pipes
    global lower_pipes
    global refreshed

    upper_pipes.clear()
    lower_pipes.clear()
    for i in range(1, 6):
        ran = random.choice(pipe_heights)
        upper_pipes.append(pipe_upper.get_rect(midbottom=(100 + i * pipe_distance, ran)))
        lower_pipes.append(pipe_lower.get_rect(midtop=(100 + i * pipe_distance, ran + pass_distance)))

    bird_position = height / 2
    bird_speed = 0
    # bird_rect.center = (100,bird_position)
    get_birds()
    # running = True
    refreshed = True


def game_over():
    global running
    global refreshed
    running = False
    refreshed = False


def compute():
    global upper_pipes
    x_dis = 0
    y_dis = 0


# u_pipe = upper_pipes[0]
# l_pipe = lower_pipes[0]
# if u_pipe.centerx < 100:
# 	u_pipe = upper_pipes[1]
# 	l_pipe = lower_pipes[1]
# x_dis = u_pipe.centerx - 100
# y_dis = bird_rect.centery - (u_pipe.midbottom[1]+l_pipe.midtop[1])/2

# print("x_dis = {}, y_dis = {}", x_dis, y_dis)

def get_birds():
    global birds
    birds.clear()
    birds.append((bird_mid_flap.get_rect(center=(100, bird_position)), 1))
    birds.append((bird_mid_flap.get_rect(center=(120, bird_position)), 1))
    birds.append((bird_mid_flap.get_rect(center=(150, bird_position)), 1))


pygame.init()

running = False
refreshed = False
screen = pygame.display.set_mode((width, height))

bg_surface = pygame.transform.rotozoom(pygame.image.load('assets/background-day.png').convert(), 0, 1.5)
base = pygame.transform.rotozoom(pygame.image.load('assets/base.png').convert(), 0, 1.5)
pipe = pygame.image.load('assets/pipe-green.png').convert_alpha()
pipe_lower = pygame.transform.rotozoom(pipe, 0, 1.5)
pipe_upper = pygame.transform.flip(pygame.transform.rotozoom(pipe, 0, 1.5), False, True)
bird_mid_flap = pygame.transform.rotozoom(pygame.image.load('assets/bluebird-midflap.png').convert_alpha(), 0, 1.5)

bird_position = height / 2
bird_speed = 0
birds = []
get_birds()

upper_pipes = []
lower_pipes = []

# refresh_game()

last_time = pygame.time.get_ticks()
clock = pygame.time.Clock()
counter = pygame.time.get_ticks()
while True:
    time_now = pygame.time.get_ticks()
    delta_time = time_now - last_time
    last_time = time_now

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and running:
                bird_speed = -0.7
            if event.key == pygame.K_SPACE and running == False:
                running = True

    if time_now - counter > 500 and refreshed == False:
        refresh_game()

    if time_now % 10 == 0 and running:
        compute()

    if check_collision():
        if running:
            counter = time_now
            game_over()

    screen.blit(bg_surface, (0, 0))

    handle_pipe(delta_time)
    handle_base(delta_time)
    handle_bird(delta_time)

    clock.tick(120)
    pygame.display.update()
pygame.quit()
