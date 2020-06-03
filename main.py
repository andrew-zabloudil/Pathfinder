#! python3

"""
This progam displays the visual component of a pathfinding program.
The program allows users to click on squares to color them in and create
obstacles for a pathfinding algorithm to work around.
"""

import sys
import pygame
from pygame.locals import *
from algorithms.dijkstra import Dijkstra
from algorithms.dijkstra_visual import Dijkstra_visual

"""
A class to easily set up buttons.
"""


class Button():
    def __init__(self, pos, size, label):
        self.pos = pos
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.size = size
        self.label = label
        self.pressed = False

        self.button_rect = pygame.Rect(self.pos, self.size)
        self.button_text = font.render(
            self.label, True, TEXT_COLOR, BUTTON_COLOR)
        self.button_text_rect = self.button_text.get_rect()
        self.button_text_rect.centerx = self.button_rect.centerx
        self.button_text_rect.centery = self.button_rect.centery
        self.button_pos = []
        for x in range(self.x_pos, self.x_pos + self.size[0]):
            for y in range(self.y_pos, self.y_pos + self.size[1]):
                self.button_pos.append((x, y))

        self.button_img = pygame.image.load('img/button.png')
        self.button_pressed_img = pygame.image.load('img/button_pressed.png')

    def draw_button(self):
        if self.pressed == False:
            self.button_text = font.render(
                self.label, True, TEXT_COLOR, BUTTON_COLOR)
            window_surface.blit(self.button_img, self.button_rect)
            window_surface.blit(self.button_text, self.button_text_rect)
        else:
            self.button_text = font.render(
                self.label, True, TEXT_COLOR, BUTTON_PRESSED_COLOR)
            window_surface.blit(self.button_pressed_img, self.button_rect)
            window_surface.blit(self.button_text, self.button_text_rect)


# Terminates the program.

def terminate():
    pygame.quit()
    sys.exit()

# Creates or removes a wall block at the designated position.


def draw_wall(pos):
    global path
    x_grid = int(pos[0] / GRID_SIZE) * GRID_SIZE
    y_grid = int(pos[1] / GRID_SIZE) * GRID_SIZE
    if y_grid < WINDOW_HEIGHT:
        wall_vertex = (x_grid, y_grid)
        wall_rect = pygame.Rect(x_grid, y_grid, GRID_SIZE, GRID_SIZE)
        if can_draw_wall == True:
            if wall_vertex not in wall_vertices:
                wall_vertices.append(wall_vertex)
                walls.append(wall_rect)
                path = []
        elif can_erase_wall == True:
            if wall_vertex in wall_vertices:
                wall_vertices.remove(wall_vertex)
                walls.remove(wall_rect)
                path = []
    else:
        return


# Creates the start and end nodes.


def draw_node(pos):
    global path
    x_grid = int(pos[0] / GRID_SIZE) * GRID_SIZE
    y_grid = int(pos[1] / GRID_SIZE) * GRID_SIZE
    if y_grid < WINDOW_HEIGHT:
        if can_draw_start == True:
            nodes[0] = (x_grid, y_grid)
            node_rect[0] = pygame.Rect(x_grid, y_grid, GRID_SIZE, GRID_SIZE)
            path = []

        if can_draw_end == True:
            nodes[1] = (x_grid, y_grid)
            node_rect[1] = pygame.Rect(x_grid, y_grid, GRID_SIZE, GRID_SIZE)
            path = []
    else:
        return

# Finds the shortest path based on the chosen algorithm.


def find_path(nodes, wall_vertices):
    if visualize_solver == False:
        return Dijkstra(nodes, wall_vertices, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE)
    else:
        return Dijkstra_visual(nodes, wall_vertices, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, window_surface)

# Draws the shortest path found in find_path


def draw_path(path):
    for vertex in path:
        path_rect = pygame.Rect(vertex[0], vertex[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(window_surface, PATH_COLOR, path_rect)

# Creates a light grid in the drawing space for ease of use.


def draw_grid():
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(window_surface, GRID_COLOR,
                         (x, 0), (x, WINDOW_HEIGHT), 1)
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(window_surface, GRID_COLOR,
                         (0, y), (WINDOW_WIDTH, y), 1)

# Displays a message if solve is clicked without a start and end node.


def display_error():
    error_text = font.render(
        "Select a start and an end node first.", True, TEXT_COLOR, ERROR_COLOR)
    error_text_rect = error_text.get_rect()
    error_text_rect.centerx = int(WINDOW_WIDTH / 2)
    error_text_rect.centery = int(WINDOW_HEIGHT / 2)
    window_surface.blit(error_text, error_text_rect)


"""
This block defines constants.
"""
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
BANNER_HEIGHT = 175
GRID_SIZE = 20
BUTTON_SIZE = (200, 50)

TEXT_COLOR = (250, 250, 250)
BACKGROUND_COLOR = (240, 240, 240)
BANNER_COLOR = (220, 220, 220)
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (35, 235, 35)
PATHFINDING_COLOR = (35, 35, 235)
NODE_COLORS = [(235, 35, 35), (235, 235, 35)]
BUTTON_COLOR = (40, 120, 200)
BUTTON_PRESSED_COLOR = (30, 60, 180)
GRID_COLOR = (200, 200, 200)
ERROR_COLOR = (230, 23, 23)

pygame.init()

# Sets default settings.
can_draw_wall = True
drawing_wall = False
can_erase_wall = False
can_draw_start = False
can_draw_end = False
visualize_solver = False
display_error_message = False


# Prepares empty structures to be used in later functions.
buttons = []
walls = []
wall_vertices = []
path = {}
nodes = [None, None]
node_rect = [None, None]


# Sets up display window and surfaces

pygame.display.set_caption("Pathfinder")
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)
pygame.mouse.set_visible(True)
font = pygame.font.SysFont(None, 42)

window_surface = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT + BANNER_HEIGHT))
banner_surface = pygame.Surface((WINDOW_WIDTH, BANNER_HEIGHT))
window_surface.blit(banner_surface, (0, WINDOW_HEIGHT))

# Creates the buttons

start_node_button = Button(
    (40, WINDOW_HEIGHT + 25),
    BUTTON_SIZE,
    "Place Start"
)
end_node_button = Button(
    (40, WINDOW_HEIGHT + BANNER_HEIGHT - 25 - BUTTON_SIZE[1]),
    BUTTON_SIZE,
    "Place End"
)
place_wall_button = Button(
    (BUTTON_SIZE[0] + 80, WINDOW_HEIGHT + 25),
    BUTTON_SIZE,
    "Place Walls"
)
erase_wall_button = Button(
    (BUTTON_SIZE[0] + 80, WINDOW_HEIGHT + BANNER_HEIGHT - 25 - BUTTON_SIZE[1]),
    BUTTON_SIZE,
    "Erase Walls"
)
solve_button = Button(
    (WINDOW_WIDTH - BUTTON_SIZE[0] - 40, WINDOW_HEIGHT + 25),
    BUTTON_SIZE,
    "Solve"
)
visualize_button = Button(
    (WINDOW_WIDTH - BUTTON_SIZE[0] - 40,
     WINDOW_HEIGHT + BANNER_HEIGHT - 25 - BUTTON_SIZE[1]),
    BUTTON_SIZE,
    "Visualize"
)

# Main Loop

while True:
    for event in pygame.event.get():
        # Quits the program.
        if event.type == QUIT:
            terminate()
        if event.type == MOUSEBUTTONDOWN:
            if event.pos in start_node_button.button_pos:
                can_draw_start = True
                can_draw_wall = False
                can_draw_end = False
                can_erase_wall = False
                display_error_message = False
                start_node_button.pressed = True
                end_node_button.pressed = False
                place_wall_button.pressed = False
                erase_wall_button.pressed = False
            elif event.pos in end_node_button.button_pos:
                can_draw_start = False
                can_draw_wall = False
                can_draw_end = True
                can_erase_wall = False
                display_error_message = False
                start_node_button.pressed = False
                end_node_button.pressed = True
                place_wall_button.pressed = False
                erase_wall_button.pressed = False
            elif event.pos in place_wall_button.button_pos:
                can_draw_start = False
                can_draw_wall = True
                can_draw_end = False
                can_erase_wall = False
                display_error_message = False
                start_node_button.pressed = False
                end_node_button.pressed = False
                place_wall_button.pressed = True
                erase_wall_button.pressed = False
            elif event.pos in erase_wall_button.button_pos:
                can_draw_start = False
                can_draw_wall = False
                can_draw_end = False
                can_erase_wall = True
                display_error_message = False
                start_node_button.pressed = False
                end_node_button.pressed = False
                place_wall_button.pressed = False
                erase_wall_button.pressed = True
            elif event.pos in solve_button.button_pos:
                if nodes[0] != None and nodes[1] != None:
                    display_error_message = False
                    path = find_path(nodes, wall_vertices)
                else:
                    display_error_message = True
            elif event.pos in visualize_button.button_pos:
                if visualize_solver == False:
                    display_error_message = False
                    visualize_solver = True
                    visualize_button.pressed = True
                else:
                    display_error_message = False
                    visualize_solver = False
                    visualize_button.pressed = False

            if can_draw_wall == True:
                drawing_wall = True
                draw_wall(event.pos)
            if can_erase_wall == True:
                drawing_wall = True
                draw_wall(event.pos)
            if can_draw_start == True or can_draw_end == True:
                draw_node(event.pos)
        if event.type == MOUSEBUTTONUP:
            drawing_wall = False
        if event.type == MOUSEMOTION:
            if drawing_wall:
                draw_wall(event.pos)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()

    # Draws the window.
    window_surface.fill(BACKGROUND_COLOR)
    window_surface.blit(banner_surface, (0, WINDOW_HEIGHT))
    banner_surface.fill(BANNER_COLOR)
    pygame.draw.line(window_surface, (180, 180, 180),
                     (0, WINDOW_HEIGHT), (WINDOW_WIDTH, WINDOW_HEIGHT), 2)
    draw_grid()

    # Draws the buttons to the surface.
    start_node_button.draw_button()
    end_node_button.draw_button()
    place_wall_button.draw_button()
    erase_wall_button.draw_button()
    solve_button.draw_button()
    visualize_button.draw_button()

    # Draws the path taken or displays an error message.
    if path:
        draw_path(path)
    elif display_error_message == True:
        display_error()

    # Draws start and end nodes.
    for i, node in enumerate(node_rect):
        if node != None:
            pygame.draw.rect(window_surface, NODE_COLORS[i], node)

    # Draws the walls onto the screen.
    for wall in walls:
        pygame.draw.rect(window_surface, WALL_COLOR, wall)

    # Updates the display.
    pygame.display.update()
