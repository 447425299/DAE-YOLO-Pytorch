# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'detect_ui_v3.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)
import icon_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1246, 589)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame_5 = QFrame(self.centralwidget)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setGeometry(QRect(-40, -40, 1331, 691))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setStyleSheet(u"")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.frame_5)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 130, 400, 320))
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"\n"
"")
        self.label.setLineWidth(1)
        self.label.setScaledContents(False)
        self.label_14 = QLabel(self.frame_5)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(460, 130, 400, 320))
        self.label_14.setStyleSheet(u"\n"
"background-color: rgb(255, 255, 255);\n"
"")
        self.label_14.setLineWidth(1)
        self.pushButton_openimg = QPushButton(self.frame_5)
        self.pushButton_openimg.setObjectName(u"pushButton_openimg")
        self.pushButton_openimg.setGeometry(QRect(240, 510, 151, 51))
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(5)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_openimg.sizePolicy().hasHeightForWidth())
        self.pushButton_openimg.setSizePolicy(sizePolicy2)
        self.pushButton_openimg.setMaximumSize(QSize(16777215, 63))
        icon = QIcon()
        icon.addFile(u":/img/img/\u6587\u4ef6.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_openimg.setIcon(icon)
        self.pushButton_openimg.setAutoRepeatDelay(301)
        self.pushButton_openimg.setAutoRepeatInterval(100)
        self.pushButton_start_stop = QPushButton(self.frame_5)
        self.pushButton_start_stop.setObjectName(u"pushButton_start_stop")
        self.pushButton_start_stop.setGeometry(QRect(520, 510, 151, 51))
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(5)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButton_start_stop.sizePolicy().hasHeightForWidth())
        self.pushButton_start_stop.setSizePolicy(sizePolicy3)
        self.pushButton_start_stop.setMaximumSize(QSize(16777215, 63))
        icon1 = QIcon()
        icon1.addFile(u":/img/img/\u8fd0\u884c.png", QSize(), QIcon.Normal, QIcon.Off)
        icon1.addFile(u":/img/img/\u6682\u505c.png", QSize(), QIcon.Normal, QIcon.On)
        self.pushButton_start_stop.setIcon(icon1)
        self.pushButton_start_stop.setCheckable(True)
        self.pushButton_exit = QPushButton(self.frame_5)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setGeometry(QRect(1120, 510, 131, 51))
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(5)
        sizePolicy4.setVerticalStretch(2)
        sizePolicy4.setHeightForWidth(self.pushButton_exit.sizePolicy().hasHeightForWidth())
        self.pushButton_exit.setSizePolicy(sizePolicy4)
        self.pushButton_exit.setMaximumSize(QSize(16777215, 63))
        icon2 = QIcon()
        icon2.addFile(u":/img/img/\u7ed3\u675f.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_exit.setIcon(icon2)
        self.label_3 = QLabel(self.frame_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(40, 60, 1321, 41))
        font = QFont()
        font.setFamilies([u"\u534e\u6587\u6977\u4f53"])
        font.setPointSize(17)
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_15 = QLabel(self.frame_5)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(870, 130, 400, 320))
        self.label_15.setStyleSheet(u"\n"
"background-color: rgb(255, 255, 255);\n"
"")
        self.label_15.setLineWidth(1)
        self.pushButton_start_stop_2 = QPushButton(self.frame_5)
        self.pushButton_start_stop_2.setObjectName(u"pushButton_start_stop_2")
        self.pushButton_start_stop_2.setGeometry(QRect(810, 510, 141, 51))
        sizePolicy3.setHeightForWidth(self.pushButton_start_stop_2.sizePolicy().hasHeightForWidth())
        self.pushButton_start_stop_2.setSizePolicy(sizePolicy3)
        self.pushButton_start_stop_2.setMaximumSize(QSize(16777215, 63))
        self.pushButton_start_stop_2.setIcon(icon1)
        self.pushButton_start_stop_2.setCheckable(True)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText("")
        self.label_14.setText("")
        self.pushButton_openimg.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4f20\u56fe\u7247/\u89c6\u9891", None))
        self.pushButton_start_stop.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb/\u6682\u505c\u68c0\u6d4b", None))
        self.pushButton_exit.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u675f", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u57fa\u4e8e\u6df1\u5ea6\u5b66\u4e60\u7684\u5f31\u5c0f\u76ee\u6807\u68c0\u6d4b\u7cfb\u7edf", None))
        self.label_15.setText("")
        self.pushButton_start_stop_2.setText(QCoreApplication.translate("MainWindow", u"\u70ed\u529b\u56fe\u751f\u6210", None))
    # retranslateUi

