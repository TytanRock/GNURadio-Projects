import sys, time
from PyQt6.QtGui import QPixmap, QImage, QColor
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt6.QtCore import QTimer, Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Image Viewer"
        self.setWindowTitle(self.title)

        self.lastY = 0

        self.image = QImage(2080, 1, QImage.Format.Format_Grayscale8)
        self.label = QLabel(self)
    
    def updateImage(self, x, y):
        if not self.lastY == y:
            self.image = self.image.copy(0, 0, 2080, y+1)
            self.lastY = y
        self.image.setPixelColor(x,y,QColor(128,128,128))
        pixmap = QPixmap.fromImage(self.image)
        self.label.setPixmap(pixmap)
        self.setCentralWidget(self.label)


app = QApplication(sys.argv)
w = MainWindow()
w.show()

i = 0
j = 0
def run():
    global i
    global j
    print('Updating ' + str(i) + ' ' + str(j))
    w.updateImage(i, j)
    i += 1
    if i == 2080:
        i = 0
        j += 1

timer = QTimer()
timer.timeout.connect(run)
timer.start(10)

sys.exit(app.exec())
