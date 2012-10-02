#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'about_ui.ui'
#
# Created: Mon Jul  2 16:33:17 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(324, 150)
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 321, 151))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.retranslateUi(Dialog)
        """
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QtCore.QCoreApplication.instance().quit)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QtCore.QCoreApplication.instance().quit)
        """
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("About")
        self.label.setText(QtGui.QApplication.translate("Dialog", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse eget nibh ornare orci viverra bibendum. Pellentesque at velit a dui placerat volutpat nec eu metus. Etiam eget mauris ultricies tortor dapibus hendrerit nec eget massa. Sed velit sem, semper eu lobortis nec, pellentesque et tellus. Proin volutpat, nibh at iaculis venenatis, neque elit ornare dui, a pretium sapien eros ut neque. Sed lorem turpis, euismod ut lacinia non, mollis eget dui. Praesent neque nulla, tristique ac pellentesque in, vestibulum quis purus. Change this text.", None, QtGui.QApplication.UnicodeUTF8))

