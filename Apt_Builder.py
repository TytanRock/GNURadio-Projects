import sys, time, socket
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
        self.resize (2080, 500)
    
    def updateImage(self, x, y, c):
        if not self.lastY == y:
            self.image = self.image.copy(0, 0, 2080, y+1)
            self.lastY = y
        self.image.setPixelColor(x,y,QColor(c,c,c))
    
    def refreshImage(self):
        pixmap = QPixmap.fromImage(self.image)
        self.label.setPixmap(pixmap)
        self.setCentralWidget(self.label)


app = QApplication(sys.argv)
w = MainWindow()
w.show()

UDP_IP = "127.0.0.1"
UDP_PORT = 7762
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
x = 0
y = 0
def run():
    global x
    global y
    global sock
    global w
    data, addr = sock.recvfrom(2080)
    for i in range(len(data)):
        w.updateImage(x, y, data[i])
        x += 1
        if x >= 2080:
            x = 0
            y += 1
    
    w.refreshImage()

timer = QTimer()
timer.timeout.connect(run)
timer.start(1)

sys.exit(app.exec())
