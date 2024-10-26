import pygame
import sys
import heapq

# Initialize Pygame
pygame.init()

# Screen settings
screen_width, screen_height = 600, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Robot Pathfinding Simulation")

# Grid settings
cols, rows = 20, 20  # Grid size
cell_size = screen_width // cols

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)   # Robot
RED = (255, 0, 0)     # Goal
GRAY = (200, 200, 200) # Obstacles
GREEN = (0, 255, 0)   # Path
#YELLOW = (255, 255, 0) # Checkpoints

# Create a grid
grid = [[0 for _ in range(cols)] for _ in range(rows)]

# Set start and goal positions
start_pos = (0, 0)
goal_pos = (rows - 1, cols - 1)
grid[start_pos[0]][start_pos[1]] = 2  # Start position
grid[goal_pos[0]][goal_pos[1]] = 3    # Goal position

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

# Add checkpoints
checkpoints = [(3, 3), (10, 5), (15, 10)]
for checkpoint in checkpoints:
    grid[checkpoint[0]][checkpoint[1]] = 4  # Mark checkpoints

def draw_grid():
    for row in range(rows):
        for col in range(cols):
            color = WHITE
            if grid[row][col] == 1:  # Obstacle
                color = GRAY
            elif grid[row][col] == 2:  # Start
                color = BLUE
            elif grid[row][col] == 3:  # Goal
                color = RED
            #elif grid[row][col] == 4:  # Checkpoint
                #color = YELLOW
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size), 1)

# A* Pathfinding Algorithm
def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = { (row, col): float("inf") for row in range(rows) for col in range(cols) }
    g_score[start] = 0
    f_score = { (row, col): float("inf") for row in range(rows) for col in range(cols) }
    f_score[start] = heuristic(start, goal)

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            return reconstruct_path(came_from, current)

        neighbors = get_neighbors(current, rows, cols)
        for neighbor in neighbors:
            if grid[neighbor[0]][neighbor[1]] == 1:  # Skip obstacles
                continue

            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found

# Heuristic function for A* (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Get neighbors of a cell in the grid
def get_neighbors(pos, rows, cols):
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, down, left, right
        x, y = pos[0] + dx, pos[1] + dy
        if 0 <= x < rows and 0 <= y < cols:
            neighbors.append((x, y))
    return neighbors

# Reconstruct the path from start to goal
def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# Draw the path
def draw_path(path):
    for cell in path:
        pygame.draw.rect(screen, GREEN, (cell[1] * cell_size, cell[0] * cell_size, cell_size, cell_size))

# Main loop
running = True
path = astar(grid, start_pos, goal_pos)  # Calculate the path using A*
robot_position = start_pos  # Set initial robot position

while running:
    screen.fill(WHITE)
    draw_grid()
    
    if path:
        #draw_path(path)  # Highlight the entire path in green
        
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