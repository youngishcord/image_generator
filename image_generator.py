from typing import Optional
from PIL import Image, ImageDraw
from random import randint
import sys
import PySide6
from PySide6 import (QtCore, QtWidgets, QtGui)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox,
                               QPushButton, QFileDialog, QLabel)
from PySide6.QtCore import (Slot, Signal)


class ImageGenerator(QMainWindow):
    
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.setFixedSize(QtCore.QSize(400, 600))
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.lay = QtWidgets.QVBoxLayout(self.widget)

        self.figure_type = QtWidgets.QComboBox()
        self.figure_type.addItems(['Квадрат', 'Круг', 'Треугольник'])
        self.lay.addWidget(self.figure_type)

        self.lay.addWidget(QLabel("Размер изображений"))
        self.image_size = (64, 64)
        self.x_size = QtWidgets.QSpinBox()
        self.x_size.setValue(self.image_size[0])
        self.x_size.setMinimum(1)
        self.x_size.setMaximum(4096)
        self.x_size.valueChanged.connect(self.set_image_size)
        self.y_size = QtWidgets.QSpinBox()
        self.y_size.setValue(self.image_size[1])
        self.y_size.setMinimum(1)
        self.y_size.setMaximum(4096)
        self.y_size.valueChanged.connect(self.set_image_size)
        size_lay = QtWidgets.QHBoxLayout()
        size_lay.addWidget(self.x_size)
        size_lay.addWidget(self.y_size)
        self.lay.addLayout(size_lay)

        self.fixed_figure_size = QtWidgets.QCheckBox()
        self.lay.addWidget(QLabel("Фиксированный размер фигуры"))
        self.lay.addWidget(self.fixed_figure_size)
        self.fixed_figure_size.setChecked(True)
        self.fixed_figure_size.setEnabled(False) ################################################################################

        self.quantity = 10
        self.quantity_widget = QtWidgets.QSpinBox()
        self.quantity_widget.setMinimum(1)
        self.quantity_widget.setValue(self.quantity)
        self.quantity_widget.valueChanged.connect(self.set_quantity)
        self.lay.addWidget(QLabel("Количество изображений"))
        self.lay.addWidget(self.quantity_widget)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(QLabel("Цвет фона"), 0, 0)
        grid.addWidget(QLabel("Цвет фигуры"), 0, 1)

        self.figure_color = "black"
        self.figure_color_widget = QtWidgets.QPushButton()
        self.figure_color_widget.clicked.connect(self.set_figure_color)
        self.figure_color_widget.setStyleSheet(f"background-color: {self.figure_color}")
        grid.addWidget(self.figure_color_widget, 1, 0)

        self.bg_color = "white"
        self.bg_color_widget = QtWidgets.QPushButton()
        self.bg_color_widget.clicked.connect(self.set_background_color)
        self.bg_color_widget.setStyleSheet(f"background-color: {self.bg_color}")
        grid.addWidget(self.bg_color_widget, 1, 1)
        
        self.lay.addLayout(grid)

        self.lay.addWidget(QLabel("Путь для сохранения"))
        path_lay = QtWidgets.QHBoxLayout()
        self.lay.addLayout(path_lay)
        self.path_line = QtWidgets.QLineEdit()
        self.path_line.setReadOnly(True)
        self.path_line.setText("./")
        path_lay.addWidget(self.path_line)

        self.path_bt = QtWidgets.QPushButton("Путь")
        self.path_bt.clicked.connect(self.set_path)
        path_lay.addWidget(self.path_bt)

        self.create_bt = QtWidgets.QPushButton()
        self.create_bt.setText("Создать изображения")
        self.create_bt.clicked.connect(self.create_images)
        self.lay.addWidget(self.create_bt)

    def set_figure_color(self):
        q = QtWidgets.QColorDialog.getColor().name()
        self.figure_color_widget.setStyleSheet(f"background-color: {q}")
        self.figure_color = q

    def set_background_color(self):
        q = QtWidgets.QColorDialog.getColor().name()
        self.bg_color_widget.setStyleSheet(f"background-color: {q}")
        self.bg_color = q

    def set_quantity(self):
        self.quantity = self.quantity_widget.value()

    def set_path(self):
        self.path_line.setText(QFileDialog.getExistingDirectory(self, "Укажите путь сохранения") + "/")

    def set_image_size(self):
        self.image_size = (self.x_size.value(), self.y_size.value())

    def draw_square(self, draw: ImageDraw, x1, x2, delta):
        draw.rectangle([(x1, x2), (x1+delta, x2+delta)], fill=self.figure_color, outline=self.figure_color)

    def draw_circle(self, draw: ImageDraw, x1, x2, delta):
        draw.ellipse([(x1, x2), (x1+delta, x2+delta)], fill=self.figure_color, outline=self.figure_color)

    def draw_triangle(self):
        pass

    def get_func(self, *args):
        types = {
            'Квадрат': self.draw_square,
            'Круг': self.draw_circle,
            'Треугольник': self.draw_triangle,
        }
        return types[self.figure_type.currentText()](*args)

    # Нужны: размеры, количество, форма, цвет фона, цвет фигуры
    def create_images(self):
        for i in range(self.quantity):
            delta = 10**(len(str(min(self.image_size)))-1)
            x1, x2 = (randint(0, self.image_size[0]-delta), randint(0, self.image_size[1]-delta))
            image = Image.new("RGB", self.image_size, self.bg_color)
            draw = ImageDraw.Draw(image)

            self.get_func(draw, x1, x2, delta)
            
            image.save(f"./images/image_{i}.png")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageGenerator()
    window.show()
    app.exec()