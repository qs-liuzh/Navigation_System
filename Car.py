import math
import numpy as np

from algorithm import find_shortest_path, class_to_np_Points, class_to_np_Edges


class Car:
    def __init__(self, points, edges, start_point_num, end_point_num):
        self.start_point_num = start_point_num
        self.end_point_num = end_point_num
        points_np = class_to_np_Points(points)
        edges_np = class_to_np_Edges(edges)
        self.path = find_shortest_path(points_np, edges_np, start_point_num, end_point_num)
        self.edges_in_path_np = self.generate_edges_in_path()
        self.current_edge_num = 0
        self.distance_on_current_edge = 0
        self.speed = None

    def generate_edges_in_path(self):
        edges_in_path_list = []
        for i in range(len(self.path) - 1):
            edges_in_path_list.append([self.path[i], self.path[i + 1]])
        edges_in_path_np = np.array(edges_in_path_list)

        return edges_in_path_np

    def update(self, edges):
        self.update_speed(edges)
        self.distance_on_current_edge += self.speed

        # 处理可能跨越多个边的情况
        while self.current_edge_num < len(self.edges_in_path_np):
            current_edge = self.edges_in_path_np[self.current_edge_num]
            edge_length = edges[current_edge[0]].length  # 通过起点索引获取实际边长

            if self.distance_on_current_edge < edge_length:
                break

            self.distance_on_current_edge -= edge_length
            self.current_edge_num += 1

        # 当处理完所有边时返回True
        return self.current_edge_num >= len(self.edges_in_path_np)

    def update_speed(self, edges):
        current_edge = edges[self.current_edge_num]
        if current_edge.n <= current_edge.v:
            self.speed = 1 / current_edge.c
        elif current_edge.n > current_edge.v:
            self.speed = max(0.05,
                             1 / (current_edge.c * (1 + math.e * current_edge.n / current_edge.v)))

        return
