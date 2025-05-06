import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Original screen dimensions
ORIGINAL_SCREEN_WIDTH = 800
ORIGINAL_SCREEN_HEIGHT = 600

# New screen dimensions (half the original size)
SCREEN_WIDTH = ORIGINAL_SCREEN_WIDTH // 2
SCREEN_HEIGHT = ORIGINAL_SCREEN_HEIGHT // 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
WATER_BLUE = (0, 119, 190)

# Player properties
player_width = 25
player_height = 5
player_speed = 5
wheel_radius = 10
nozzle_width = 5
nozzle_height = 10

# Bullet properties
bullet_width = 3
bullet_height = 5
bullet_speed = 7
bullets = []

# Object properties
object_radius = 10
object_speed = 1  # Slower speed for level 1
objects = []

# Level properties
level = 1
objects_dropped = 0
objects_cleared = 0
objects_to_clear_current_level = 5
object_spawn_rate = 100  # Start with slowest rate

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 50))  # Extra space for buttons
pygame.display.set_caption("Falling Objects Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Smallest font
font = pygame.font.Font(None, 12)

# Game control flags
game_active = False
game_paused = False
game_over = False

# Function to draw water-like ground
def draw_water():
    pygame.draw.rect(screen, WATER_BLUE, (0, SCREEN_HEIGHT - 30, SCREEN_WIDTH, 30))

# Function to draw the player
def draw_player(x, y):
    pygame.draw.rect(screen, RED, (x, y, player_width, player_height))
    pygame.draw.circle(screen, BLACK, (x + player_width // 2, y + player_height + wheel_radius), wheel_radius, 2)
    for angle in range(0, 360, 45):
        dx = int(wheel_radius * math.cos(math.radians(angle)))
        dy = int(wheel_radius * math.sin(math.radians(angle)))
        pygame.draw.line(screen, BLACK, (x + player_width // 2, y + player_height + wheel_radius), 
                         (x + player_width // 2 + dx, y + player_height + wheel_radius + dy), 2)
    pygame.draw.rect(screen, BLACK, (x + player_width // 2 - nozzle_width // 2, y - nozzle_height, nozzle_width, nozzle_height))

# Function to draw a bullet
def draw_bullet(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, bullet_width, bullet_height))

# Function to draw a falling object resembling a coronavirus shape
def draw_object(x, y):
    pygame.draw.circle(screen, GREEN, (x, y), object_radius)
    for angle in range(0, 360, 30):
        dx = int(object_radius * 1.5 * math.cos(math.radians(angle)))
        dy = int(object_radius * 1.5 * math.sin(math.radians(angle)))
        pygame.draw.circle(screen, GREEN, (x + dx, y + dy), 3)

# Function to update the level
def update_level():
    global level, object_speed, object_spawn_rate, objects_to_clear_current_level, player_speed
    level += 1
    object_speed = level  # Increase speed with each level
    player_speed = 5 + level  # Increase player speed with each level
    object_spawn_rate = max(10, 100 - 10 * level)  # Increase spawn rate
    objects_to_clear_current_level = 5 * level

# Function to display text on the screen
def display_text(text, x, y, size=12):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))

# Function to draw buttons
def draw_buttons(buttons):
    button_rects = []
    for i, (text, x, y, width, height) in enumerate(buttons):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, GRAY, rect)
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (rect.x + (width - text_surface.get_width()) // 2, rect.y + (height - text_surface.get_height()) // 2))
        button_rects.append(rect)
    return button_rects

# Function to reset the game
def reset_game():
    global objects, bullets, objects_dropped, objects_cleared, score, level, object_speed, object_spawn_rate, game_active, game_paused, game_over
    objects.clear()
    bullets.clear()
    objects_dropped = 0
    objects_cleared = 0
    score = 0
    level = 1
    object_speed = 1
    object_spawn_rate = 100
    game_active = True
    game_paused = False
    game_over = False

# Main game loop
def game_loop():
    global objects_dropped, objects_cleared, object_speed, object_spawn_rate, game_active, game_paused, game_over, score

    # Player position
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - 50  # Floating above the water

    # Score
    score = 0

    # Main loop flag
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if game_over:
                    buttons = [("Start", 75, SCREEN_HEIGHT // 2 + 40, 75, 22), ("End", 225, SCREEN_HEIGHT // 2 + 40, 75, 22)]
                else:
                    buttons = [("Start", 37, SCREEN_HEIGHT + 10, 75, 22), ("Pause", 117, SCREEN_HEIGHT + 10, 75, 22), ("Restart", 197, SCREEN_HEIGHT + 10, 75, 22), ("End", 277, SCREEN_HEIGHT + 10, 75, 22)]
                
                button_rects = draw_buttons(buttons)

                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):
                        if buttons[i][0] == "Start":
                            reset_game()
                        elif buttons[i][0] == "Pause":
                            game_paused = not game_paused
                        elif buttons[i][0] == "Restart":
                            reset_game()
                        elif buttons[i][0] == "End":
                            running = False

        # Get the list of keys pressed
        keys = pygame.key.get_pressed()

        if game_active and not game_paused:
            # Move the player left and right
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
                player_x += player_speed

            # Draw the borders
            pygame.draw.rect(screen, BLUE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

            # Draw the water-like ground
            draw_water()

            # Draw the player
            draw_player(player_x, player_y)

            # Automatically fire bullets
            if len(bullets) == 0 or bullets[-1][1] < SCREEN_HEIGHT - 100:
                bullets.append([player_x + player_width // 2, player_y - nozzle_height])

            # Draw and move bullets
            for bullet in bullets[:]:
                bullet[1] -= bullet_speed
                if bullet[1] < 0:
                    bullets.remove(bullet)
                draw_bullet(bullet[0], bullet[1])

            # Add a new object at random x position
            if objects_dropped < objects_to_clear_current_level and random.randint(1, object_spawn_rate) == 1:
                obj_x = random.randint(0, SCREEN_WIDTH - object_radius * 2)
                objects.append([obj_x, 0])
                objects_dropped += 1

            # Move objects down and check for collisions
            for obj in objects[:]:
                obj[1] += object_speed
                if obj[1] > SCREEN_HEIGHT - 30:  # Water-level height
                    game_over = True
                    game_active = False
                    break
                for bullet in bullets[:]:
                    if math.hypot(bullet[0] - (obj[0] + object_radius), bullet[1] - (obj[1] + object_radius)) < object_radius:
                        objects.remove(obj)
                        bullets.remove(bullet)
                        score += 1
                        objects_cleared += 1
                        if objects_cleared >= objects_to_clear_current_level:
                            update_level()
                            objects_dropped = 0
                            objects_cleared = 0
                        break
                draw_object(obj[0] + object_radius, obj[1] + object_radius)

            # Display the score
            display_text(f"Score: {score}", 10, 10)

        if game_over:
            display_text("Game Over", SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 - 40, size=36)
            display_text(f"Final Score: {score}", SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2, size=24)
            buttons = [("Start", 75, SCREEN_HEIGHT // 2 + 40, 75, 22), ("End", 225, SCREEN_HEIGHT // 2 + 40, 75, 22)]
            button_rects = draw_buttons(buttons)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(mouse_pos):
                            if buttons[i][0] == "Start":
                                reset_game()
                            elif buttons[i][0] == "End":
                                running = False
        else:
            # Draw buttons
            buttons = [("Start", 37, SCREEN_HEIGHT + 10, 75, 22), ("Pause", 117, SCREEN_HEIGHT + 10, 75, 22), ("Restart", 197, SCREEN_HEIGHT + 10, 75, 22), ("End", 277, SCREEN_HEIGHT + 10, 75, 22)]
            draw_buttons(buttons)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

    pygame.quit()

# Run the game
game_loop()