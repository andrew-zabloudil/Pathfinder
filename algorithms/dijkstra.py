"""
Bugs: 
3.  It will loop infinitely and stop responding if there is no possible path
    due to wall placement.
3a. It no longer loops infinitely, but it doesn't notify the user when it breaks
"""


def Dijkstra(nodes, walls, WIDTH, HEIGHT, GRID_SIZE):
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
                    return path

            for offset in neighbor_offsets:
                u = (v[0] + offset[0], v[1] + offset[1])
                if u in Q and u not in walls:
                    try:
                        alt = dist[v] + GRID_SIZE
                        if alt < dist[u]:
                            dist[u] = alt
                    except:
                        continue

    except:
        return path
