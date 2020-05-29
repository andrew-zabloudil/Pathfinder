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

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
TEXT_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (35, 235, 35)
PATHFINDING_COLOR = (35, 35, 235)
NODE_COLORS = [(235, 35, 35), (235, 235, 35)]
GRID_SIZE = 20


def terminate():
    pygame.quit()
    sys.exit()


def draw_wall(pos):
    x_grid = int(pos[0] / 20) * 20
    y_grid = int(pos[1] / 20) * 20
    wall_vertex = (x_grid, y_grid)
    wall_vertices.append(wall_vertex)
    wall_rect = pygame.Rect(x_grid, y_grid, GRID_SIZE, GRID_SIZE)
    walls.append(wall_rect)


def draw_node(pos):
    x_grid = int(pos[0] / 20) * 20
    y_grid = int(pos[1] / 20) * 20
    if can_draw_start == True:
        nodes[0] = (x_grid, y_grid)
        node_rect[0] = pygame.Rect(x_grid, y_grid, GRID_SIZE, GRID_SIZE)

    if can_draw_end == True:
        nodes[1] = (x_grid, y_grid)
        node_rect[1] = pygame.Rect(x_grid, y_grid, GRID_SIZE, GRID_SIZE)


def find_path(nodes, wall_vertices, choice):
    if choice == "Dijkstra":
        return Dijkstra(nodes, wall_vertices, WINDOW_WIDTH, WINDOW_HEIGHT)


def draw_path(path):
    for vertex in path:
        path_rect = pygame.Rect(vertex[0], vertex[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(window_surface, PATH_COLOR, path_rect)


pygame.init()
can_draw_wall = True
drawing_wall = False
can_draw_start = False
can_draw_end = False
walls = []
wall_vertices = []
path = {}
nodes = [None, None]
node_rect = [None, None]
algorithm_choice = "Dijkstra"

# Set up window surface
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pathfinder")
pygame.mouse.set_visible(True)
font = pygame.font.SysFont(None, 48)


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
