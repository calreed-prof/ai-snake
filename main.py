import sys
import pygame
import time
import random

# Start PyGame
pygame.init()

# Display Window
screen_width, screen_height = 515, 545
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake AI :)')

# Grid / Should not be changed
cell_size = 25
grid_color = (255, 255, 255)
highlight_color = (255, 0, 0)
background_color = (0, 0, 0)
offset = 20
top_offset = 30  # Additional offset for the top

# These need to be flipped because the grid is flipped
NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)

# Snake starting position
snek_head_x = 10
snek_head_y = 10
started = True
current_direction = NORTH
next_direction = NORTH

# Apple starting position
apple_x = random.randint(0, 18)
apple_y = random.randint(0, 18)
apple_score = 0

snake = [(snek_head_x, snek_head_y)]

def draw_snake():
    # This is translating the x and y to the pixel position
    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0), (segment[0] * cell_size + offset, segment[1] * cell_size + offset + top_offset, cell_size, cell_size))

def check_direction_rules(next_direction):
    if next_direction == NORTH and current_direction == SOUTH:
        return False
    if next_direction == SOUTH and current_direction == NORTH:
        return False
    if next_direction == EAST and current_direction == WEST:
        return False
    if next_direction == WEST and current_direction == EAST:
        return False
    return True

def move_snake(next_direction):
    global snek_head_x, snek_head_y, current_direction
    current_direction = next_direction
    snek_head_x += current_direction[0]
    snek_head_y += current_direction[1]

    # Add the new snake head to the snake
    new_snake_head = (snek_head_x, snek_head_y)
    snake.append(new_snake_head)
    if not (snek_head_x == apple_x and snek_head_y == apple_y):
        snake.pop(0)

def draw_apple():
    pygame.draw.rect(screen, (255, 0, 0), (apple_x * cell_size + offset, apple_y * cell_size + offset + top_offset, cell_size, cell_size))

def check_game_over():
    if snek_head_x == -1 or snek_head_x > 18 or snek_head_y == -1 or snek_head_y > 18:
        print("Game over")
        pygame.quit()
        sys.exit()

    if len(snake) != len(set(snake)):
        print("Game over")
        pygame.quit()
        sys.exit()

# Loop
clock = pygame.time.Clock()
running = True

# Snake movement
snake_speed = .1  # in seconds
last_move_time = time.time()

key_buffer = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                key_buffer = NORTH
            if event.key == pygame.K_s:
                key_buffer = SOUTH
            if event.key == pygame.K_a:
                key_buffer = WEST
            if event.key == pygame.K_d:
                key_buffer = EAST

    # Check if the key buffer is not None and if the direction is valid
    if key_buffer and check_direction_rules(key_buffer):
        next_direction = key_buffer
        key_buffer = None  # clear the key buffer

    current_time = time.time()
    if current_time - last_move_time > snake_speed:
        move_snake(next_direction)
        last_move_time = current_time

    if snek_head_x == apple_x and snek_head_y == apple_y:
        while True:
            apple_x = random.randint(0, 18)
            apple_y = random.randint(0, 18)
            if (apple_x, apple_y) not in snake:
                break
        apple_score += 1

    # x and y are based on column and row NOT pixel position
    check_game_over()

    # Fill the Screen with Black
    screen.fill(background_color)
    # Draw the Grid based on the Cell Size
    for x in range(offset, screen_width - offset + 1, cell_size):
        pygame.draw.line(screen, grid_color, (x, offset + top_offset), (x, screen_height - offset))
    for y in range(offset + top_offset, screen_height - offset + 1, cell_size):
        pygame.draw.line(screen, grid_color, (offset, y), (screen_width - offset, y))

    draw_snake()
    draw_apple()
    pygame.display.flip()

    # fps
    clock.tick(60)

    # fps = clock.get_fps()
    # print(f"FPS: {fps:.2f}")

pygame.quit()
sys.exit()
