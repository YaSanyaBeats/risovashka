import sys
import os

import database

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QMessageBox, QTableWidgetItem, QPushButton, QSplashScreen, QVBoxLayout, QGraphicsScene, QGraphicsTextItem, QGraphicsItem, QGraphicsRectItem
from PySide6.QtCore import QCoreApplication, Signal
from PySide6.QtCore import Qt, QUrl, SIGNAL
from PySide6.QtGui import QIcon, QPixmap, QBrush, QPen, QColor, QFont
from PySide6.QtWebEngineWidgets import *

from ui_mainWindow import Ui_MainWindow
from ui_game import Ui_Game

colors = ['#CCCCCC', '#EB4C42', '#9F4576', '#318CE7', '#9457EB', '#8DA399', '#EEEEEE', '#222222', '#907C6A', '#FA6E79', '#50C878', '#F07427', '#F4CA16']

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
        self.activeColorId = 0
        self.contentMatrix = []

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
        button = QPushButton("Очистить")
        button.clicked.connect(self.clearScene)
        self.ui.verticalLayout.addWidget(button)
        self.scene = QGraphicsScene()
        self.updateGraph()

        if database.getStatus(self.gameId) == "In progress":
            self.loadProgress()

    def clearScene(self):
        for item in self.scene.items():
            if type(item) is QGraphicsRectItem:
                item.setBrush(QBrush(QColor('#ffffff')))
        self.saveProgress()
        database.deleteProgress(self.gameId)
    def loadProgress(self):
        progress = database.getProgress(self.gameId).split(',')
        index = 0
        for item in self.scene.items():
            if type(item) is QGraphicsRectItem:
                item.setBrush(QBrush(QColor(progress[index])))
                index += 1

    def saveProgress(self):
        progress = ''
        for item in self.scene.items():
            if type(item) is QGraphicsRectItem:
                progress += item.brush().color().name() + ','
        database.setProgress(self.gameId, progress[:-1])

    def handlePress(self):
        items = self.scene.selectedItems()
        for item in items:
            x = item.rect().x() / 30 + 1
            y = item.rect().y() / 30
            print(int(x) - 1, int(y) - 1)
            print(int(self.contentMatrix[int(y) - 1][int(x) - 1]))
            if colors[int(self.contentMatrix[int(y) - 1][int(x) - 1])] != item.brush().color().name().upper():
                item.setBrush(QBrush(QColor(self.activeColor)))

        self.saveProgress()



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
            self.contentMatrix.append([])
            for inner_index, cell in enumerate(tmp):
                self.contentMatrix[index - 1].append(cell)
                rect = self.scene.addRect(inner_index * 30, index * 30, 30, 30, pen, brush)
                rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

                text = self.scene.addText(cell, font)
                text.setPos(inner_index * 30, index * 30)

    def setActiveColor(self, color, colorId):
        self.activeColor = color
        self.activeColorId = colorId

    def createButton(self, colorId):
        button = QPushButton(colorId)
        button.clicked.connect(lambda: self.setActiveColor(colors[int(colorId)], colorId))
        button.setStyleSheet('QPushButton{background-color: ' + colors[int(colorId)] + ';}')
        self.ui.palette.addWidget(button)
        self.setActiveColor(colors[int(colorId)], colorId)

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

        self.levels = None
        self.progressLevels = None
        self.initLevels()

        self.ui.helpWidget.load(QUrl('file:///' + os.path.abspath("help/index.html").replace("\\", "/")))
        self.ui.pushButton.clicked.connect(sys.exit)

        self.ui.tabWidget.tabBarClicked.connect(self.handleTab)

    def handleTab(self):
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
        self.ui.gridLayout.addWidget(tmpImage, int(index / 5), index % 5, Qt.AlignmentFlag.AlignCenter)

    def initProgressLevel(self, index, level):
        tmpLayout = QVBoxLayout()
        tmpLabel = QLabel(level[1])
        tmpImage = ClickedLabel()
        tmpImage.setPixmap(QPixmap('assets/' + level[2]))
        tmpGameId = level[0]
        tmpImage.clicked.connect(lambda: self.openGame(tmpGameId))
        tmpLayout.addWidget(tmpLabel)
        tmpLayout.addWidget(tmpImage)
        self.ui.gridLayout_3.addWidget(tmpImage, int(index / 5), index % 5, Qt.AlignmentFlag.AlignCenter)


    def initLevels(self):
        self.levels = database.getLevels()
        self.progressLevels = database.getProgressLevels()

        for i in reversed(range(self.ui.gridLayout_3.count())):
            self.ui.gridLayout_3.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.ui.gridLayout.count())):
            self.ui.gridLayout.itemAt(i).widget().setParent(None)

        for index, level in enumerate(self.levels):
            self.initLevel(index, level)

        for index, level in enumerate(self.progressLevels):
            self.initProgressLevel(index, level)


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

