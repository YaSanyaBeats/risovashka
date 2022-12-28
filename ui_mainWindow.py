# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QMainWindow,
    QPushButton, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.mainTab = QWidget()
        self.mainTab.setObjectName(u"mainTab")
        self.horizontalLayout = QHBoxLayout(self.mainTab)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")

        self.horizontalLayout.addLayout(self.gridLayout)

        self.tabWidget.addTab(self.mainTab, "")
        self.progressTab = QWidget()
        self.progressTab.setObjectName(u"progressTab")
        self.verticalLayout_3 = QVBoxLayout(self.progressTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")

        self.verticalLayout_3.addLayout(self.gridLayout_3)

        self.tabWidget.addTab(self.progressTab, "")
        self.helpTab = QWidget()
        self.helpTab.setObjectName(u"helpTab")
        self.verticalLayout_2 = QVBoxLayout(self.helpTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.helpWidget = QWebEngineView(self.helpTab)
        self.helpWidget.setObjectName(u"helpWidget")
        self.helpWidget.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_2.addWidget(self.helpWidget)

        self.tabWidget.addTab(self.helpTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Raskraska", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mainTab), QCoreApplication.translate("MainWindow", u"Main", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.progressTab), QCoreApplication.translate("MainWindow", u"In progress", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.helpTab), QCoreApplication.translate("MainWindow", u"Help", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0445\u043e\u0434", None))
    # retranslateUi

