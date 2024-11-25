import pygame
from constants import *

# Draw the grid
def draw_grid(screen, grid):
    for row in range(rows):
        for col in range(cols):
            color = WHITE
            if grid[row][col] == 1:  # Obstacle
                color = GRAY
            elif grid[row][col] == 2:  # Start
                color = BLUE
            elif grid[row][col] == 3:  # Goal
                color = RED
            elif grid[row][col] == 4:  # Checkpoint
                color = YELLOW
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size), 1)

# Draw the path
def draw_path(screen, path):
    for cell in path:
        pygame.draw.rect(screen, GREEN, (cell[1] * cell_size, cell[0] * cell_size, cell_size, cell_size))
