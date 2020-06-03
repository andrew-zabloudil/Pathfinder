"""
Uses Dijkstra's algorithm to solve a pathfinding problem generated by a user.
Visualizes the algorithm as it runs.
"""

import pygame
import pygame.time
from pygame.locals import *

PATHFINDING_COLOR = (35, 35, 235)
pathfinding = []


def draw_pathfinding(vertex, GRID_SIZE, window_surface):
    pathfinding_rect = pygame.Rect(vertex[0], vertex[1], GRID_SIZE, GRID_SIZE)
    pathfinding.append(pathfinding_rect)
    for rectangle in pathfinding:
        pygame.draw.rect(window_surface, PATHFINDING_COLOR, rectangle)
    pygame.display.update()


def Dijkstra_visual(nodes, walls, WIDTH, HEIGHT, GRID_SIZE, window_surface):
    start = nodes[0]
    end = nodes[1]

    dist = {}
    Q = []
    path = []

    try:
        for x in range(0, WIDTH, GRID_SIZE):
            for y in range(0, HEIGHT, GRID_SIZE):
                vertex = (x, y)
                Q.append(vertex)
                if vertex != start:
                    dist[vertex] = 1000000
                else:
                    dist[vertex] = 0

        while len(Q) != 0:
            if start in Q:
                v = start
            else:
                min_dist = 1000000
                for vertex in Q:
                    if dist[vertex] < min_dist and dist[vertex] > 0:
                        min_dist = dist[vertex]
                        v = vertex
            if v in Q:
                Q.remove(v)
            else:
                break

            neighbor_offsets = [
                (GRID_SIZE, 0),
                (-GRID_SIZE, 0),
                (0, GRID_SIZE),
                (0, -GRID_SIZE)
            ]

            if v == end:
                while v != start:
                    min_dist = 1000000
                    v_temp = v
                    for offset in neighbor_offsets:
                        try:
                            u = (v[0] + offset[0], v[1] + offset[1])
                            if (dist[u] < min_dist) and (u not in walls):
                                min_dist = dist[u]
                                v_temp = u
                        except:
                            continue
                    v = v_temp
                    path.append(v)
                if v == start:
                    global pathfinding
                    pathfinding = []
                    return path

            for offset in neighbor_offsets:
                u = (v[0] + offset[0], v[1] + offset[1])
                if u in Q and u not in walls:
                    draw_pathfinding(u, GRID_SIZE, window_surface)
                    try:
                        alt = dist[v] + GRID_SIZE
                        if alt < dist[u]:
                            dist[u] = alt
                    except:
                        continue

    except:
        return path
