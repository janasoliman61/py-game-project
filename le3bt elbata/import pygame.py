import pygame
import sys
import random

speed = 3
tick = 1920

def game_floor():
    screen.blit(floor_base, (floor_x_pos, 750))
    screen.blit(floor_base, (floor_x_pos + 576, 750))


def check_collision(pipes):
    #check pipe is not hit
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
         die_sound.play()
         return False
    #check floor is not hit
    if bird_rect.top <= -100 or bird_rect.bottom >= 750:
    #    
       return False
    return True


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom=(900, random_pipe_pos - 300))
    bottom_pipe = pipe_surface.get_rect(midtop=(900, random_pipe_pos))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= speed
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def draw_text(text, font, text_col):
    img = font.render(text, True, text_col)
    screen.blit(img, (10, 10))

pygame.init()
clock = pygame.time.Clock()

# variables
gravity = 0.25
bird_movement = 0
screen = pygame.display.set_mode((540, 1080))
game_active = True
font = pygame.font.Font('freesansbold.ttf', 32)
white = (255, 255, 255)

#Background
background = pygame.image.load('image/background-day.png').convert()
background = pygame.transform.scale2x(background)

#BIRD
bird = pygame.image.load('image/bird-midflap.png').convert()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100, 512))

#Floor
floor_base = pygame.image.load('image/base.png').convert()
floor_base = pygame.transform.scale2x(floor_base)
floor_x_pos = 0

message = pygame.image.load('image/message.png').convert_alpha()
message = pygame.transform.scale2x(message)
game_over_rect = message.get_rect(center=(288, 512))

# Building pipes
pipe_surface = pygame.image.load('image/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [400, 600, 800]
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, tick)
pipe_rect = pipe_surface.get_rect(center=(100, 512))



# Score
score = -1
pass_pipe = False 
HEIGHT = 1024
WIDTH = 576
FONT_COLOR = (255,255,255)
CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2
CENTER = (CENTER_X,CENTER_Y)

def display_message(text):
    pass  ############################


# ssound
flap_sound=pygame.mixer.Sound('sound/audio_wing.ogg')
die_sound=pygame.mixer.Sound('sound/audio_die.ogg')

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                bird_rect.center = (100, 512)
                bird_movement = 0
                game_active = True
                pipe_list.clear()
        if event.type == SPAWN_PIPE and game_active:
            pipe_list.extend(create_pipe())
            score  += 1
        if score == 3:
            speed = 5
            tick = 1200
        if score == 8:
            display_message('YOU WON')

    



    screen.blit(background, (0, 0))

    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird, bird_rect)
        # Draw pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        # Collision with the floor
        game_active = check_collision(pipe_list)
    else:
        screen.blit(message, game_over_rect)
        score  = -1 
        speed = 3
        tick = 1920
    #Create game floor
    game_floor()
    floor_x_pos -= 1
    if floor_x_pos <= -576:
        floor_x_pos = 0


    # Show score
    x = 0
    if score != -1:
        x = score
    draw_text('Score : '+str(x), font, white)
    pygame.display.update()
    clock.tick(120)
