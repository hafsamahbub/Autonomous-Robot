import pygame
import sys
from grid import draw_grid, draw_path
from pathfinding import astar
from constants import *

# Initialize Pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Robot Pathfinding Simulation")

# Create a grid
grid = [[0 for _ in range(cols)] for _ in range(rows)]

# Set start and goal positions
start_pos = (0, 0)
goal_pos = (rows - 1, cols - 1)
grid[start_pos[0]][start_pos[1]] = 2  # Start position
grid[goal_pos[0]][goal_pos[1]] = 3    # Goal position

# Obstacles and checkpoints
obstacles = [
    (0, 3), (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6),
    (5, 5), (5, 6), (5, 7), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
    (10, 10), (10, 11), (10, 12), (10, 13), (10, 14), (11, 14),
    (12, 14), (13, 14), (14, 14), (15, 14), (16, 14), (17, 14),
    (18, 14), (18, 15), (18, 16), (17, 16), (16, 16), (15, 16),
    (14, 16), (13, 16), (13, 17), (13, 18), (14, 18), (15, 18),
    (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3), (15, 3),
    (15, 4), (15, 5), (15, 6), (15, 7), (15, 8), (16, 8), (17, 8),
    (8, 15), (8, 16), (8, 17), (8, 18), (7, 18), (6, 18), (5, 18), (4, 18)
]
for obstacle in obstacles:
    grid[obstacle[0]][obstacle[1]] = 1  # Mark obstacles

checkpoints = [(3, 3), (10, 5), (15, 10)]
for checkpoint in checkpoints:
    grid[checkpoint[0]][checkpoint[1]] = 4  # Mark checkpoints

# Pathfinding
path = astar(grid, start_pos, goal_pos)  # Calculate the path using A*
robot_position = start_pos  # Set initial robot position

# Main loop
running = True
while running:
    screen.fill(WHITE)
    draw_grid(screen, grid)  # Draw the grid
    
    if path:
        draw_path(screen, path)  # Highlight the entire path in green
        
        # Move the robot along the path
        if robot_position != goal_pos and path:
            robot_position = path.pop(0)
        
        # Draw the robot at the current position
        pygame.draw.rect(screen, BLUE, (robot_position[1] * cell_size, robot_position[0] * cell_size, cell_size, cell_size))
    
    pygame.display.flip()
    pygame.time.delay(200)  # Delay to slow down movement

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
