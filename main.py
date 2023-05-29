#создай тут фоторедактор Easy Editor!
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog,QWidget,QTextEdit, QListWidget, QPushButton, QHBoxLayout, QGroupBox, QVBoxLayout, QLabel, QMessageBox, QRadioButton
from PyQt5.QtGui import QPixmap
import os
from PIL import Image, ImageFilter
from PIL.ImageFilter import SHARPEN


app = QApplication([])
mw = QWidget()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def choseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg', '.jpeg' , '.png', '.gif', '.bmp']
    choseWorkdir()
    files = os.listdir(workdir)
    filenames = filter(files, extensions)
    sp.clear()
    for filename in filenames:
        sp.addItem(filename)




class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir,filename)
        self.image = Image.open(image_path)

    def saveImage(self):
        path = os.path.join(workdir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)

        
    def showImage(self, path):
        car.hide()
        pixmapimage = QPixmap(path)
        w, h = car.width(), car.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        car.setPixmap(pixmapimage)
        car.show()

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

mw.setWindowTitle("Фото редактор")
p = QPushButton("Папка")
sp = QListWidget()
car = QLabel("Картинка")
but_1 = QPushButton("Лево")
but_2 = QPushButton("Право")
but_3 = QPushButton("Зеркало")
but_4 = QPushButton("Резкость")
but_5 = QPushButton("ЧБ")



row = QHBoxLayout()
lin_V1 = QVBoxLayout()
lin_V2 = QVBoxLayout()
dop_lin = QHBoxLayout()

lin_V1.addWidget(p)
lin_V1.addWidget(sp)

dop_lin.addWidget(but_1)
dop_lin.addWidget(but_2)
dop_lin.addWidget(but_3)
dop_lin.addWidget(but_4)
dop_lin.addWidget(but_5)

lin_V2.addWidget(car)
lin_V2.addLayout(dop_lin)

row.addLayout(lin_V1)
row.addLayout(lin_V2)
mw.setLayout(row)

workimage = ImageProcessor()

def showChosenImage():
    if sp.currentRow() >= 0:
        filename = sp.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)
but_1.clicked.connect(workimage.do_left)
but_5.clicked.connect(workimage.do_bw)
but_2.clicked.connect(workimage.do_right)
but_4.clicked.connect(workimage.do_sharpen)
but_3.clicked.connect(workimage.do_flip)

sp.currentRowChanged.connect(showChosenImage)
p.clicked.connect(showFilenamesList)
mw.show()
app.exec()