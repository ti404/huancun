import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer

class FullScreenImage(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle('Full Screen Image')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        
        # 创建标签来显示图片
        self.image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        
        # 设置定时器，10秒后关闭程序
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close)
        self.timer.start(10000)  # 10秒

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = 'tea.jpg'  # 默认图片路径
    ex = FullScreenImage(image_path)
    ex.showFullScreen()
    sys.exit(app.exec_())