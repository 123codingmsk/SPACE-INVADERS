import math
import random
import os
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Define asset paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), 'assets')
IMAGE_DIR = os.path.join(ASSET_DIR, 'images')
SOUND_DIR = os.path.join(ASSET_DIR, 'sounds')
FONT_DIR = os.path.join(ASSET_DIR, 'fonts')

def show_loading_screen(asset_status):
    # Create a dark background
    screen.fill((0, 0, 0))
    
    # Title
    title_font = pygame.font.SysFont(None, 48)
    title = title_font.render("Space Invaders - Loading Assets", True, (255, 255, 255))
    screen.blit(title, (400 - title.get_width()//2, 50))
    
    # Status font
    status_font = pygame.font.SysFont(None, 32)
    y_offset = 150
    
    # Show each asset's status
    for category, assets in asset_status.items():
        # Category header
        category_text = status_font.render(f"{category}:", True, (200, 200, 200))
        screen.blit(category_text, (100, y_offset))
        y_offset += 40
        
        # Individual assets
        for asset, status in assets.items():
            color = (0, 255, 0) if status else (255, 0, 0)
            status_text = "✓" if status else "✗"
            asset_text = status_font.render(f"{status_text} {asset}", True, color)
            screen.blit(asset_text, (150, y_offset))
            y_offset += 30
        
        y_offset += 20
    
    # Instructions
    if not all(status for assets in asset_status.values() for status in assets.values()):
        instruction_font = pygame.font.SysFont(None, 24)
        instruction = instruction_font.render("Press SPACE to continue with fallback graphics", True, (200, 200, 200))
        screen.blit(instruction, (400 - instruction.get_width()//2, 500))
    
    pygame.display.update()
    
    # Wait for space key if any assets are missing
    if not all(status for assets in asset_status.values() for status in assets.values()):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

def check_assets():
    required_assets = {
        "Images": {
            "background.png": os.path.exists(os.path.join(IMAGE_DIR, 'background.png')),
            "player.png": os.path.exists(os.path.join(IMAGE_DIR, 'player.png')),
            "enemy.png": os.path.exists(os.path.join(IMAGE_DIR, 'enemy.png')),
            "bullet.png": os.path.exists(os.path.join(IMAGE_DIR, 'bullet.png')),
            "ufo.png": os.path.exists(os.path.join(IMAGE_DIR, 'ufo.png'))
        },
        "Sounds": {
            "background.wav": os.path.exists(os.path.join(SOUND_DIR, 'background.wav')),
            "laser.wav": os.path.exists(os.path.join(SOUND_DIR, 'laser.wav')),
            "explosion.wav": os.path.exists(os.path.join(SOUND_DIR, 'explosion.wav'))
        },
        "Fonts": {
            "freesansbold.ttf": os.path.exists(os.path.join(FONT_DIR, 'freesansbold.ttf'))
        }
    }
    return required_assets

# Show loading screen and check assets
asset_status = check_assets()
show_loading_screen(asset_status)

def create_player_ship(size, color):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    # Draw a triangle for the ship
    points = [
        (size[0]//2, 0),  # Top point
        (0, size[1]),     # Bottom left
        (size[0], size[1]) # Bottom right
    ]
    pygame.draw.polygon(surface, color, points)
    # Add a small rectangle for the cockpit
    cockpit_color = (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255))
    pygame.draw.rect(surface, cockpit_color, (size[0]//4, size[1]//3, size[0]//2, size[1]//3))
    return surface

def create_enemy_ship(size, color):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    # Draw a hexagon for the enemy
    center = (size[0]//2, size[1]//2)
    radius = min(size[0], size[1])//2
    points = []
    for i in range(6):
        angle = math.pi/3 * i
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)
    # Add eyes
    eye_color = (255, 255, 255)
    eye_radius = radius//4
    pygame.draw.circle(surface, eye_color, (center[0]-radius//3, center[1]-radius//3), eye_radius)
    pygame.draw.circle(surface, eye_color, (center[0]+radius//3, center[1]-radius//3), eye_radius)
    return surface

def create_bullet(size, color):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    # Draw a laser beam
    pygame.draw.rect(surface, color, (size[0]//4, 0, size[0]//2, size[1]))
    # Add glow effect
    glow_color = (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255))
    pygame.draw.rect(surface, glow_color, (size[0]//3, 0, size[0]//3, size[1]))
    return surface

def create_background(size, color):
    surface = pygame.Surface(size)
    surface.fill(color)
    # Add stars
    for _ in range(100):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        brightness = random.randint(100, 255)
        pygame.draw.circle(surface, (brightness, brightness, brightness), (x, y), 1)
    return surface

def load_image(filename, default_color=(255, 255, 255)):
    try:
        return pygame.image.load(os.path.join(IMAGE_DIR, filename))
    except FileNotFoundError:
        # Create sophisticated fallback graphics
        if filename == 'background.png':
            return create_background((800, 600), (0, 0, 0))
        elif filename == 'player.png':
            return create_player_ship((64, 64), (0, 255, 0))
        elif filename == 'enemy.png':
            return create_enemy_ship((64, 64), (255, 0, 0))
        elif filename == 'bullet.png':
            return create_bullet((32, 32), (255, 255, 0))
        elif filename == 'ufo.png':
            return create_enemy_ship((64, 64), (0, 0, 255))
        else:
            # Default fallback for any other image
            surface = pygame.Surface((64, 64), pygame.SRCALPHA)
            surface.fill(default_color)
            return surface

def load_sound(filename):
    try:
        return mixer.Sound(os.path.join(SOUND_DIR, filename))
    except FileNotFoundError:
        print(f"Warning: Sound file {filename} not found")
        return None

def load_font(filename, size):
    try:
        return pygame.font.Font(os.path.join(FONT_DIR, filename), size)
    except FileNotFoundError:
        print(f"Warning: Font file {filename} not found, using system font")
        return pygame.font.SysFont(None, size)

# Background
background = load_image('background.png', (0, 0, 0))

# Sound
try:
    mixer.music.load(os.path.join(SOUND_DIR, "background.wav"))
    mixer.music.play(-1)
except FileNotFoundError:
    print("Warning: Background music not found")

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = load_image('ufo.png', (0, 0, 255))
pygame.display.set_icon(icon)

# Player
playerImg = load_image('player.png', (0, 255, 0))
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(load_image('enemy.png', (255, 0, 0)))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(20)

# Bullet
bulletImg = load_image('bullet.png', (255, 255, 0))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
high_score = 0
font = load_font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = load_font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    high_score_text = font.render("High Score : " + str(high_score), True, (255, 255, 255))
    screen.blit(score, (x, y))
    screen.blit(high_score_text, (x, y + 40))

def game_over_text():
    global high_score
    
    # Update high score if current score is higher
    if score_value > high_score:
        high_score = score_value
    
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    score_text = font.render(f"Final Score: {score_value}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    retry_text = font.render("Press R to Retry", True, (255, 255, 255))
    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))
    
    screen.blit(over_text, (400 - over_text.get_width()//2, 150))
    screen.blit(score_text, (400 - score_text.get_width()//2, 250))
    screen.blit(high_score_text, (400 - high_score_text.get_width()//2, 300))
    screen.blit(retry_text, (400 - retry_text.get_width()//2, 350))
    screen.blit(quit_text, (400 - quit_text.get_width()//2, 400))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Retry
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()
    return False

def reset_game():
    global playerX, playerY, playerX_change
    global enemyX, enemyY, enemyX_change, enemyY_change
    global bulletX, bulletY, bullet_state
    global score_value
    
    # Reset player
    playerX = 370
    playerY = 480
    playerX_change = 0
    
    # Reset enemies
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 736)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = 2
        enemyY_change[i] = 20
    
    # Reset bullet
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    
    # Reset score
    score_value = 0

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = load_sound("laser.wav")
                    if bulletSound:
                        bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    game_over = False
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            if game_over_text():  # If retry is selected
                reset_game()
                break
            else:
                running = False
                break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = load_sound("explosion.wav")
            if explosionSound:
                explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
