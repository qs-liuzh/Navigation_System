import numpy as np

class Edge():
    def __init__(self, start_point_num, end_point_num, points_np):
        self.start_point_num = start_point_num
        self.end_point_num = end_point_num
        self.length = self.initialize_length(points_np)
        self.n = 0
        self.v = self.length * 2
        self.c = 3

    def initialize_length(self, points_np):

        start_point = points_np[self.start_point_num]
        end_point = points_np[self.end_point_num]

        length = np.linalg.norm(end_point - start_point)

        return length
