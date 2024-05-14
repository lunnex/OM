import sys


highlighted_rows = []
crossed_columns = []
crossed_rows = []
used_nodes = []
used_edges = []


def prim(matrix, max_power):
    tree = []
    second_index = 0

    while not is_full_tree(tree, len(matrix)):
        index = second_index

        highlighted_rows.append(index)
        crossed_columns.append(index)
        index, second_index, value = get_min_item(matrix, highlighted_rows)
        highlighted_rows.append(second_index)

        tree.append((index, second_index))
        used_nodes.append(index)
        used_nodes.append(second_index)

        for edge in get_max_power_node((index, second_index), max_power):
            while edge in highlighted_rows:
                highlighted_rows.remove(edge)
            crossed_rows.append(edge)

    return tree


def get_max_power_node(edge, max_power):
    for item in edge:
        if used_nodes.count(item) >= max_power:
            yield item


def get_min_item(matrix, hl_rows):
    max_value = sys.maxsize
    first_result_index = -1
    second_result_index = -1
    for row in list(filter(lambda e: e not in crossed_rows, hl_rows)):
        for index, item in enumerate(matrix[row]):
            if item > 0 and index not in crossed_columns:
                value = item

                if max_value > value:
                    max_value = value
                    first_result_index = row
                    second_result_index = index

    return first_result_index, second_result_index, max_value


def kruskal(matrix, max_power):
    edges_with_weight = get_edges_with_weight(matrix)
    edges = get_edges_without_weight(edges_with_weight)
    tree = []

    for i, edge in enumerate(edges):
        if is_full_tree(tree, len(matrix)):
            break
        if is_already_contains_edge(tree, edge):
            continue
        if is_circle(edge, max_power):
            continue
        if not is_adjacent(edge, i):
            continue
        else:
            tree.append(edge)

    return tree


def get_edges_with_weight(matrix):
    result = dict()
    for i, row in enumerate(matrix):
        for j, column in enumerate(row):
            if i == j:
                continue
            result[(i, j)] = matrix[i][j]

    return sorted(result.items(), key=lambda x: x[1])


def get_edges_without_weight(sorted_list_with_weight):
    sorted_list_without_weight = []

    for item in sorted_list_with_weight:
        sorted_list_without_weight.append(item[0])

    return sorted_list_without_weight


visited_nodes = []


def is_circle(branch, max_power):
    if visited_nodes.count(branch[0]) > max_power - 1 or visited_nodes.count(branch[1]) > max_power - 1:
        return True

    if branch[0] in visited_nodes and branch[1] in visited_nodes:
        return True

    return False


def is_adjacent(edge, num_of_iteration):
    if num_of_iteration == 0:
        fill_visited_nodes(edge)
        return True

    if edge[0] not in visited_nodes and edge[1] not in visited_nodes:
        return False

    fill_visited_nodes(edge)
    return True


def is_already_contains_edge(tree, edge):
    if (edge[1], edge[0]) in tree:
        return True
    return False


def fill_visited_nodes(edge):
    for node in edge:
        visited_nodes.append(node)


def is_full_tree(tree, matrix_size):
    if len(tree) < matrix_size - 1:
        return False
    else:
        return True


def get_route_len(tree, mat):
    length = 0
    for edge in tree:
        length += mat[edge[0]][edge[1]]
    return length


# g = [[0, 1, 3, 4, 5, 6],
#     [1, 0, 4, 3, 1, 3],
#     [3, 4, 0, 2, 2, 1],
#     [4, 3, 2, 0, 2, 4],
#     [5, 1, 2, 2, 0, 5],
#     [6, 3, 1, 4, 5, 0]]

g = [[0, 5, 6, 7, 8, 9],
     [5, 0, 1, 2, 3, 4],
     [6, 1, 0, 9, 8, 7],
     [7, 2, 9, 0, 6, 5],
     [8, 3, 8, 6, 0, 4],
     [9, 4, 7, 5, 4, 0]]

kruskal_result = kruskal(g, 2)
prim_result = prim(g, 2)

print(kruskal_result, get_route_len(kruskal_result, g))
print(prim_result, get_route_len(kruskal_result, g))
