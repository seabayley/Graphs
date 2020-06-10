def earliest_ancestor(ancestors, starting_node):
    al = {}
    paths = []
    path_stack = [[starting_node]]

    for edge in ancestors:
        al.setdefault(edge[1], []).append(edge[0])
    vertices = al.keys()

    if starting_node not in vertices:
        return -1

    vertice = starting_node

    while len(path_stack) > 0:
        current_path = path_stack.pop()
        vertice = current_path[-1]
        neighbors = al[vertice]
        for neighbor in neighbors:
            if neighbor in vertices:
                new_path = current_path[:]
                new_path.append(neighbor)
                path_stack.append(new_path)
            else:
                new_path = current_path[:]
                new_path.append(neighbor)
                paths.append(new_path)

    earliest_ancestor = None

    paths.sort(key=len)
    if len(paths) > 1:
        path1 = paths[-1]
        path2 = paths[-2]
        if len(path1) == len(path2):
            earliest_ancestor = min(path1[-1], path2[-1])

    if earliest_ancestor is None:
        earliest_ancestor = paths[-1][-1]

    return earliest_ancestor
