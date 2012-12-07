# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xop_config_ui.ui'
#
# Created: Fri Dec  7 10:51:15 2012
#      by: PyQt4 UI code generator 4.9.2
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
        Dialog.resize(231, 84)
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 231, 85))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.xop_name = QtGui.QLineEdit(self.widget)
        self.xop_name.setObjectName(_fromUtf8("xop_name"))
        self.verticalLayout.addWidget(self.xop_name)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.xop_submit = QtGui.QPushButton(self.widget)
        self.xop_submit.setObjectName(_fromUtf8("xop_submit"))
        self.verticalLayout_2.addWidget(self.xop_submit)
        self.xop_box = QtGui.QDialogButtonBox(self.widget)
        self.xop_box.setOrientation(QtCore.Qt.Vertical)
        self.xop_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.xop_box.setObjectName(_fromUtf8("xop_box"))
        self.verticalLayout_2.addWidget(self.xop_box)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.xop_box, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.xop_box, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "XOP Configure", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Location of bin folder", None, QtGui.QApplication.UnicodeUTF8))
        self.xop_submit.setText(QtGui.QApplication.translate("Dialog", "Select Folder", None, QtGui.QApplication.UnicodeUTF8))

