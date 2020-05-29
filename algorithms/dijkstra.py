def Dijkstra(nodes, walls, width, height):
    start = nodes[0]
    end = nodes[1]

    dist = {}
    graph = []
    Q = []
    path = []

    for x in range(0, width, 20):
        for y in range(0, height, 20):
            graph.append((x, y))

    for vertex in graph:
        if vertex != start:
            dist[vertex] = 1000000
        else:
            dist[vertex] = 0
        Q.append(vertex)

    while len(Q) != 0:
        if start in Q:
            v = start
        else:
            min_dist = 1000000
            for vertex in Q:
                if dist[vertex] < min_dist:
                    min_dist = dist[vertex]
                    v = vertex
        if v in Q:
            Q.remove(v)

        if v == end:
            dist[start] = 0
            while v != start:
                min_dist = 1000000
                u1 = (v[0] - 20, v[1])
                u2 = (v[0], v[1] - 20)
                u3 = (v[0] + 20, v[1])
                u4 = (v[0], v[1] + 20)
                possible_u = [u1, u2, u3, u4]
                for u in possible_u:
                    if (dist[u] < min_dist) and (u not in walls):
                        min_dist = dist[u]
                        v = u
                path.append(v)
            if v == start:
                return path

        for i in range(4):
            if i == 0 and (v[0] - 20, v[1]) in Q:
                u = (v[0] - 20, v[1])
                if u not in walls:
                    alt = dist[v] + 20
                    if alt < dist[u]:
                        dist[u] = alt
            elif i == 1 and (v[0], v[1] - 20) in Q:
                u = (v[0], v[1] - 20)
                if u not in walls:
                    alt = dist[v] + 20
                    if alt < dist[u]:
                        dist[u] = alt
            elif i == 2 and (v[0] + 20, v[1]) in Q:
                u = (v[0] + 20, v[1])
                if u not in walls:
                    alt = dist[v] + 20
                    if alt < dist[u]:
                        dist[u] = alt
            elif i == 3 and (v[0], v[1] + 20) in Q:
                u = (v[0], v[1] + 20)
                if u not in walls:
                    alt = dist[v] + 20
                    if alt < dist[u]:
                        dist[u] = alt

        if v == start:
            dist.pop(v)

    return path
