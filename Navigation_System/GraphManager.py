import numpy as np
import pyqtgraph as pg


class GraphManager:
    def __init__(self, plot_widget):
        self.plot_widget = plot_widget
        self.points = {}  
        self.lines = {}
        self.current_id = 0

    def add_point(self, pos, color='r', size=10):
        scatter = pg.ScatterPlotItem(pos=[pos], size=size, pen=pg.mkPen(color), brush=pg.mkBrush(color))
        self.plot_widget.addItem(scatter)
        self.current_id += 1
        self.points[self.current_id] = {
            'item': scatter,
            'data': np.array(pos)
        }
        return self.current_id

    def add_line(self, start_id, end_id, color='w', width=2):
        if start_id not in self.points or end_id not in self.points:
            raise ValueError("Invalid point IDs")

        line = pg.PlotDataItem(pen=pg.mkPen(color, width=width))
        self._update_line_position(line, start_id, end_id)
        self.plot_widget.addItem(line)
        self.current_id += 1
        self.lines[self.current_id] = {
            'item': line,
            'start': start_id,
            'end': end_id
        }
        return self.current_id

    def _update_line_position(self, line_item, start_id, end_id):
        start_pos = self.points[start_id]['data']
        end_pos = self.points[end_id]['data']
        line_item.setData([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]])

    def update_point_position(self, point_id, new_pos):
        if point_id not in self.points:
            return
        self.points[point_id]['data'] = np.array(new_pos)
        self.points[point_id]['item'].setData(pos=[new_pos])

        for line_id in self.lines:
            line_info = self.lines[line_id]
            if line_info['start'] == point_id or line_info['end'] == point_id:
                self._update_line_position(line_info['item'], line_info['start'], line_info['end'])

    def remove_element(self, element_id):
         if element_id in self.points:
            self.plot_widget.removeItem(self.points[element_id]['item'])
            del self.points[element_id]
            for line_id in list(self.lines.keys()):
                if self.lines[line_id]['start'] == element_id or self.lines[line_id]['end'] == element_id:
                    self.remove_element(line_id)
        elif element_id in self.lines:
            self.plot_widget.removeItem(self.lines[element_id]['item'])
            del self.lines[element_id]
