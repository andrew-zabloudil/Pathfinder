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

    def draw_button(self):
        pygame.draw.rect(window_surface, BUTTON_COLOR, self.button_rect)
        window_surface.blit(self.button_text, self.button_text_rect)


# Terminates the program.

def terminate():
    pygame.quit()
    sys.exit()

# Creates a wall block at the designated position.


def draw_wall(pos):
    x_grid = int(pos[0] / 20) * 20
    y_grid = int(pos[1] / 20) * 20
    if y_grid < WINDOW_HEIGHT:
        wall_vertex = (x_grid, y_grid)
        wall_vertices.append(wall_vertex)
        wall_rect = pygame.Rect(x_grid, y_grid, GRID_SIZE, GRID_SIZE)
        walls.append(wall_rect)
    else:
        return

# Creates the start and end nodes.


def draw_node(pos):
    x_grid = int(pos[0] / 20) * 20
    y_grid = int(pos[1] / 20) * 20
    if y_grid < WINDOW_HEIGHT:
        if can_draw_start == True:
            nodes[0] = (x_grid, y_grid)
            node_rect[0] = pygame.Rect(x_grid, y_grid, GRID_SIZE, GRID_SIZE)

        if can_draw_end == True:
            nodes[1] = (x_grid, y_grid)
            node_rect[1] = pygame.Rect(x_grid, y_grid, GRID_SIZE, GRID_SIZE)
    else:
        return

# Finds the shortest path based on the chosen algorithm.


def find_path(nodes, wall_vertices, choice):
    if choice == "Dijkstra":
        return Dijkstra(nodes, wall_vertices, WINDOW_WIDTH, WINDOW_HEIGHT)

# Draws the shortest path found in find_path


def draw_path(path):
    for vertex in path:
        path_rect = pygame.Rect(vertex[0], vertex[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(window_surface, PATH_COLOR, path_rect)


""" 
This block defines constants.
"""
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
BANNER_HEIGHT = 250
TEXT_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)
BANNER_COLOR = (45, 220, 100)
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (35, 235, 35)
PATHFINDING_COLOR = (35, 35, 235)
NODE_COLORS = [(235, 35, 35), (235, 235, 35)]
GRID_SIZE = 20
BUTTON_COLOR = (220, 90, 50)
BUTTON_SIZE = (200, 50)


pygame.init()

# Sets default settings.
can_draw_wall = True
drawing_wall = False
can_draw_start = False
can_draw_end = False
algorithm_choice = "Dijkstra"


# Prepares empty structures to be used in later functions.
buttons = []
walls = []
wall_vertices = []
path = {}
nodes = [None, None]
node_rect = [None, None]


# Sets up window surface
window_surface = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT + BANNER_HEIGHT))
banner_surface = pygame.Surface((WINDOW_WIDTH, BANNER_HEIGHT))
window_surface.blit(banner_surface, (0, WINDOW_HEIGHT))

pygame.display.set_caption("Pathfinder")
pygame.mouse.set_visible(True)
font = pygame.font.SysFont(None, 48)

start_node_button = Button((100, 625), BUTTON_SIZE, "Place Start")
end_node_button = Button((100, 700), BUTTON_SIZE, "Place End")
place_wall_button = Button((100, 775), BUTTON_SIZE, "Place Walls")


# Main Loop

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_1:
                can_draw_start = True
                can_draw_wall = False
                can_draw_end = False
            if event.key == K_2:
                can_draw_start = False
                can_draw_wall = False
                can_draw_end = True
            if event.key == K_3:
                can_draw_start = False
                can_draw_wall = True
                can_draw_end = False
            if event.key == K_RETURN:
                path = find_path(nodes, wall_vertices, algorithm_choice)
        if event.type == MOUSEBUTTONDOWN:
            if event.pos in start_node_button.button_pos:
                can_draw_start = True
                can_draw_wall = False
                can_draw_end = False
            if event.pos in end_node_button.button_pos:
                can_draw_start = False
                can_draw_wall = False
                can_draw_end = True
            elif event.pos in place_wall_button.button_pos:
                can_draw_start = False
                can_draw_wall = True
                can_draw_end = False
            if can_draw_wall == True:
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

    window_surface.fill(BACKGROUND_COLOR)
    window_surface.blit(banner_surface, (0, WINDOW_HEIGHT))
    banner_surface.fill(BANNER_COLOR)

    start_node_button.draw_button()
    end_node_button.draw_button()
    place_wall_button.draw_button()

    # Draws the path taken
    if path:
        draw_path(path)

    # Draws start and end nodes.
    for i, node in enumerate(node_rect):
        if node != None:
            pygame.draw.rect(window_surface, NODE_COLORS[i], node)

    # Draws the walls onto the screen.
    for wall in walls:
        pygame.draw.rect(window_surface, WALL_COLOR, wall)

    pygame.display.update()
