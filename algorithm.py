import networkx as nx
import numpy as np
from scipy.spatial import Delaunay
import math

from Point import Point
from Edge import Edge



def delaunay_triangulation(points):
    points_list = []
    for point in points:
        points_list.append([point.x, point.y])
    points_np = np.array(points_list)
    tri = Delaunay(points_np)
    edges_np = tri.simplices[:, [[0, 1], [1, 2], [2, 0]]].reshape(-1, 2)
    edges_np.sort(axis=1)
    edges_np = np.unique(edges_np, axis=0)
    edges = []
    for i in range(edges_np.shape[0]):
        edge = Edge(edges_np[i, 0], edges_np[i, 1], points_np)
        edges.append(edge)

    return edges


def aggregate_points_by_grids(points, size):

    points_np = class_to_np_Points(points)

    grid_coords = (points_np // size).astype(int)

    _, group_labels = np.unique(grid_coords, axis=0, return_inverse=True)

    rand_values = np.random.rand(points_np.shape[0])

    sort_order = np.lexsort((-rand_values, group_labels))

    sorted_labels = group_labels[sort_order]
    _, first_indices = np.unique(sorted_labels, return_index=True)

    selected_indices = sort_order[first_indices]

    new_points = []
    for i in selected_indices:
        point = Point(points_np[i, 0], points_np[i, 1])
        new_points.append(point)

    return new_points


def find_shortest_path(points_np, edges_np, start_point, end_point):

    graph = nx.Graph()

    for u, v in edges_np:
        length = np.linalg.norm(points_np[u] - points_np[v])
        graph.add_edge(u, v, weight=length)

    path = nx.shortest_path(graph, source=start_point, target=end_point, weight='weight')

    return path

def find_time_shortest_path(edges, start_point, end_point):

    graph = nx.Graph()

    for edge in edges:
        u, v = edge.start_point_num, edge.end_point_num
        time = None
        if edge.n <= edge.v:
             time = edge.length * edge.c
        elif edge.n > edge.v:
            time = edge.length * edge.c * (1 + math.e * edge.n / edge.v)

        graph.add_edge(u, v, weight=time)

    path = nx.shortest_path(graph, source=start_point, target=end_point, weight='weight')

    return path


def class_to_np_Points(points):

    points_list = []
    for point in points:
        points_list.append([point.x, point.y])
    points_np = np.array(points_list)

    return points_np


def class_to_np_Edges(edges):
    edges_list = []

    for edge in edges:
        edges_list.append([edge.start_point_num, edge.end_point_num])
    edges_np = np.array(edges_list)

    return edges_np
