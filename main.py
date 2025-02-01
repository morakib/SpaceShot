import math
import random
import pygame
from pygame import mixer
import tkinter as tk
import asyncio
from tkinter import simpledialog

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Caption and Icon
pygame.display.set_caption("SpaceShot")
icon = pygame.image.load('assets/shuttle.png')  # Updated path
pygame.display.set_icon(icon)

# Player Input for Names
root = tk.Tk()
root.withdraw()  # Hide the root window
player1_name = simpledialog.askstring("Input", "Enter Player 1's name (Player):") or "Player"
player2_name = simpledialog.askstring("Input", "Enter Player 2's name (Enemy):") or "Enemy"
winning_score = simpledialog.askinteger("Input", "Enter the winning score:", minvalue=1, maxvalue=20) or 2

# Player
playerImg = pygame.image.load('assets/spaceship.png')  # Updated path
playerX = random.randint(0, 736)
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('assets/game.png')  # Updated path
enemyX = random.randint(0, 736)
enemyY = 50
enemyX_change = 0

# Bullet
bulletImg = pygame.image.load('assets/bullet.png')  # Updated path
bulletX = 0
bulletY = 480
bulletY_change = 12
bullet_state = "ready"

# Enemy Bullet
enemy_bulletIMG = pygame.image.load('assets/bulletrev.png')  # Updated path
enemy_bulletX = 0
enemy_bulletY = enemyY
enemy_bulletY_change = 12
enemy_bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 550

# Bottom Score
enemy_score = 0
bottom_textX = 10
bottom_textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_bottom_score(x, y):
    score = font.render(f"{player2_name} Score : " + str(enemy_score), True, (0, 0, 0))
    screen.blit(score, (x, y))

def show_score(x, y):
    score = font.render(f"{player1_name} Score : " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def fire_enemy_bullet(x, y):
    global enemy_bullet_state
    enemy_bullet_state = "fire"
    screen.blit(enemy_bulletIMG, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

def isPlayerHit(playerX, playerY, enemy_bulletX, enemy_bulletY):
    distance = math.sqrt(math.pow(playerX - enemy_bulletX, 2) + (math.pow(playerY - enemy_bulletY, 2)))
    return distance < 27

game_break = False
running = True

# Game Loop

async def main():
    global running, playerX, playerX_change, bulletY, bullet_state, enemyX, enemyY, enemyX_change, enemy_bulletY, enemy_bullet_state, score_value, enemy_score, game_break, playerY, bulletX, bulletY_change, bullet_state, enemy_bulletX, enemy_bulletY_change    
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Player movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -1
                if event.key == pygame.K_RIGHT:
                    playerX_change = 1
                if event.key == pygame.K_UP:
                    if bullet_state == "ready":
                        bulletSound = mixer.Sound("assets/laser.wav")  # Updated path
                        bulletSound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    playerX_change = 0

            # Enemy movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    enemyX_change = -1
                if event.key == pygame.K_d:
                    enemyX_change = 1
                if event.key == pygame.K_w:
                    if enemy_bullet_state == "ready":
                        bulletSound = mixer.Sound("assets/laser.wav")  # Updated path
                        bulletSound.play()
                        enemy_bulletX = enemyX
                        fire_enemy_bullet(enemy_bulletX, enemy_bulletY)

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d]:
                    enemyX_change = 0

        # Player movement
        playerX += playerX_change
        playerX = max(0, min(playerX, 736))

        # Enemy movement
        enemyX += enemyX_change
        enemyX = max(0, min(enemyX, 736))

        # Bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        # Enemy bullet movement
        if enemy_bulletY >= 600:
            enemy_bulletX = enemyX
            enemy_bulletY = enemyY
            enemy_bullet_state = "ready"

        if enemy_bullet_state == "fire":
            fire_enemy_bullet(enemy_bulletX, enemy_bulletY)
            enemy_bulletY += enemy_bulletY_change

        # Winner logic
        if score_value == winning_score or enemy_score == winning_score:
            winner_text = f"{player1_name} WIN" if score_value == winning_score else f"{player2_name} WIN"
            over_text = over_font.render(winner_text, True, (0, 0, 0))
            screen.blit(over_text, (200, 250))
            game_break = True

        # Collision
        if isCollision(enemyX, enemyY, bulletX, bulletY) and not game_break:
            explosionSound = mixer.Sound("assets/explosion.wav")  # Updated path
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX = random.randint(0, 736)
            enemyY = 50

        if isPlayerHit(playerX, playerY, enemy_bulletX, enemy_bulletY) and not game_break:
            explosionSound = mixer.Sound("assets/explosion.wav")  # Updated path
            explosionSound.play()
            enemy_bulletY = 50
            enemy_bullet_state = "ready"
            enemy_score += 1
            playerX = random.randint(0, 736)
            playerY = 480

        player(playerX, playerY)
        enemy(enemyX, enemyY)
        show_score(textX, textY)
        show_bottom_score(bottom_textX, bottom_textY)
        pygame.display.update()
        await asyncio.sleep(0)
asyncio.run(main())
