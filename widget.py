from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QCheckBox, QSlider, QComboBox, QListWidget, QLabel


class CustomButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)

class CustomCheckBox(QCheckBox):
    def __init__(self, text):
        super().__init__(text)

class CustomSlider(QSlider):
    def __init__(self, orientation):
        super().__init__(orientation)

class CustomComboBox(QComboBox):
    def __init__(self, items):
        super().__init__()
        self.addItems(items)

class ThumbnailList(QListWidget):
    def __init__(self):
        super().__init__()



class ImageLabel(QLabel):
    """自定义 QLabel 类，用于显示图像，并实现图像的缩放和自适应窗口功能"""

    def __init__(self, parent=None):
        super().__init__(parent)    # 初始化父类
        self.scale_factor = 1.0  # 缩放比例因子
        self.setAlignment(Qt.AlignCenter)  # 设置图像居中显示
        self.contours = None    # 用于保存轮廓
        self.contourImage = None    # 用于保存轮廓图像

    def setPixmap(self, pixmap):
        """设置并保存原始图像"""
        self.pixmap_original = pixmap
        super().setPixmap(pixmap)

    def wheelEvent(self, event):
        """实现鼠标滚轮缩放功能"""
        angle = event.angleDelta().y()
        factor = 1.1 if angle > 0 else 0.9
        self.scaleImage(factor)

    def scaleImage(self, factor):
        """按比例缩放图像"""
        self.scale_factor *= factor # 更新缩放比例因子
        size = self.pixmap_original.size()  # 获取原始图像大小
        new_size = size * self.scale_factor # 计算缩放后的图像大小
        scaled_pixmap = self.pixmap_original.scaled(new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 缩放图像
        super().setPixmap(scaled_pixmap)    # 设置缩放后的图像

    def resizeEvent(self, event):
        """调整图像以适应窗口大小"""
        if hasattr(self, 'pixmap_original'):    # 如果有原始图像
            self.fitToWindow()  # 缩放图像以适应窗口大小
        super().resizeEvent(event)    # 调用父类的 resizeEvent 方法

    def fitToWindow(self):
        """将图像缩放以适应窗口大小"""
        self.setFixedSize(self.size())
        self.scale_factor = 1.0
        if not self.pixmap_original:    # 如果没有原始图像
            return
        size = self.size()  # 获取窗口大小
        if self.pixmap_original.width() > size.width():
            self.scale_factor = size.width() / self.pixmap_original.width() # 计算缩放比例
        if self.pixmap_original.height() > size.height():    # 如果图像高度大于窗口高度
            self.scale_factor = size.height() / self.pixmap_original.height()   # 计算缩放比例
        scaled_pixmap = self.pixmap_original.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 缩放图像
        super().setPixmap(scaled_pixmap)    # 设置缩放后的图像


