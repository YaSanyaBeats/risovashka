import sys
import os

import database

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QMessageBox, QTableWidgetItem, QPushButton, QSplashScreen, QVBoxLayout, QGraphicsScene, QGraphicsTextItem, QGraphicsItem
from PySide6.QtCore import QCoreApplication, Signal
from PySide6.QtCore import Qt, QUrl, SIGNAL
from PySide6.QtGui import QIcon, QPixmap, QBrush, QPen, QColor, QFont
from PySide6.QtWebEngineWidgets import *

from ui_mainWindow import Ui_MainWindow
from ui_game import Ui_Game

colors = ['#CCCCCC', '#EB4C42', '#9F4576', '#318CE7', '#9457EB', '#8DA399', '#FFFFFF', '#000000', '#907C6A', '#FA6E79', '#50C878', '#F07427', '#F4CA16']

class ClickedLabel(QLabel):
    clicked = Signal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)

        self.clicked.emit()

class Game(QMainWindow):
    def __init__(self, parent=None):
        super(Game, self).__init__(parent)
        self.ui = Ui_Game()
        self.gameId = None
        self.ui.setupUi(self)
        self.colors = set()
        self.content = None
        self.width = None
        self.height = None
        self.activeColor = ''

    def setGame(self, gameId):
        self.gameId = gameId
        self.content = database.getContent(self.gameId)

        for index, row in enumerate(self.content.split('\n')):
            tmp = row.split(',')
            if index == 0:
                self.width = tmp[0]
                self.height = tmp[1]
                continue
            for color in tmp:
                self.colors.add(color)
        self.initColorButtons()
        self.scene = QGraphicsScene()
        self.updateGraph()

    def handlePress(self):
        items = self.scene.selectedItems()
        for item in items:
            print(item.setBrush(QBrush(QColor(self.activeColor))))

    def updateGraph(self):

        self.ui.mainGraph.setScene(self.scene)
        self.scene.selectionChanged.connect(self.handlePress)

        brush = QBrush(QColor(255, 255, 255, 255))
        pen = QPen(QColor(200, 200, 200, 255))
        font = QFont()
        text = QGraphicsTextItem()

        for index, row in enumerate(self.content.split('\n')):
            if index == 0:
                continue
            tmp = row.split(',')
            for inner_index, cell in enumerate(tmp):
                rect = self.scene.addRect(index * 30, inner_index * 30, 30, 30, pen, brush)
                rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

                text = self.scene.addText(cell, font)
                text.setPos(index * 30, inner_index * 30)

    def setActiveColor(self, color):
        self.activeColor = color

    def createButton(self, colorId):
        button = QPushButton(colorId)
        button.clicked.connect(lambda: self.setActiveColor(colors[int(colorId)]))
        button.setStyleSheet('QPushButton{background-color: ' + colors[int(colorId)] + ';}')
        self.ui.palette.addWidget(button)
        self.setActiveColor(colors[int(colorId)])

    def initColorButtons(self):
        layout = self.ui.palette
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

        for colorId in self.colors:
            self.createButton(colorId)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.levels = database.getLevels()
        self.initLevels()

    def initLevel(self, index, level):
        tmpLayout = QVBoxLayout()
        tmpLabel = QLabel(level[1])
        tmpImage = ClickedLabel()
        tmpImage.setPixmap(QPixmap('assets/' + level[2]))
        tmpGameId = level[0]
        tmpImage.clicked.connect(lambda: self.openGame(tmpGameId))
        tmpLayout.addWidget(tmpLabel)
        tmpLayout.addWidget(tmpImage)
        self.ui.gridLayout.addWidget(tmpImage, (int)(index / 5), index % 5, Qt.AlignmentFlag.AlignCenter)

    def initLevels(self):
        for index, level in enumerate(self.levels):
            self.initLevel(index, level)


    def openGame(self, gameId):
        self.game = Game(self)
        self.game.setGame(gameId)
        self.game.show()





def main():
    app = QApplication()
    pixmap = QPixmap("splash.png")
    splash = QSplashScreen(pixmap)
    splash.show()
    app.processEvents()

    window = MainWindow()
    window.setWindowIcon(QPixmap('splash.png'))
    window.show()
    splash.finish(window)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

