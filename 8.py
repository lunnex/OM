import copy
import random
import sys
import numpy as np


class Graph:
    def __init__(self, edges, n):
        self.graph = [[] for _ in range(n)]
        self.n = n
        for (src, dest) in edges:
            self.graph[src].append(dest)
            self.graph[dest].append(src)  # Make the graph undirected

    def isCyclicUtil(self, v, visited, parent):
        visited[v] = True

        for neighbor in self.graph[v]:
            if not visited[neighbor]:
                if self.isCyclicUtil(neighbor, visited, v):
                    return True
            elif neighbor != parent:
                return True

        return False

    def isCyclic(self):
        visited = [False] * self.n
        for node in range(self.n):
            if not visited[node]:
                if self.isCyclicUtil(node, visited, -1):
                    return True
        return False

    def isConnectedUtil(self, v, visited):
        visited[v] = True
        for neighbor in self.graph[v]:
            if not visited[neighbor]:
                self.isConnectedUtil(neighbor, visited)

    def isConnected(self):
        visited = [False] * self.n
        self.isConnectedUtil(0, visited)  # Start from any vertex, here we choose 0

        if any(not v for v in visited):
            return False
        return True

    def hasLessThanTwoEdges(self):
        for node in range(self.n):
            if len(self.graph[node]) > 2:
                return False
        return True


class Inhabitant:
    def __init__(self, x):
        self.edges = x
        self.weight = 0


def is_circle(matrix, tree):
    graph = Graph(tree, len(matrix))

    if graph.isCyclic():
        return True
    else:
        return False


def is_make_circle(matrix, tree, edge):
    deep_copy_tree = copy.deepcopy(tree)
    deep_copy_tree.append(edge)
    return is_circle(matrix, deep_copy_tree)


def is_already_contains_edge(tree, edge):
    if (edge[1], edge[0]) in tree or (edge[0], edge[1]) in tree:
        return True
    return False


def is_full_tree(tree, matrix):
    all_nodes = range(0, len(matrix) - 1)
    nodes_in_tree = []

    for edge in tree:
        for node in edge:
            nodes_in_tree.append(node)

    for edge in all_nodes:
        if edge not in nodes_in_tree:
            return False

    return True


def is_the_same_node(edge):
    return edge[0] == edge[1]


def is_connected(matrix, tree):
    graph = Graph(tree, len(matrix))

    return graph.isConnected()


def is_adjust_constraint(matrix, tree, constraint):
    graph = Graph(tree, len(matrix))

    return graph.hasLessThanTwoEdges()


def is_correct_tree_with_new_edge(matrix, tree, new_edge):
    if is_already_contains_edge(tree, new_edge):
        return False

    if is_make_circle(matrix, tree, new_edge):
        return False

    if is_the_same_node(new_edge):
        return False

    if not is_adjust_constraint(matrix, tree, 2):
        return False

    return True


def is_correct_tree(matrix, tree):
    for edge in tree:
        if is_the_same_node(edge):
            return False

    if is_circle(matrix, tree):
        return False

    if not is_connected(matrix, tree):
        return False

    if not is_adjust_constraint(matrix, tree, 2):
        return False

    #is_not_contains_reverse_edges = False

    #for edge in tree:
    #    is_not_contains_reverse_edges |= is_already_contains_edge(tree, edge)

    return True


def create_first_population(matrix, size_of_generation, max_attempts):
    generation = []

    for i in range(0, size_of_generation):
        tree = []
        attempts = 0

        while len(tree) < len(matrix) - 1:
            new_edge = (random.randrange(0, len(matrix)), random.randrange(0, len(matrix)))
            if is_correct_tree_with_new_edge(matrix, tree, new_edge):
                tree.append(new_edge)
                attempts = 0
            else:
                attempts += 1
                if attempts > max_attempts:
                    tree.clear()
                    attempts = 0
                    continue
        generation.insert(i, Inhabitant(tree))

    return generation


def get_weight(matrix, tree):
    weight = 0
    for edge in tree.edges:
        weight += matrix[int(edge[0])][int(edge[1])]
    return weight


def selection(new_population, size_of_generation):
    result = []

    while len(result) < size_of_generation:
        first_index = random.randrange(0, len(new_population))
        second_index = random.randrange(0, len(new_population))

        if new_population[first_index].weight > new_population[second_index].weight:
            result.append(new_population[second_index])
        else:
            result.append(new_population[first_index])

    return result


def crossover(matrix, pair, mutation_threshold, max_attempts):
    is_correct = False
    ind1 = pair[0]
    ind2 = pair[1]

    attempts = 0
    while not is_correct:

        if attempts > max_attempts:
            return None

        cut_point = random.randrange(0, len(matrix))

        b1cut1 = pair[0].edges[0:cut_point]
        b1cut2 = pair[0].edges[cut_point:len(matrix) - 1]
        b2cut1 = pair[1].edges[0:cut_point]
        b2cut2 = pair[1].edges[cut_point:len(matrix) - 1]

        ind1 = b1cut1 + b2cut2
        ind2 = b2cut1 + b1cut2

        ind1 = Inhabitant(mutation(matrix, ind1, mutation_threshold))
        ind2 = Inhabitant(mutation(matrix, ind2, mutation_threshold))

        is_correct = is_correct_tree(matrix, ind1.edges) and is_correct_tree(matrix, ind2.edges)

        attempts += 1

    return ind1, ind2


def mutation(matrix, child, mutation_threshold):
    if random.randrange(0, 1000) > mutation_threshold:
        point_for_mutation = random.randrange(0, len(matrix) - 1)

        node1 = random.randrange(0, len(matrix) - 1)
        node2 = random.randrange(0, len(matrix) - 1)

        resulted_edge = (node1, node2)
        child[point_for_mutation] = resulted_edge
    return child


def get_pair(population):
    pair = []
    while len(pair) < 2:
        random_number = random.randrange(0, len(population))
        pair.append(population[random_number])
    return pair


def print_info(population):
    trees = []
    weights = []
    max_weight = sys.maxsize
    number_of_the_best_tree = 0
    for i in range(0, len(population)):
        trees.append(population[i])
        weights.append(population[i].weight)
        if max_weight > population[i].weight:
            max_weight = population[i].weight
            number_of_the_best_tree = i

    #for i in population:
    #    print(i.edges)

    print("Средние значения в поколении")
    print(np.average(weights))
    print("Особь с наибольшим значением функциии полезности")
    print(population[number_of_the_best_tree].edges, population[number_of_the_best_tree].weight)
    print("________________________________________________________________")


def process(count_of_iterations, size_of_generation, matrix, mutation_threshold, max_attempts):
    population = create_first_population(matrix, size_of_generation, max_attempts)
    next_population = []

    for i in range(0, count_of_iterations):
        new_trees = []

        while len(next_population) < len(population) * 2:
            pair = get_pair(population)

            new_trees = crossover(matrix, pair, mutation_threshold, max_attempts)
            if new_trees is not None:
                next_population.append(new_trees[0])
                next_population.append(new_trees[1])

        for tree in next_population:
            tree.weight = get_weight(matrix, tree)

        next_population = selection(new_trees, size_of_generation)

        population = copy.deepcopy(next_population)
        next_population.clear()

        print_info(population)


q = [[0, 5, 6, 7, 8, 9],
     [5, 0, 1, 2, 3, 4],
     [6, 1, 0, 9, 8, 7],
     [7, 2, 9, 0, 6, 5],
     [8, 3, 8, 6, 0, 4],
     [9, 4, 7, 5, 4, 0]]


process(500, 1000, q, 900, 100)

