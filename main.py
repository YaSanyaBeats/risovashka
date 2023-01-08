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

# hex Цвета, в соотсветствии с БД
colors = ['#CCCCCC', '#EB4C42', '#9F4576', '#318CE7', '#9457EB', '#8DA399', '#EEEEEE', '#222222', '#907C6A', '#FA6E79', '#50C878', '#F07427', '#F4CA16']

# Делаем QLabel кликабельным (используется при нажатии на картинки)
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

        # Получаем контент уровня с БД
        self.content = database.getContent(self.gameId)

        for index, row in enumerate(self.content.split('\n')):
            tmp = row.split(',')

            # задаём размеры уровня
            if index == 0:
                self.width = tmp[0]
                self.height = tmp[1]
                continue

            # запоминаем все цвета, которые используются в уровне
            for color in tmp:
                self.colors.add(color)

        # создаём кнопки палитры
        self.initColorButtons()

        # создаём кнопку очистить и привязываем функцию self.clearScene
        button = QPushButton("Очистить")
        button.clicked.connect(self.clearScene)

        self.ui.verticalLayout.addWidget(button)
        self.scene = QGraphicsScene()
        self.updateGraph()

        # если игра уже была запущена, то восстанавливаем прогресс
        if database.getStatus(self.gameId) == "In progress":
            self.loadProgress()

    def clearScene(self):
        # закрашиваем все плитки белым цветом и сохраняем прогресс
        for item in self.scene.items():
            if type(item) is QGraphicsRectItem:
                item.setBrush(QBrush(QColor('#ffffff')))
        self.saveProgress()
        database.deleteProgress(self.gameId)
    def loadProgress(self):
        # получаем прогресс с БД и закрашиваем плитки
        progress = database.getProgress(self.gameId).split(',')
        index = 0
        for item in self.scene.items():
            if type(item) is QGraphicsRectItem:
                item.setBrush(QBrush(QColor(progress[index])))
                index += 1

    def saveProgress(self):
        # перебираем все плитки и сохраняем в БД их цвета (это будет прогресс уровня)
        progress = ''
        for item in self.scene.items():
            if type(item) is QGraphicsRectItem:
                progress += item.brush().color().name() + ','
        database.setProgress(self.gameId, progress[:-1])

    # Выполняется при каждом нажатии на QPraphicsView
    def handlePress(self):

        items = self.scene.selectedItems()

        # перебираем все ВЫБРАННЫЕ плитки
        for item in items:
            x = item.rect().x() / 30 + 1
            y = item.rect().y() / 30

            # Если номер плитки НЕ соответствует цвету, в который плитка закрашена на данный момент, то
            if colors[int(self.contentMatrix[int(y) - 1][int(x) - 1])] != item.brush().color().name().upper():
                # меняем цвет плитки
                item.setBrush(QBrush(QColor(self.activeColor)))

        # сохраняем прогресс
        self.saveProgress()

        isComplete = True

        # получаем и перебираем все плитки
        allItems = self.scene.items()
        for item in allItems:
            if type(item) is QGraphicsRectItem:
                x = item.rect().x() / 30 + 1
                y = item.rect().y() / 30
                # если есть неправильно закрашенная плитка, то уровень считается НЕпройденным
                if colors[int(self.contentMatrix[int(y) - 1][int(x) - 1])] != item.brush().color().name().upper():
                    isComplete = False

        # если уровень пройден, то выводим сообщение
        if isComplete:
            QMessageBox.information(self, "Поздравляем", "Вы всё сделали правильно!",
                                    QMessageBox.Ok)



    def updateGraph(self):

        self.ui.mainGraph.setScene(self.scene)
        self.scene.selectionChanged.connect(self.handlePress)

        brush = QBrush(QColor(255, 255, 255, 255))
        pen = QPen(QColor(200, 200, 200, 255))
        font = QFont()
        text = QGraphicsTextItem()

        # располагаем прямоугольники на сцене
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
        # создаём кнопку палитры с нужным цветом
        button = QPushButton(colorId)
        button.clicked.connect(lambda: self.setActiveColor(colors[int(colorId)], colorId))
        button.setStyleSheet('QPushButton{background-color: ' + colors[int(colorId)] + ';}')
        self.ui.palette.addWidget(button)
        self.setActiveColor(colors[int(colorId)], colorId)

    def initColorButtons(self):
        # удаляем все кнопки с палитры и заполняем новыми кнопками
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

        # Загружаем html документ в виджет WebEngine
        self.ui.helpWidget.load(QUrl('file:///' + os.path.abspath("help/index.html").replace("\\", "/")))

        # При нажатии на кнопку выхода закрываем приложение
        self.ui.pushButton.clicked.connect(sys.exit)

        # При нажатии на Табы сверху, вызываем функцию seld.handleTab
        self.ui.tabWidget.tabBarClicked.connect(self.handleTab)

    def handleTab(self):
        # при смене таба заново инициализируем картинки уровней
        self.initLevels()


    def initLevel(self, index, level):
        tmpLayout = QVBoxLayout()
        tmpLabel = QLabel(level[1])
        tmpImage = ClickedLabel()
        tmpImage.setPixmap(QPixmap('assets/' + level[2]))
        tmpGameId = level[0]

        # При клике на картинку, запускаем соответствующий уровень
        tmpImage.clicked.connect(lambda: self.openGame(tmpGameId))

        tmpLayout.addWidget(tmpLabel)
        tmpLayout.addWidget(tmpImage)

        # Вставляем картинку в сетку уровней
        self.ui.gridLayout.addWidget(tmpImage, int(index / 5), index % 5, Qt.AlignmentFlag.AlignCenter)

    def initProgressLevel(self, index, level):
        tmpLayout = QVBoxLayout()
        tmpLabel = QLabel(level[1])
        tmpImage = ClickedLabel()
        tmpImage.setPixmap(QPixmap('assets/' + level[2]))
        tmpGameId = level[0]

        # При клике на картинку, запускаем соответствующий уровень
        tmpImage.clicked.connect(lambda: self.openGame(tmpGameId))
        tmpLayout.addWidget(tmpLabel)
        tmpLayout.addWidget(tmpImage)

        # Вставляем картинку в сетку уровней
        self.ui.gridLayout_3.addWidget(tmpImage, int(index / 5), index % 5, Qt.AlignmentFlag.AlignCenter)


    def initLevels(self):
        # получаем с базы данных все уровни
        self.levels = database.getLevels()

        # получаем с базы данных начатые уровни
        self.progressLevels = database.getProgressLevels()

        # Очищаем сетки уровней
        for i in reversed(range(self.ui.gridLayout_3.count())):
            self.ui.gridLayout_3.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.ui.gridLayout.count())):
            self.ui.gridLayout.itemAt(i).widget().setParent(None)

        # Заполняем сетки уровней
        for index, level in enumerate(self.levels):
            self.initLevel(index, level)

        for index, level in enumerate(self.progressLevels):
            self.initProgressLevel(index, level)


    # Запуск уровня
    def openGame(self, gameId):
        self.game = Game(self)
        self.game.setGame(gameId)
        self.game.show()





def main():
    app = QApplication()

    # загрузочный экран
    pixmap = QPixmap("splash.png")
    splash = QSplashScreen(pixmap)
    splash.show()

    app.processEvents()

    # запуск MainWindow
    window = MainWindow()
    window.setWindowIcon(QPixmap('splash.png'))
    window.show()

    # после запуска MainWindow закрываем загрузочный экран
    splash.finish(window)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

