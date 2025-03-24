from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, \
    QComboBox, QCheckBox, QSlider, QLineEdit, QListWidget, QListWidgetItem, QFileDialog, QInputDialog

from widget import ImageLabel
from function import *
from function import thumbnailClicked





class MainWindow(QMainWindow):
    """主窗口类，处理图像的打开、分析、保存等功能"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def loadThumbnails(self):
        loadThumbnails(self)

    def contourImage(self):
        self.contourImage(self)

    def thumbnailClicked(self):
        thumbnailClicked(self, self.thumbnailList.currentItem())    # 传递当前选中的缩略图项, 传递给函数 thumbnailClicked

    def loadImage(self, fileName):
        loadImage(self, fileName)
    def processImage(self):
        processImage(self)
    #
    def openImage(self):
        openImage(self)

    def displayImage(self, img):
        displayImage(self, self.image)
    #

    def selectContourInList(self):
        selectContourInList(self)

    def promptImageSize(self):
        promptImageSize(self)
    #
    def saveImage(self):
        saveImage(self)
    #
    def updateDisplayedImage(self):
        updateDisplayedImage(self)
    #
    def updateSliderState(self):
        updateSliderState(self)

    def set_status(self):
        set_status(self)

    def updateContours(self):
        updateContours(self)


    def initUI(self):
        """初始化用户界面"""
        self.setWindowTitle('肿瘤识别')
        self.width = 1400
        self.height = 800
        self.resize(self.width, self.height)

        # 设置背景颜色为黑色
        self.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")

        # 设置字体
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

        # 创建图像标签，用于显示图像
        self.label = ImageLabel(self)
        self.label.setText("未选择图像")
        self.label.setStyleSheet("background-color: #3c3f41;")

        # 打开图像按钮
        self.selectButton = QPushButton('打开图像', self)
        self.selectButton.clicked.connect(self.openImage)

        # 选择单位下拉框
        self.unitComboBox = QComboBox()
        self.unitComboBox.addItems(['像素', '厘米'])
        self.unitComboBox.currentIndexChanged.connect(self.promptImageSize) # 连接下拉框的信号和槽函数

        # 分析图像按钮
        self.processButton = QPushButton('分析图像', self)
        self.processButton.clicked.connect(self.processImage)

        # 保存图像按钮
        self.saveButton = QPushButton('保存图像', self)
        self.saveButton.clicked.connect(self.saveImage)

        # 仅显示轮廓勾选框
        self.showContoursCheckBox = QCheckBox('仅显示轮廓')
        self.showContoursCheckBox.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
        self.showContoursCheckBox.stateChanged.connect(self.updateDisplayedImage)

        # 灰度阈值滑动条
        self.thresholdSlider = QSlider(Qt.Horizontal)
        self.thresholdLabel = QLabel('灰度阈值:')
        self.thresholdValueLabel = QLabel(str(self.thresholdSlider.value()))
        self.thresholdSlider.setMinimum(0)
        self.thresholdSlider.setMaximum(255)
        self.thresholdSlider.setValue(150)
        self.thresholdSlider.valueChanged.connect(self.processImage)




        # 范围查找灰度勾选框
        self.rangeSearchCheckBox = QCheckBox('范围查找灰度')
        self.rangeSearchCheckBox.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }")
        self.rangeSearchCheckBox.stateChanged.connect(self.updateSliderState)

        # 灰度范围滑动条
        self.grayRangeLabel = QLabel('灰度范围:')
        self.grayRangeSlider = QSlider(Qt.Horizontal)
        self.grayRangeSlider.setMinimum(0)
        self.grayRangeSlider.setMaximum(255)
        self.grayRangeSlider.setValue(100)
        self.grayRangeSlider.setTickPosition(QSlider.TicksBelow)
        self.grayRangeSlider.setTickInterval(10)
        self.grayRangeSlider.setSingleStep(1)
        self.grayRangeSlider.setEnabled(False)
        self.grayRangeSlider.valueChanged.connect(self.processImage)
        self.grayRangeValueLabel = QLineEdit()
        self.grayRangeValueLabel.setReadOnly(True)
        self.grayRangeValueLabel.setStyleSheet("background-color: #3c3f41; color: #ffffff;")

        # 创建缩略图列表
        thumbnailLayout = QVBoxLayout()        # 创建垂直布局
        thumbnailLayout.addWidget(self.unitComboBox)       # 添加单位选择框
        thumbnailLayout.addWidget(self.selectButton)        # 添加选择按钮
        thumbnailLayout.addStretch()            # 添加拉伸因子，使按钮靠上对齐
        self.thumbnailList = QListWidget()        # 创建缩略图列表
        self.thumbnailList.setViewMode(QListWidget.IconMode)    # 设置视图模式为图标模式
        self.thumbnailList.setIconSize(QSize(100, 100))        # 设置图标大小
        self.thumbnailList.setResizeMode(QListWidget.Adjust)    # 设置调整模式
        self.thumbnailList.itemClicked.connect(self.thumbnailClicked)        # 连接点击事件
        thumbnailLayout.addWidget(self.thumbnailList, 1)       # 添加缩略图列表，并设置拉伸因子为1，使列表占据剩余空间

        # 创建轮廓列表
        self.contourList = QListWidget()
        self.contourList.setSelectionMode(QListWidget.MultiSelection)
        self.contourList.itemSelectionChanged.connect(self.updateContours)

        # 创建按钮和滑动条布局
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.showContoursCheckBox,2)
        buttonLayout.addWidget(self.processButton,5)
        buttonLayout.addWidget(self.saveButton,5)

        sliderLayout1 = QHBoxLayout()     # 创建水平布局
        sliderLayout1.addWidget(self.thresholdLabel,2)   # 添加标签和滑动条
        sliderLayout1.addWidget(self.thresholdValueLabel,2)   # 添加标签和滑动条
        sliderLayout1.addWidget(self.thresholdSlider,20)

        sliderLayout2 = QHBoxLayout()
        sliderLayout2.addWidget(self.rangeSearchCheckBox)
        sliderLayout2.addWidget(self.grayRangeLabel)
        sliderLayout2.addWidget(self.grayRangeValueLabel)

        sliderLayout3 = QHBoxLayout()
        sliderLayout3.addWidget(self.grayRangeSlider)


        buttonSliderLayout = QVBoxLayout()
        buttonSliderLayout.addLayout(sliderLayout1)
        buttonSliderLayout.addLayout(sliderLayout2)
        buttonSliderLayout.addLayout(sliderLayout3)


        # 创建主布局
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(thumbnailLayout, 1)    # 添加缩略图列表，并设置拉伸因子为1，使列表占据剩余空间
        mainLayout.addWidget(self.label, 6)    # 添加图像标签
        mainLayout.addWidget(self.contourList, 1)    # 添加轮廓列表

        layout = QVBoxLayout()    # 创建主布局
        layout.addLayout(mainLayout)    # 添加主布局
        layout.addLayout(buttonLayout)    # 添加按钮布局
        layout.addLayout(buttonSliderLayout)    # 添加按钮布局


        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 初始化变量
        self.imagePath = None
        self.image = None
        self.pixel_per_cm = None

        # 加载缩略图
        self.loadThumbnails()



    def displayImage(self, img):
        """显示图像"""
        #若此时未点击识别图像，不进行处理
        if self.image is None:
            return 0

        qformat = QImage.Format_Indexed8 if len(img.shape) == 2 else QImage.Format_RGB888   # 若为灰度图像，则使用 Format_Indexed8 格式
        img = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], qformat) # 将图像转换为 QImage 格式
        img = img.rgbSwapped()  # 将图像颜色通道转换为 RGB 格式
        self.label.setPixmap(QPixmap.fromImage(img))    # 将 QImage 转换为 QPixmap 并显示在标签中
        self.label.setAlignment(Qt.AlignCenter) # 设置标签的对齐方式, 居中对齐
        self.label.fitToWindow()    # 调整标签大小以适应图像
