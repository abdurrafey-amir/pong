import pygame
import sys
import random


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    # movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
        pygame.mixer.Sound.play(pong_sound)
    
    # player score
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()

    # opponent score
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
    
    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_reset():
    global ball_speed_y, ball_speed_x, score_time
    
    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)

    if current_time - score_time < 700:
        number_3 = font.render('3', False, light_grey)
        screen.blit(number_3, (screen_width/2 - 10, screen_height/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_2 = font.render('2', False, light_grey)
        screen.blit(number_2, (screen_width/2 - 10, screen_height/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_1 = font.render('1', False, light_grey)
        screen.blit(number_1, (screen_width/2 - 10, screen_height/2 + 20))
          
    if current_time - score_time < 2100:
        ball_speed_x = 0
        ball_speed_y = 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None

# general setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# setting up the main window
screen_width = 1280
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# game rectangles
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# text variables
player_score = 0
opponent_score = 0
font = pygame.font.Font("freesansbold.ttf", 32)

# timer
score_time = True

# sound
pong_sound = pygame.mixer.Sound('pong.ogg')
score_sound = pygame.mixer.Sound('score.ogg')

while True:
    # handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    ball_animation()
    player_animation()
    opponent_animation()
    
    # visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

    player_text = font.render(f'{player_score}', False, light_grey)
    screen.blit(player_text, (screen_width/2 + 15, screen_height/2))

    opponent_text = font.render(f'{opponent_score}', False, light_grey)
    screen.blit(opponent_text, (screen_width/2 - 30, screen_height/2))

    if score_time:
        ball_reset()

    # updating the window
    pygame.display.flip()
    clock.tick(60)