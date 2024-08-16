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

# Font
font = pygame.font.Font(None, 25)

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


def get_distance_to_apple():
    snek_head_coords = (snek_head_x, snek_head_y)
    apple_coords = (apple_x, apple_y)
    distance_to_apple = abs(snek_head_coords[0] - apple_coords[0]) + abs(snek_head_coords[1] - apple_coords[1])
    return distance_to_apple

def get_distance_to_wall():
    DistToWallUp = abs(snek_head_y)
    DistToWallDown = abs(snek_head_y - 18)
    DistToWallLeft = abs(snek_head_x)
    DistToWallRight = abs(snek_head_x - 18)

    return DistToWallUp, DistToWallDown, DistToWallLeft, DistToWallRight

def check_body():
    body_up = 0
    body_down = 0
    body_left = 0
    body_right = 0

    for segment in snake[1:]:
        segment_x, segment_y = segment
        if segment_y < snek_head_y:
            body_up = 1
        elif segment_y > snek_head_y:
            body_down = 1
        elif segment_x < snek_head_x:
            body_left = 1
        elif segment_x > snek_head_x:
            body_right = 1

    return body_up, body_down, body_left, body_right

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

    # Move the snake
    current_time = time.time()
    if current_time - last_move_time > snake_speed:
        move_snake(next_direction)
        last_move_time = current_time

    # x and y are based on column and row NOT pixel position
    check_game_over()

    # Check if the snake has eaten the apple
    if snek_head_x == apple_x and snek_head_y == apple_y:
        while True:
            apple_x = random.randint(0, 18)
            apple_y = random.randint(0, 18)
            if (apple_x, apple_y) not in snake:
                break
        apple_score += 1
        snake_speed -= .0001 # Increases speed as the snake gets longer

    check_body()
    get_distance_to_wall()

    # Fill the Screen with Black
    screen.fill(background_color)

    # Draw the Grid based on the Cell Size
    for x in range(offset, screen_width - offset + 1, cell_size):
        pygame.draw.line(screen, grid_color, (x, offset + top_offset), (x, screen_height - offset))
    for y in range(offset + top_offset, screen_height - offset + 1, cell_size):
        pygame.draw.line(screen, grid_color, (offset, y), (screen_width - offset, y))

    # Score and FPS
    score_text = font.render(f"Score: {apple_score}", True, (255, 255, 255))
    screen.blit(score_text, (offset, offset))
    fps_text = font.render(f"FPS: {clock.get_fps():.0f}", True, (255, 255, 255))
    screen.blit(fps_text, (435, offset))
    dist_to_apple_text = font.render(f"Distance: {get_distance_to_apple()}", True, (255, 255, 255))
    screen.blit(dist_to_apple_text, (offset + 80, offset))

    # Draw the snake and apple
    draw_snake()
    draw_apple()

    # Update the display
    pygame.display.flip()

    # fps
    clock.tick(60)

pygame.quit()
sys.exit()
