import os
import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QInputDialog
import pydicom

flag = 0


def open_image(file_name):
    """打开图像文件并返回路径"""
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getOpenFileName(None, '选择图像', '', 'Images (*.png *.jpg *.bmp *.dcm)', options=options)
    return file_name

def save_image(image, default_directory):
    """保存图像到指定文件夹"""
    new_img_dir = os.path.join(default_directory, 'newImg')
    if not os.path.exists(new_img_dir):
        os.makedirs(new_img_dir)

    save_path, _ = QFileDialog.getSaveFileName(None, '保存图像', new_img_dir, 'Images (*.png *.jpg *.bmp)') # 添加文件类型过滤
    if save_path:
        cv2.imwrite(save_path, image)      # 保存图像
        print(f'图像已保存到: {save_path}')    # 打印保存路径

def loadThumbnails(self):
    """加载所有支持的图像格式（包括DICOM）的缩略图"""
    img_dir = os.path.join(os.getcwd(), 'img')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    for img_name in os.listdir(img_dir):
        img_path = os.path.join(img_dir, img_name)
        lower_name = img_name.lower()

        # DICOM文件处理
        if lower_name.endswith('.dcm'):
            try:
                ds = pydicom.dcmread(img_path)
                img = ds.pixel_array
                img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
                if len(img.shape) == 2:  # 灰度图转RGB
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            except Exception as e:
                print(f"Error loading DICOM: {str(e)}")
                continue

        # 普通图像文件处理
        elif lower_name.endswith(('.png', '.jpg', '.bmp')):
            img = cv2.imread(img_path)
            if img is None:
                continue

        else:
            continue  # 跳过不支持的文件格式

        # 生成缩略图
        h, w = img.shape[:2]
        aspect_ratio = w / h
        thumbnail = cv2.resize(img, (int(100 * aspect_ratio), 100))
        qimg = QImage(thumbnail.data, thumbnail.shape[1], thumbnail.shape[0],
                      thumbnail.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        item = QListWidgetItem(QIcon(pixmap), img_name)
        item.setData(Qt.UserRole, img_path)
        self.thumbnailList.addItem(item)


def addImage(self):
    """添加图像到列表"""
    img_path = open_image('')    # 打开图像文件
    if img_path:
        img_name = os.path.basename(img_path)
        img_dir = os.path.join(os.getcwd(), 'img')  # 图像文件夹路径
        if not os.path.exists(img_dir):  # 如果文件夹不存在，则创建
            os.makedirs(img_dir)  # 创建文件夹
            os.makedirs(img_dir)    # 创建文件夹

        img_path = os.path.join(img_dir, img_name)
        cv2.imwrite(img_path, self.image)
        pixmap = QPixmap(img_path)
        item = QListWidgetItem(QIcon(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)),
                               img_name)
        item.setData(Qt.UserRole, img_path)
        self.thumbnailList.addItem(item)


def thumbnailClicked(self, item):
    """点击缩略图时的操作"""
    self.imagePath = item.data(Qt.UserRole)
    self.loadImage(self.imagePath)

def processImage(self):
    """处理图像，进行轮廓检测和面积、周长计算"""
    if self.image is None:
        return

    gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) # 转换为灰度图像

    if self.rangeSearchCheckBox.isChecked():    # 如果选中了灰度范围搜索
        low = self.grayRangeSlider.value() - 10
        high = self.grayRangeSlider.value() + 10
        _, thresh = cv2.threshold(gray, low, high, cv2.THRESH_BINARY)
        self.grayRangeValueLabel.setText(f"灰度范围: {low}-{high}") # 更新标签显示
    else:
        ret, thresh = cv2.threshold(gray, self.thresholdSlider.value(), 255, cv2.THRESH_BINARY)     # 二值化处理
        self.thresholdValueLabel.setText(str(self.thresholdSlider.value())) # 更新标签显示

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    self.label.contours = contours
    self.label.contourImage = self.image.copy()

    self.processedImage = self.image.copy()
    self.contourImage = self.image.copy()

    self.contourList.clear()
    for i, cnt in enumerate(contours):
        item = QListWidgetItem(f"Contour {i + 1}")
        item.setData(Qt.UserRole, cnt)
        self.contourList.addItem(item)

        M = cv2.moments(cnt)
        if M["m00"] == 0:
            continue

        x1, y1, w, h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        perimeter = round(perimeter, 4)

        if self.pixel_per_cm:
            actual_area = area / (self.pixel_per_cm ** 2)
            actual_perimeter = perimeter / self.pixel_per_cm
            actual_area = round(actual_area, 4)
            actual_perimeter = round(actual_perimeter, 4)

            if not self.showContoursCheckBox.isChecked():
                cv2.drawContours(self.processedImage, [cnt], -1, (0, 255, 255), 3)
                cv2.putText(self.processedImage, f'area: {actual_area} cm^2', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 255, 0), 2)
                cv2.putText(self.processedImage, f'perimeter: {actual_perimeter} cm', (x1, y1 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            if not self.showContoursCheckBox.isChecked():
                cv2.drawContours(self.processedImage, [cnt], -1, (0, 255, 255), 3)
                cv2.putText(self.processedImage, f'area: {area} px', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0, 255, 0), 2)
                cv2.putText(self.processedImage, f'perimeter: {perimeter} px', (x1, y1 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.drawContours(self.contourImage, [cnt], -1, (0, 255, 255), 3)

    self.updateDisplayedImage()


def thumbnailClicked(self, item):
    """点击缩略图时的操作"""
    self.imagePath = item.data(Qt.UserRole)
    self.loadImage(self.imagePath)    # 加载图像

def openImage(self):
    """打开图像文件"""
    options = QFileDialog.Options()
    fileName, _ = QFileDialog.getOpenFileName(self, '选择图像', '', 'Images (*.png *.jpg *.bmp *.dcm)', options=options)
    if fileName:
        self.imagePath = fileName
        self.loadImage(fileName)

def loadImage(self, fileName):
    """通用图像加载方法"""
    if fileName.lower().endswith('.dcm'):
        ds = pydicom.dcmread(fileName)
        self.image = ds.pixel_array
        # DICOM图像标准化
        self.image = cv2.normalize(self.image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        if len(self.image.shape) == 2:  # 转换为3通道
            self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
    else:
        self.image = cv2.imread(fileName)

    if self.image is not None:
        self.displayImage(self.image)

def promptImageSize(self):
    """根据单位类型提示用户输入图像尺寸"""
    if self.unitComboBox.currentText() == 'Centimeters':
        ok, w = QInputDialog.getDouble(self, '图像宽度', '请输入图像宽度（厘米）:', min=0.01, decimals=2)
        if ok:
            self.pixel_per_cm = self.image.shape[1] / w
    else:
        self.pixel_per_cm = None



def updateDisplayedImage(self):
    """根据勾选框状态更新显示的图像"""
    if self.showContoursCheckBox.isChecked():    # 如果选中了显示轮廓复选框
        #如果没有点击缩略图,则不进行操作
        if self.image is None:
            return
        #如果点击了缩略图但没有点击分析图像按钮,则不进行操作
        elif self.label.contours is None:
            return
        #如果点击了缩略图且点击了分析图像按钮,则进行操作
        else:
            self.displayImage(self.contourImage)    # 显示轮廓图像
    else:    # 否则显示处理后的图像
        self.displayImage(self.processedImage)    # 显示处理后的图像

def updateContours(self):
    """更新图像以仅显示选中的轮廓"""
    selected_items = self.contourList.selectedItems()    # 获取选中的轮廓
    if not selected_items:    # 如果没有选中轮廓, 则显示原始图像
        self.updateDisplayedImage()
        return

    selected_contours = [item.data(Qt.UserRole) for item in selected_items]

    contour_image = self.image.copy()
    for cnt in selected_contours:
        cv2.drawContours(contour_image, [cnt], -1, (0, 255, 255), 3)

    self.displayImage(contour_image)


def displayImage(self, img):
    """显示图像的统一方法"""
    # 确保图像是3通道的
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # 转换为QImage
    h, w, ch = img.shape
    bytes_per_line = ch * w
    qimg = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

    self.label.setPixmap(QPixmap.fromImage(qimg))
    self.label.setAlignment(Qt.AlignCenter)
    self.label.fitToWindow()

def selectContourInList(self, contour_index):
    """在列表中选中指定的轮廓"""
    self.contourList.setCurrentRow(contour_index)
    self.updateContours()

def saveImage(self):
    """保存图像到指定文件夹"""
    if self.image is None:
        return

    new_img_dir = os.path.join(os.getcwd(), 'newImg')
    if not os.path.exists(new_img_dir):
        os.makedirs(new_img_dir)

    save_path, _ = QFileDialog.getSaveFileName(self, 'Save Image', new_img_dir, 'Images (*.png *.jpg *.bmp)')
    if save_path:
        image_to_save = self.label.contourImage if self.showContoursCheckBox.isChecked() else self.processedImage
        cv2.imwrite(save_path, image_to_save)
        print(f'图像已保存到: {save_path}')

def updateSliderState(self):
    """更新滑动条的启用状态"""
    print("updateSliderState called")
    enabled = self.rangeSearchCheckBox.isChecked()
    self.thresholdSlider.setEnabled(not enabled)
    self.grayRangeSlider.setEnabled(enabled)

def set_status(self, message):
    """更新状态信息"""
    print("set_status called")
    self.label.setText(message)
