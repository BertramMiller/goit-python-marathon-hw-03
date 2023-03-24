import random
import pygame
from os import listdir
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 1366,700

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
font = pygame.font.SysFont(None, 46)
main_surface = pygame.display.set_mode(screen)
IMGS_PATH = 'player-animation'
BG_PATH = 'background-animation'

bg_imgs =  [pygame.image.load(BG_PATH + '/' + file).convert_alpha() for file in listdir(BG_PATH)]
bg_index = 0
bg = pygame.transform.scale(bg_imgs[bg_index].convert(), screen)

player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
player_index = 0
player = player_imgs[player_index]
player_rect = player.get_rect()
player_speed = 3

def create_enemy():
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(width, random.randint(0, height-20), *enemy.get_size())
    enemy_speed = random.randint(2, 6)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(0, width-20), 0, *bonus.get_size())
    bonus_speed = 1
    return [bonus, bonus_rect, bonus_speed]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 250)

CHANGE_BG = pygame.USEREVENT + 4
pygame.time.set_timer(CHANGE_BG, 300)

img_index = 0

score = 0
enemies = []
bonuses = []

is_working = True
game_over = False

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if not game_over:
            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())
            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())
            if event.type == CHANGE_BG:
                bg_index = (bg_index + 1) % len(bg_imgs)
                bg = pygame.transform.scale(bg_imgs[bg_index], screen)
                if bg_index == len(bg_imgs):
                    bg_index = 0
                    bg = bg_imgs[bg_index]

            if event.type == CHANGE_IMG:
                player_index = (player_index + 1) % len(player_imgs)
                player = player_imgs[player_index]
                if img_index == len(player_imgs):
                    img_index = 0
                    player = player_imgs[img_index]

    pressed_keys = pygame.key.get_pressed()

    main_surface.blit(bg, (0, 0))
    main_surface.blit(font.render(str(score), True, RED), (width - 30, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

        if not game_over and player_rect.colliderect(enemy[1]):
            bg = pygame.transform.scale(pygame.image.load('screen.png').convert(), screen)
            enemies = []
            bonuses = []
            game_over = True

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].top > height:
            bonuses.pop(bonuses.index(bonus))

        if not game_over and player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1

    if not game_over:

        if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
            player_rect = player_rect.move(0, player_speed)

        if pressed_keys[K_UP] and not player_rect.top <= 0:
            player_rect = player_rect.move(0, -player_speed)

        if pressed_keys[K_RIGHT] and not player_rect.right >= width:
            player_rect = player_rect.move(player_speed, 0)

        if pressed_keys[K_LEFT] and not player_rect.left <= 0:
            player_rect = player_rect.move(-player_speed, 0)

    main_surface.blit(player, player_rect)

    if game_over and score <= 5:
        text = font.render("GAME OVER!", True, RED)
        text_rect = text.get_rect(center=(width/2, height/2))
        main_surface.blit(text, text_rect)

    if game_over and score > 5:
        text = font.render("WIN!", True, GREEN)
        text_rect = text.get_rect(center=(width/2, height/2))
        main_surface.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
