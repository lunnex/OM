import sys


def prim(matrix):
    tree = []
    visited = [0]
    main_iterator = 0
    while main_iterator < len(matrix[0]):
        min_value = sys.maxsize
        min_index = -1
        min_i = -1
        for i in visited:
            j = 0
            while j < len(matrix[i]):
                if j not in visited:
                    if min_value > matrix[i][j] != 0:
                        min_value = matrix[i][j]
                        min_index = j
                        min_i = i
                j = j + 1
        if min_index != -1:
            visited.append(min_index)
            tree.append([min_i, min_index])
        main_iterator = main_iterator + 1
    return tree


def kruskal(matrix):
    edges = get_sorted_edges(matrix)
    tree = []

    for edge in edges:
        if is_full_tree(tree, len(matrix)):
            break
        if is_circle(edge):
            continue
        else:
            tree.append(edge)

    return tree


def get_sorted_edges(matrix):
    result = dict()
    for i, row in enumerate(matrix):
        for j, column in enumerate(row):
            if i == j or (j, i) in result:
                continue
            result[(i, j)] = matrix[i][j]
    return dict(sorted(result.items(), key=lambda item: item[1]))


left_nodes = []
right_nodes = []


def is_circle(branch):
    if branch[0] in right_nodes or branch[1] in left_nodes:
        return True

    if branch[0] not in left_nodes:
        left_nodes.append(branch[0])
    if branch[1] not in right_nodes:
        right_nodes.append(branch[1])

    return False


def is_full_tree(tree, matrix_size):
    visited_nodes = []

    for branch in tree:
        for node in branch:
            if node not in visited_nodes:
                visited_nodes.append(node)

    if len(visited_nodes) < matrix_size:
        return False
    else:
        return True


g = [[0, 5, 6, 7, 8, 9],
     [5, 0, 1, 2, 3, 4],
     [6, 1, 0, 9, 8, 7],
     [7, 2, 9, 0, 6, 5],
     [8, 3, 8, 6, 0, 4],
     [9, 4, 7, 5, 4, 0]]

print(prim(g))
