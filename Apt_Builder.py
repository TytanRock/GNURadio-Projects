import sys, time, socket, threading
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

keepRunning = True
lock = threading.Lock()
toAdd = []
def loop():
    global w
    global keepRunning
    global lock
    global toAdd

    UDP_IP = "127.0.0.1"
    UDP_PORT = 7762
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while keepRunning:
        try:
            sock.settimeout(1)
            data, addr = sock.recvfrom(2080)
            lock.acquire()
            toAdd.extend(data)
            lock.release()
        except socket.timeout:
            pass


x = 0
y = 0
def update_gui():
    global toAdd
    global x
    global y
    lock.acquire()
    for i in range(len(toAdd)):
        w.updateImage(2079-x, y, toAdd[i])
        x += 1
        if x > 2079:
            x = 0
            y += 1
    toAdd = []
    lock.release()
    w.refreshImage()


loop_thread = threading.Thread(target=loop)
loop_thread.start()

timer = QTimer()
timer.timeout.connect(update_gui)
timer.start(1)

# Run the app until we close
app_ret = app.exec()
# Tell thread to finish
keepRunning = False
# Wait for thread to finish
loop_thread.join()
# Exit
sys.exit(app_ret)
