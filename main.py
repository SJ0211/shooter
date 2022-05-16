# -*- coding: utf-8 -*-


import pygame
import random
from Player import Player
from Enemy import Enemy
from Projectile import Projectile
import Weapon
import math
from Items import Health
from pygame import RLEACCEL

pygame.init()
size = (1280, 720)
BGCOLOR = (255, 255, 255)
screen = pygame.display.set_mode(size)
scoreFont = pygame.font.Font("fonts/UpheavalPro.ttf", 30)
healthFont = pygame.font.Font("fonts/OmnicSans.ttf", 50)
healthRender = healthFont.render('z', True, pygame.Color('red'))
pygame.display.set_caption("SJ Pygame")
bg = pygame.image.load("background.png").convert()
pygame.mouse.set_visible(False)  # hide the cursor

# Image for "manual" cursor
MANUAL_CURSOR = pygame.image.load('aim.png').convert_alpha()


done = False
hero = pygame.sprite.GroupSingle(Player(screen.get_size()))
enemies = pygame.sprite.Group()
healths = pygame.sprite.Group()
lastEnemy = 0
score = 0
clock = pygame.time.Clock()

def move_entities(hero, enemies, timeDelta):
    global screen

    score = 0
    hero.sprite.move(screen.get_size(), timeDelta)
    for enemy in enemies:
        enemy.move(enemies, hero.sprite.rect.topleft, timeDelta)
        enemy.shoot(hero.sprite.rect.topleft)
    for proj in Enemy.projectiles:
        proj.move(screen.get_size(), timeDelta)
        if pygame.sprite.spritecollide(proj, hero, False):
            proj.kill()
            hero.sprite.health -= 1
            sound = pygame.mixer.Sound("lost.wav")
            pygame.mixer.Sound.play(sound)
            if hero.sprite.health <= 0:
                hero.sprite.alive = False
    for proj in Player.projectiles:
        proj.move(screen.get_size(), timeDelta)
        enemiesHit = pygame.sprite.spritecollide(proj, enemies, True)
        if enemiesHit:
            proj.kill()
            score += len(enemiesHit)

            i = random.randint(1, 30)
            if i == 1:   #spawn health
                print("health")
                x = random.randint(0, 800)
                y = random.randint(0, 600)
                health = Health(x, y)
                healths.add(health)



    for health in healths:
        if pygame.sprite.spritecollide(health, hero, False):
            health.kill()
            hero.sprite.health += 1
            sound = pygame.mixer.Sound("health.wav")
            pygame.mixer.Sound.play(sound)



    return score

def render_entities(hero, enemies):
    hero.sprite.render(screen)
    for health in healths:
        health.render(screen)
    for proj in Player.projectiles:
        proj.render(screen)
    for proj in Enemy.projectiles:
        proj.render(screen)
    for enemy in enemies:
        enemy.render(screen)




def process_keys(keys, hero):
    if keys[pygame.K_w]:
        hero.sprite.movementVector[1] -= 1
    if keys[pygame.K_a]:
        hero.sprite.movementVector[0] -= 1
        hero.sprite.image = pygame.image.load("player-left.png")

    if keys[pygame.K_s]:
        hero.sprite.movementVector[1] += 1
    if keys[pygame.K_d]:
        hero.sprite.movementVector[0] += 1
        hero.sprite.image = pygame.image.load("player-right.png")

    if keys[pygame.K_1]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[0]
    if keys[pygame.K_2]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[1]
    if keys[pygame.K_3]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[2]
        
def process_mouse(mouse, hero):
    if mouse[0]:
        hero.sprite.shoot(pygame.mouse.get_pos())

pygame.mixer.init()
pygame.mixer.music.load("msi.wav")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play()

def game_loop():
    done = False
    hero = pygame.sprite.GroupSingle(Player(screen.get_size()))
    enemies = pygame.sprite.Group()
    healths = pygame.sprite.Group()
    lastEnemy = pygame.time.get_ticks()
    score = 0
    
    while hero.sprite.alive and not done:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        currentTime = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        
        process_keys(keys, hero)
        process_mouse(mouse, hero)

        # Enemy spawning process
        if lastEnemy < currentTime - 200 and len(enemies) < 50:
            spawnSide = random.random()
            if spawnSide < 0.25:
                enemies.add(Enemy((0, random.randint(0, size[1]))))
            elif spawnSide < 0.5:
                enemies.add(Enemy((size[0], random.randint(0, size[1]))))
            elif spawnSide < 0.75:
                enemies.add(Enemy((random.randint(0, size[0]), 0)))
            else:
                enemies.add(Enemy((random.randint(0, size[0]), size[1])))
            lastEnemy = currentTime
        
        score += move_entities(hero, enemies, clock.get_time()/17)
        screen.blit(bg, (0, 0))
        render_entities(hero, enemies)

        #weapon aim
        screen.blit(MANUAL_CURSOR, (pygame.mouse.get_pos()))

        # Health and score render
        for hp in range(hero.sprite.health):
            screen.blit(healthRender, (15 + hp*35, 0))
        scoreRender = scoreFont.render(str(score), True, pygame.Color('black'))
        scoreRect = scoreRender.get_rect()
        scoreRect.right = size[0] - 20
        scoreRect.top = 20
        screen.blit(scoreRender, scoreRect)
        
        pygame.display.flip()
        clock.tick(120)

done = game_loop()
while not done:
    pygame.mixer.music.stop()
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    currentTime = pygame.time.get_ticks()
    screen.blit(pygame.image.load("died.png"), (0,120))
    for i in healths:
        i.kill()

    scoreRender = scoreFont.render(str(score), True, pygame.Color('black'))
    scoreRect = scoreRender.get_rect()
    scoreRect.right = size[0] - 20
    scoreRect.top = 20
    screen.blit(scoreRender, scoreRect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    if keys[pygame.K_r]:
        pygame.mixer.music.load("msi.wav")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        done = game_loop()


    clock.tick(30)
pygame.quit()
