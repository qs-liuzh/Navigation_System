import sys
import copy
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet

from CustomPlotWidget import CustomPlotWidget
from ToggleButton import ToggleButton
from algorithm import (aggregate_points_by_grids, delaunay_triangulation, find_shortest_path, class_to_np_Points,
                       class_to_np_Edges, find_time_shortest_path)
from Point import Point
from Car import Car


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('icon.png'))
        self.resize(1600, 900)
        self.center()

        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.update_map)

        self.car_timer = QTimer()
        self.car_timer.timeout.connect(self.update_flow)

        self.initial_points = self.initialize_points()
        self.initial_edges = delaunay_triangulation(self.initial_points)
        self.points = copy.deepcopy(self.initial_points)
        self.edges = copy.deepcopy(self.initial_edges)
        self.cars = []

        self.main_widget = QWidget()
        self.plot_graph = CustomPlotWidget()
        self.vbox = QVBoxLayout()
        self.hbox_1 = QHBoxLayout()
        self.hbox_2 = QHBoxLayout()
        self.hbox_3 = QHBoxLayout()
        self.hbox_4 = QHBoxLayout()
        self.line_1 = QLineEdit()
        self.line_2 = QLineEdit()
        self.button_1 = QPushButton("查找")
        self.line_3 = QLineEdit()
        self.line_4 = QLineEdit()
        self.button_2 = QPushButton("选择点 1")
        self.line_5 = QLineEdit()
        self.line_6 = QLineEdit()
        self.button_3 = QPushButton("选择点 2")
        self.button_4 = QPushButton("查找")
        self.button_5 = ToggleButton("显示车流")
        self.line_7 = QLineEdit()
        self.line_8 = QLineEdit()
        self.button_6 = QPushButton("选择点 1")
        self.line_9 = QLineEdit()
        self.line_10 = QLineEdit()
        self.button_7 = QPushButton("选择点 2")
        self.button_8 = QPushButton("查找")

        self.setCentralWidget(self.main_widget)
        self.main_widget.setLayout(self.vbox)
        self.vbox.addWidget(self.plot_graph)
        self.vbox.addLayout(self.hbox_1)
        self.vbox.addLayout(self.hbox_2)
        self.vbox.addLayout(self.hbox_3)
        self.vbox.addLayout(self.hbox_4)
        self.hbox_1.addWidget(self.line_1)
        self.hbox_1.addWidget(self.line_2)
        self.hbox_1.addWidget(self.button_1)
        self.hbox_2.addWidget(self.line_3)
        self.hbox_2.addWidget(self.line_4)
        self.hbox_2.addWidget(self.button_2)
        self.hbox_2.addWidget(self.line_5)
        self.hbox_2.addWidget(self.line_6)
        self.hbox_2.addWidget(self.button_3)
        self.hbox_2.addWidget(self.button_4)
        self.hbox_3.addWidget(self.button_5)
        self.hbox_4.addWidget(self.line_7)
        self.hbox_4.addWidget(self.line_8)
        self.hbox_4.addWidget(self.button_6)
        self.hbox_4.addWidget(self.line_9)
        self.hbox_4.addWidget(self.line_10)
        self.hbox_4.addWidget(self.button_7)
        self.hbox_4.addWidget(self.button_8)

        self.plot_graph.setBackground((242, 242, 242))
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.clicked.connect(self.plot_map)
        self.plot_graph.wheel_scrolled.connect(self.update_map)
        self.plot_graph.clicked.connect(self.show_coordinate)
        self.line_1.setPlaceholderText("x坐标")
        self.line_1.setClearButtonEnabled(True)
        self.line_2.setPlaceholderText("y坐标")
        self.line_2.setClearButtonEnabled(True)
        self.button_1.clicked.connect(self.find_points_and_edges_nearby)
        self.line_3.setPlaceholderText("点1 x坐标")
        self.line_4.setPlaceholderText("点1 y坐标")
        self.button_2.clicked.connect(self.set_point_1)
        self.line_5.setPlaceholderText("点2 x坐标")
        self.line_6.setPlaceholderText("点2 y坐标")
        self.button_3.clicked.connect(self.set_point_2)
        self.button_4.clicked.connect(self.generate_path)
        self.button_5.change_to_on.connect(self.start_traffic_flow)
        self.button_5.change_to_off.connect(self.stop_traffic_flow)
        self.line_7.setPlaceholderText("点1 x坐标")
        self.line_8.setPlaceholderText("点1 y坐标")
        self.button_6.clicked.connect(self.set_point_3)
        self.line_9.setPlaceholderText("点2 x坐标")
        self.line_10.setPlaceholderText("点2 y坐标")
        self.button_7.clicked.connect(self.set_point_4)
        self.button_8.clicked.connect(self.generate_path_2)

        self.update_map()

    def initialize_points(self):

        points = []
        a = np.random.randn(10000, 2)
        for i in range(a.shape[0]):
            point = Point(a[i, 0], a[i, 1])
            points.append(point)

        return points

    def start_traffic_flow(self):

        self.car_timer.start(1000)

        return

    def stop_traffic_flow(self):

        self.car_timer.stop()
        self.cars.clear()
        self.car_scatter.clear()

        return

    def update_flow(self):
        print(1)
        """生成10辆车"""
        for _ in range(50):
            start_point_num = np.random.randint(0, len(self.points))
            end_point_num = np.random.randint(0, len(self.points))
            while start_point_num == end_point_num:
                start_point_num = np.random.randint(0, len(self.points))
                end_point_num = np.random.randint(0, len(self.points))
            car = Car(self.points, self.edges, start_point_num, end_point_num)
            self.cars.append(car)

        """"更新每条edge的n"""
        for edge in self.edges:
            edge.n = 0
        for car in self.cars:
            current_edge = car.edges_in_path_np[car.current_edge_num]
            start_point_num = current_edge[0]
            end_point_num = current_edge[1]
            for edge in self.edges:
                if ((start_point_num == edge.start_point_num and end_point_num == edge.end_point_num)
                        or (start_point_num == edge.end_point_num and end_point_num == start_point_num)):
                    edge.n += 1
                    break

        """更新车的属性，并将到达终点的车删除"""
        for i in range(len(self.cars) - 1, -1, -1):
            car = self.cars[i]
            finished = car.update(self.edges)
            if finished:
                del self.cars[i]

        self.draw_flow()

        return

    def draw_flow(self):
        self.plot_graph.clear()
        for edge in self.edges:
            start = np.array([self.points[edge.start_point_num].x, self.points[edge.start_point_num].y])
            end = np.array([self.points[edge.end_point_num].x, self.points[edge.end_point_num].y])
            x_coords = [start[0], end[0]]
            y_coords = [start[1], end[1]]
            self.plot_graph.plot(x_coords, y_coords, pen=pg.mkPen(color=(min(200, 50 + 30 * edge.n), 0, 0), width=1 + 0.05 * edge.n))

        return

    def generate_path(self):

        points_np = class_to_np_Points(self.points)
        edges_np = class_to_np_Edges(self.edges)

        start_point = None
        goal_point = None
        for i in range(points_np.shape[0]):
            point = points_np[i]
            if point[0] == float(self.line_3.text()) and point[1] == float(self.line_4.text()):
                start_point = i
            if point[0] == float(self.line_5.text()) and point[1] == float(self.line_6.text()):
                goal_point = i

        path = find_shortest_path(points_np, edges_np, start_point, goal_point)

        self.plot_graph.plot(points_np[path, 0], points_np[path, 1], pen='yellow')

        return

    def generate_path_2(self):

        points_np = class_to_np_Points(self.points)

        start_point = None
        goal_point = None
        for i in range(points_np.shape[0]):
            point = points_np[i]
            if point[0] == float(self.line_7.text()) and point[1] == float(self.line_8.text()):
                start_point = i
            if point[0] == float(self.line_9.text()) and point[1] == float(self.line_10.text()):
                goal_point = i

        path = find_time_shortest_path(self.edges, start_point, goal_point)

        self.plot_graph.plot(points_np[path, 0], points_np[path, 1], pen='green')


        return

    # 将选定位置的最近点作为点1
    def set_point_1(self):
        points_np = class_to_np_Points(self.points)

        x = float(self.line_1.text())
        y = float(self.line_2.text())
        pos = np.array([x, y])
        distances = np.linalg.norm(points_np - pos, axis=1)
        nearest_points = points_np[np.argmin(distances)]
        self.line_3.setText(str(nearest_points[0]))
        self.line_4.setText(str(nearest_points[1]))

        self.plot_graph.addItem(
            pg.ScatterPlotItem(
            [nearest_points[0]], [nearest_points[1]], color=(0, 255, 0), symbol='t', size=20
            )
        )

        return

    # 将选定位置的最近点作为点2
    def set_point_2(self):
        points_np = class_to_np_Points(self.points)

        x = float(self.line_1.text())
        y = float(self.line_2.text())
        pos = np.array([x, y])
        distances = np.linalg.norm(points_np - pos, axis=1)
        nearest_points = points_np[np.argmin(distances)]
        self.line_5.setText(str(nearest_points[0]))
        self.line_6.setText(str(nearest_points[1]))

        self.plot_graph.addItem(
            pg.ScatterPlotItem(
                [nearest_points[0]], [nearest_points[1]], color=(0, 255, 0), symbol='t1', size=20
            )
        )

        return

    def set_point_3(self):
        points_np = class_to_np_Points(self.points)

        x = float(self.line_1.text())
        y = float(self.line_2.text())
        pos = np.array([x, y])
        distances = np.linalg.norm(points_np - pos, axis=1)
        nearest_points = points_np[np.argmin(distances)]
        self.line_7.setText(str(nearest_points[0]))
        self.line_8.setText(str(nearest_points[1]))

        self.plot_graph.addItem(
            pg.ScatterPlotItem(
            [nearest_points[0]], [nearest_points[1]], color=(0, 255, 0), symbol='t', size=20
            )
        )

        return

    def set_point_4(self):
        points_np = class_to_np_Points(self.points)

        x = float(self.line_1.text())
        y = float(self.line_2.text())
        pos = np.array([x, y])
        distances = np.linalg.norm(points_np - pos, axis=1)
        nearest_points = points_np[np.argmin(distances)]
        self.line_9.setText(str(nearest_points[0]))
        self.line_10.setText(str(nearest_points[1]))

        self.plot_graph.addItem(
            pg.ScatterPlotItem(
            [nearest_points[0]], [nearest_points[1]], color=(0, 255, 0), symbol='t', size=20
            )
        )

        return

    def show_coordinate(self, x, y):

        self.line_1.setText(str(x))
        self.line_2.setText(str(y))

    def update_map(self):

        visible_range = self.plot_graph.viewRect()
        y_min = visible_range.top()
        y_max = visible_range.bottom()
        height = y_max - y_min

        self.points = aggregate_points_by_grids(self.initial_points, height / 18)
        self.edges = delaunay_triangulation(self.points)
        self.plot_graph.scatter.clear()

        points_list = []
        for point in self.points:
            points_list.append([point.x, point.y])
        points_np = np.array(points_list)

        self.plot_graph.scatter.addPoints(points_np[:, 0], points_np[:, 1])

        self.plot_map()

        return

    def plot_map(self):

        points_np = class_to_np_Points(self.points)
        edges_np = class_to_np_Edges(self.edges)

        self.plot_graph.clear()

        self.plot_graph.scatter.addPoints(points_np[:, 0], points_np[:, 1])
        self.plot_graph.addItem(self.plot_graph.scatter)

        if not edges_np.shape[0]:
            return

        starts = points_np[edges_np[:, 0]]
        ends = points_np[edges_np[:, 1]]

        x = np.empty(3 * len(edges_np))
        y = np.empty(3 * len(edges_np))
        x[0::3] = starts[:, 0]
        y[0::3] = starts[:, 1]
        x[1::3] = ends[:, 0]
        y[1::3] = ends[:, 1]
        x[2::3] = np.nan
        y[2::3] = np.nan

        self.plot_graph.plot(x, y, pen='b')

    def plot_edges(self, points, edges, _type='class', color='b'):

        points_np = points
        edges_np = edges

        if not edges_np.shape[0]:
            return

        starts = points_np[edges_np[:, 0]]
        ends = points_np[edges_np[:, 1]]

        x = np.empty(3 * len(edges_np))
        y = np.empty(3 * len(edges_np))
        x[0::3] = starts[:, 0]
        y[0::3] = starts[:, 1]
        x[1::3] = ends[:, 0]
        y[1::3] = ends[:, 1]
        x[2::3] = np.nan
        y[2::3] = np.nan

        self.plot_graph.plot(x, y, pen=color)

    def center(self):

        screen = QDesktopWidget().screenGeometry()
        size = QDesktopWidget().geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

        return

    def find_points_and_edges_nearby(self):

        initial_points_np = class_to_np_Points(self.initial_points)
        points_np = class_to_np_Points(self.points)
        edges_np = class_to_np_Edges(self.edges)

        x = float(self.line_1.text())
        y = float(self.line_2.text())

        selected_point = np.array([x, y])
        distances = np.linalg.norm(initial_points_np - selected_point, axis=1)

        points_nearby = np.argsort(distances)[:100].tolist()

        index_map = {original_idx: new_idx for new_idx, original_idx in enumerate(points_nearby)}

        edges_nearby = []
        for edge in self.initial_edges:
            u = edge.start_point_num
            v = edge.end_point_num
            if u in index_map and v in index_map:
                edges_nearby.append([index_map[u], index_map[v]])

        points_nearby_coordinates = initial_points_np[points_nearby]

        self.plot_graph.clear()
        self.plot_graph.addItem(pg.ScatterPlotItem(points_np[:, 0], points_np[:, 1]))
        self.plot_edges(points_np, np.array(edges_np), color='b')
        new_scatter = pg.ScatterPlotItem(points_nearby_coordinates[:, 0], points_nearby_coordinates[:, 1])
        self.plot_graph.addItem(new_scatter)

        self.plot_edges(points_nearby_coordinates, np.array(edges_nearby), color='r')
        self.plot_graph.addItem(pg.ScatterPlotItem([selected_point[0]], [selected_point[1]]))

        self.plot_graph.autoRange(items=[new_scatter])

        return


if __name__ == '__main__':

    np.random.seed(42)

    app = QApplication(sys.argv)

    apply_stylesheet(app, theme='light_blue.xml')

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())