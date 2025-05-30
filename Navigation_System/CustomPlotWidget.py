import pyqtgraph as pg
from PyQt5.QtCore import *

# 重写pg.PlotWidget,实现在滚动滚轮地图缩放和鼠标点击选取点
class CustomPlotWidget(pg.PlotWidget):

    def __init__(self):
        super().__init__()

        self.scatter = pg.ScatterPlotItem()

    wheel_scrolled = pyqtSignal(int, object)
    clicked = pyqtSignal(float, float)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        mouse_pos = event.pos()

        super().wheelEvent(event)

        self.wheel_scrolled.emit(delta, mouse_pos)

    def mousePressEvent(self, event):
        mouse_point = self.plotItem.vb.mapSceneToView(event.pos())
        x = mouse_point.x()
        y = mouse_point.y()

        self.clicked.emit(x, y)

        scatter = pg.ScatterPlotItem(
            pos=[(x, y)],
            symbol='o',
            size=10,
            pen=pg.mkPen('r'),
            brush=pg.mkBrush('r')
        )
        self.addItem(scatter)

        super().mousePressEvent(event)
