import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPolygon, QPainter, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt


class NodeMakerGUI(QWidget):
    def __init__(self):
        super(NodeMakerGUI, self).__init__()
        self.show()
        self.setFixedSize(1400, 900)
        self.points = QPolygon()

    def mousePressEvent(self, e):
        self.points << e.pos()
        self.update()

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        pixmap = QPixmap(r"..\images\Raw_Zones\Dun_Morogh_Raw.png")
        qp.drawPixmap(self.rect(), pixmap)
        # pen = QPen(Qt.red, 5)
        brush = QBrush(Qt.red)
        # qp.setPen(pen)
        qp.setBrush(brush)
        for i in range(self.points.count()):
            qp.drawEllipse(self.points.point(i), 2, 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NodeMakerGUI()
    sys.exit(app.exec_())
