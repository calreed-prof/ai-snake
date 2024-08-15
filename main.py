import sys
import pygame
import time

# Start PyGame
pygame.init()

# Display Window
screen_width, screen_height = 715, 515
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake AI :)')

cell_size = 25
grid_color = (255,255,255)
highlight_color = (255,0,0)
offset = 20

def highlight_cell(column, row):
    top_left_x = offset + (column * cell_size)
    top_left_y = offset + (row * cell_size)
    pygame.draw.rect(screen, highlight_color, (top_left_x, top_left_y, cell_size, cell_size))
    pygame.display.flip()

# Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse Motion
        if event.type == pygame.MOUSEMOTION:
            x,y = event.pos

            if offset < x < screen_width-offset and offset < y < screen_height-offset:
                column = (x - offset) // cell_size
                row = (y - offset) // cell_size
                # print(column, row) # Uncomment to see the coordinates

                # Calculate the Top Left Corner of the Cell
                top_left_x = offset + (column * cell_size)
                top_left_y = offset + (row * cell_size)
                print(top_left_x, top_left_y)

                highlight_cell(column, row)

    screen.fill((0,0,0))

    for x in range(offset, screen_width-offset +1, cell_size):
        pygame.draw.line(screen, grid_color, (x, offset), (x, screen_height-offset))
    for y in range(offset, screen_height-offset +1, cell_size):
        pygame.draw.line(screen, grid_color, (offset, y), (screen_width-offset, y))

pygame.quit()
sys.exit()