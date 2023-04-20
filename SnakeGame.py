import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (70, 76, 81)
BLUE = (33, 88, 136)
GOLD = (226, 168, 9)

# Snake and food settings
snake_pos = [[100, 50], [90, 50], [80, 50]]
snake_speed = 10
food_pos = [random.randrange(1, WIDTH // 10) * 10, random.randrange(1, HEIGHT // 10) * 10]
food_spawn = True
direction = 'RIGHT'

score = 0
HIGHSCORE_FILE = 'highscores.txt'

def load_highscores(file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write('0\n')

    with open(file, 'r') as f:
        highscores = [int(line.strip()) for line in f.readlines()]
        return highscores


def save_highscore(score, file):
    highscores = load_highscores(file)
    highscores.append(score)
    highscores.sort(reverse=True)
    highscores = highscores[:5]

    with open(file, 'w') as f:
        for hs in highscores:
            f.write(f'{hs}\n')


def display_score(screen, score, highscore):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score} High Score: {highscore}", True, BLACK)
    screen.blit(score_text, (10, 10))


# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

# Game Over Function
def game_over(score):
    save_highscore(score, HIGHSCORE_FILE)
    pygame.quit()
    sys.exit()


highscores = load_highscores(HIGHSCORE_FILE)
highscore = highscores[0]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over(score)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

    # Move the snake
    for i in range(len(snake_pos) - 1, 0, -1):
        snake_pos[i] = list(snake_pos[i - 1])

    if direction == 'UP':
        snake_pos[0][1] -= 10
    if direction == 'DOWN':
        snake_pos[0][1] += 10
    if direction == 'LEFT':
        snake_pos[0][0] -= 10
    if direction == 'RIGHT':
        snake_pos[0][0] += 10

    # Grow the snake
    if snake_pos[0] == food_pos:
        snake_pos.append(snake_pos[-1])
        food_spawn = False
        snake_speed += 1
        score += 10
    else:
        food_spawn = True

    if not food_spawn:
        food_pos = [random.randrange(1, WIDTH // 10) * 10, random.randrange(1, HEIGHT // 10) * 10]

    # Check for collisions
    if snake_pos[0][0] >= WIDTH or snake_pos[0][0] < 0 or snake_pos[0][1] >= HEIGHT or snake_pos[0][1] < 0:
        game_over(score)

    for block in snake_pos[1:]:
        if block == snake_pos[0]:
            game_over(score)

    # Draw the snake and food
    screen.fill(BLUE)
    for pos in snake_pos:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, GOLD, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    display_score(screen, score, highscore)

    pygame.display.flip()
    clock.tick(snake_speed)


