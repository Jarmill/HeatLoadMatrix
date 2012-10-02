#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'heatbump_ui.ui'
#
# Created: Mon Jul  2 15:19:53 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(280, 90)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 71))
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(100, 0, 175, 85))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.undButton = QtGui.QPushButton(self.layoutWidget)
        self.undButton.setObjectName(_fromUtf8("undButton"))
        self.verticalLayout.addWidget(self.undButton)
        self.wigButton = QtGui.QPushButton(self.layoutWidget)
        self.wigButton.setObjectName(_fromUtf8("wigButton"))
        self.verticalLayout.addWidget(self.wigButton)
        self.bmagButton = QtGui.QPushButton(self.layoutWidget)
        self.bmagButton.setObjectName(_fromUtf8("bmagButton"))
        self.bmagButton.setEnabled(False)
        self.verticalLayout.addWidget(self.bmagButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.filterButton = QtGui.QPushButton(self.layoutWidget)
        self.filterButton.setObjectName(_fromUtf8("filterButton"))
        self.verticalLayout_2.addWidget(self.filterButton)
        self.regionButton = QtGui.QPushButton(self.layoutWidget)
        self.regionButton.setObjectName(_fromUtf8("regionButton"))
        self.verticalLayout_2.addWidget(self.regionButton)
        self.aboutButton = QtGui.QPushButton(self.layoutWidget)
        self.aboutButton.setObjectName(_fromUtf8("aboutButton"))
        self.verticalLayout_2.addWidget(self.aboutButton)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        #MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        #Button functionality goes here
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("HeatBump")
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Generates ANSYS mesh that maps power flux", None, QtGui.QApplication.UnicodeUTF8))
        self.undButton.setText(QtGui.QApplication.translate("MainWindow", "Undulator", None, QtGui.QApplication.UnicodeUTF8))
        self.wigButton.setText(QtGui.QApplication.translate("MainWindow", "Wiggler", None, QtGui.QApplication.UnicodeUTF8))
        self.bmagButton.setText(QtGui.QApplication.translate("MainWindow", "Bending Magnet", None, QtGui.QApplication.UnicodeUTF8))
        self.filterButton.setText(QtGui.QApplication.translate("MainWindow", "Filters", None, QtGui.QApplication.UnicodeUTF8))
        self.regionButton.setText(QtGui.QApplication.translate("MainWindow", "Region Param.", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutButton.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))

