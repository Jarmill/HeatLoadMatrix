#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'filters_ui.ui'
#
# Created: Mon Jul  2 15:19:34 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(280, 178)
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 280, 178))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.material_1 = QtGui.QLineEdit(self.layoutWidget)
        self.material_1.setObjectName(_fromUtf8("material_1"))
        self.verticalLayout.addWidget(self.material_1)
        self.material_2 = QtGui.QLineEdit(self.layoutWidget)
        self.material_2.setObjectName(_fromUtf8("material_2"))
        self.verticalLayout.addWidget(self.material_2)
        self.material_3 = QtGui.QLineEdit(self.layoutWidget)
        self.material_3.setObjectName(_fromUtf8("material_3"))
        self.verticalLayout.addWidget(self.material_3)
        self.material_4 = QtGui.QLineEdit(self.layoutWidget)
        self.material_4.setObjectName(_fromUtf8("material_4"))
        self.verticalLayout.addWidget(self.material_4)
        self.material_5 = QtGui.QLineEdit(self.layoutWidget)
        self.material_5.setObjectName(_fromUtf8("material_5"))
        self.verticalLayout.addWidget(self.material_5)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.thickness_1 = QtGui.QLineEdit(self.layoutWidget)
        self.thickness_1.setObjectName(_fromUtf8("thickness_1"))
        self.verticalLayout_2.addWidget(self.thickness_1)
        self.thickness_2 = QtGui.QLineEdit(self.layoutWidget)
        self.thickness_2.setObjectName(_fromUtf8("thickness_2"))
        self.verticalLayout_2.addWidget(self.thickness_2)
        self.thickness_3 = QtGui.QLineEdit(self.layoutWidget)
        self.thickness_3.setObjectName(_fromUtf8("thickness_3"))
        self.verticalLayout_2.addWidget(self.thickness_3)
        self.thickness_4 = QtGui.QLineEdit(self.layoutWidget)
        self.thickness_4.setObjectName(_fromUtf8("thickness_4"))
        self.verticalLayout_2.addWidget(self.thickness_4)
        self.thickness_5 = QtGui.QLineEdit(self.layoutWidget)
        self.thickness_5.setObjectName(_fromUtf8("thickness_5"))
        self.verticalLayout_2.addWidget(self.thickness_5)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        """
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        """
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QtGui.qApp.quit)
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.material_1, self.thickness_1)
        Dialog.setTabOrder(self.thickness_1, self.material_2)
        Dialog.setTabOrder(self.material_2, self.thickness_2)
        Dialog.setTabOrder(self.thickness_2, self.material_3)
        Dialog.setTabOrder(self.material_3, self.thickness_3)
        Dialog.setTabOrder(self.thickness_3, self.material_4)
        Dialog.setTabOrder(self.material_4, self.thickness_4)
        Dialog.setTabOrder(self.thickness_4, self.material_5)
        Dialog.setTabOrder(self.material_5, self.thickness_5)
        Dialog.setTabOrder(self.thickness_5, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Filters")
        self.label.setText(QtGui.QApplication.translate("Dialog", "Material", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Thickness (μm)", None, QtGui.QApplication.UnicodeUTF8))

