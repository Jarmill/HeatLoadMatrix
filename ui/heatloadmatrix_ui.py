# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'heatbump_w_ui.ui'
#
# Created: Mon Nov 26 12:17:08 2012
#      by: PyQt4 UI code generator 4.9.2
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
        MainWindow.resize(660, 565)
        self.HeatLoadMatrix_2 = QtGui.QWidget(MainWindow)
        self.HeatLoadMatrix_2.setObjectName(_fromUtf8("HeatLoadMatrix_2"))
        self.layoutWidget = QtGui.QWidget(self.HeatLoadMatrix_2)
        self.layoutWidget.setGeometry(QtCore.QRect(1, 1, 661, 526))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_15 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_15.setMargin(0)
        self.verticalLayout_15.setObjectName(_fromUtf8("verticalLayout_15"))
        self.SourceConfiguration_groupBox = QtGui.QGroupBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SourceConfiguration_groupBox.sizePolicy().hasHeightForWidth())
        self.SourceConfiguration_groupBox.setSizePolicy(sizePolicy)
        self.SourceConfiguration_groupBox.setObjectName(_fromUtf8("SourceConfiguration_groupBox"))
        self.verticalLayout_14 = QtGui.QVBoxLayout(self.SourceConfiguration_groupBox)
        self.verticalLayout_14.setObjectName(_fromUtf8("verticalLayout_14"))
        self.splitter_3 = QtGui.QSplitter(self.SourceConfiguration_groupBox)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName(_fromUtf8("splitter_3"))
        self.layoutWidget1 = QtGui.QWidget(self.splitter_3)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.source_und = QtGui.QRadioButton(self.layoutWidget1)
        self.source_und.setChecked(True)
        self.source_und.setObjectName(_fromUtf8("source_und"))
        self.verticalLayout.addWidget(self.source_und)
        self.source_wig = QtGui.QRadioButton(self.layoutWidget1)
        self.source_wig.setObjectName(_fromUtf8("source_wig"))
        self.verticalLayout.addWidget(self.source_wig)
        self.source_bend = QtGui.QRadioButton(self.layoutWidget1)
        self.source_bend.setEnabled(False)
        self.source_bend.setObjectName(_fromUtf8("source_bend"))
        self.verticalLayout.addWidget(self.source_bend)
        self.config_source = QtGui.QPushButton(self.splitter_3)
        self.config_source.setObjectName(_fromUtf8("config_source"))
        self.layoutWidget_6 = QtGui.QWidget(self.splitter_3)
        self.layoutWidget_6.setObjectName(_fromUtf8("layoutWidget_6"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget_6)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.SelectedSource_Label = QtGui.QLabel(self.layoutWidget_6)
        self.SelectedSource_Label.setObjectName(_fromUtf8("SelectedSource_Label"))
        self.horizontalLayout_2.addWidget(self.SelectedSource_Label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.imported_source = QtGui.QLineEdit(self.layoutWidget_6)
        self.imported_source.setObjectName(_fromUtf8("imported_source"))
        self.horizontalLayout_2.addWidget(self.imported_source)
        self.verticalLayout_14.addWidget(self.splitter_3)
        self.verticalLayout_15.addWidget(self.SourceConfiguration_groupBox)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.verticalLayout_13 = QtGui.QVBoxLayout()
        self.verticalLayout_13.setObjectName(_fromUtf8("verticalLayout_13"))
        self.ObjectConfiguration_groupBox = QtGui.QGroupBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ObjectConfiguration_groupBox.sizePolicy().hasHeightForWidth())
        self.ObjectConfiguration_groupBox.setSizePolicy(sizePolicy)
        self.ObjectConfiguration_groupBox.setObjectName(_fromUtf8("ObjectConfiguration_groupBox"))
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.ObjectConfiguration_groupBox)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.splitter_2 = QtGui.QSplitter(self.ObjectConfiguration_groupBox)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.layoutWidget_2 = QtGui.QWidget(self.splitter_2)
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.ObjectMaterial_label = QtGui.QLabel(self.layoutWidget_2)
        self.ObjectMaterial_label.setObjectName(_fromUtf8("ObjectMaterial_label"))
        self.horizontalLayout_5.addWidget(self.ObjectMaterial_label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.mat = QtGui.QLineEdit(self.layoutWidget_2)
        self.mat.setObjectName(_fromUtf8("mat"))
        self.horizontalLayout_5.addWidget(self.mat)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.DistancetotheSource_label = QtGui.QLabel(self.layoutWidget_2)
        self.DistancetotheSource_label.setObjectName(_fromUtf8("DistancetotheSource_label"))
        self.horizontalLayout_6.addWidget(self.DistancetotheSource_label)
        self.dist = QtGui.QLineEdit(self.layoutWidget_2)
        self.dist.setObjectName(_fromUtf8("dist"))
        self.horizontalLayout_6.addWidget(self.dist)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.InclinationtotheBeam_label = QtGui.QLabel(self.layoutWidget_2)
        self.InclinationtotheBeam_label.setObjectName(_fromUtf8("InclinationtotheBeam_label"))
        self.horizontalLayout_7.addWidget(self.InclinationtotheBeam_label)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.deg = QtGui.QLineEdit(self.layoutWidget_2)
        self.deg.setEnabled(False)
        self.deg.setObjectName(_fromUtf8("deg"))
        self.horizontalLayout_7.addWidget(self.deg)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.config_region = QtGui.QPushButton(self.splitter_2)
        self.config_region.setObjectName(_fromUtf8("config_region"))
        self.verticalLayout_11.addWidget(self.splitter_2)
        self.verticalLayout_13.addWidget(self.ObjectConfiguration_groupBox)
        self.ObjectMeshConfiguration_groupBox = QtGui.QGroupBox(self.layoutWidget)
        self.ObjectMeshConfiguration_groupBox.setObjectName(_fromUtf8("ObjectMeshConfiguration_groupBox"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.ObjectMeshConfiguration_groupBox)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.mesh_uniform = QtGui.QRadioButton(self.ObjectMeshConfiguration_groupBox)
        self.mesh_uniform.setChecked(True)
        self.mesh_uniform.setObjectName(_fromUtf8("mesh_uniform"))
        self.verticalLayout_2.addWidget(self.mesh_uniform)
        self.mesh_progressive = QtGui.QRadioButton(self.ObjectMeshConfiguration_groupBox)
        self.mesh_progressive.setEnabled(False)
        self.mesh_progressive.setObjectName(_fromUtf8("mesh_progressive"))
        self.verticalLayout_2.addWidget(self.mesh_progressive)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.ConfigureMesh_pushButton_2 = QtGui.QPushButton(self.ObjectMeshConfiguration_groupBox)
        self.ConfigureMesh_pushButton_2.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ConfigureMesh_pushButton_2.sizePolicy().hasHeightForWidth())
        self.ConfigureMesh_pushButton_2.setSizePolicy(sizePolicy)
        self.ConfigureMesh_pushButton_2.setObjectName(_fromUtf8("ConfigureMesh_pushButton_2"))
        self.verticalLayout_8.addWidget(self.ConfigureMesh_pushButton_2)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.label_2 = QtGui.QLabel(self.ObjectMeshConfiguration_groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_11.addWidget(self.label_2)
        self.mesh_level = QtGui.QLineEdit(self.ObjectMeshConfiguration_groupBox)
        self.mesh_level.setEnabled(False)
        self.mesh_level.setObjectName(_fromUtf8("mesh_level"))
        self.horizontalLayout_11.addWidget(self.mesh_level)
        self.verticalLayout_8.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_3.addLayout(self.verticalLayout_8)
        self.verticalLayout_9.addLayout(self.horizontalLayout_3)
        self.verticalLayout_13.addWidget(self.ObjectMeshConfiguration_groupBox)
        self.horizontalLayout_14.addLayout(self.verticalLayout_13)
        self.FilterConfiguration_groupBox = QtGui.QGroupBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FilterConfiguration_groupBox.sizePolicy().hasHeightForWidth())
        self.FilterConfiguration_groupBox.setSizePolicy(sizePolicy)
        self.FilterConfiguration_groupBox.setObjectName(_fromUtf8("FilterConfiguration_groupBox"))
        self.verticalLayout_12 = QtGui.QVBoxLayout(self.FilterConfiguration_groupBox)
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.flt_list = QtGui.QTreeWidget(self.FilterConfiguration_groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.flt_list.sizePolicy().hasHeightForWidth())
        self.flt_list.setSizePolicy(sizePolicy)
        self.flt_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.flt_list.setAlternatingRowColors(True)
        self.flt_list.setIndentation(20)
        self.flt_list.setRootIsDecorated(False)
        self.flt_list.setUniformRowHeights(True)
        self.flt_list.setItemsExpandable(False)
        self.flt_list.setAllColumnsShowFocus(True)
        self.flt_list.setObjectName(_fromUtf8("flt_list"))
        item_0 = QtGui.QTreeWidgetItem(self.flt_list)
        self.flt_list.header().setDefaultSectionSize(60)
        self.flt_list.header().setStretchLastSection(True)
        self.horizontalLayout_4.addWidget(self.flt_list)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.flt_add = QtGui.QPushButton(self.FilterConfiguration_groupBox)
        self.flt_add.setObjectName(_fromUtf8("flt_add"))
        self.verticalLayout_3.addWidget(self.flt_add)
        self.label = QtGui.QLabel(self.FilterConfiguration_groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.flt_newmat = QtGui.QLineEdit(self.FilterConfiguration_groupBox)
        self.flt_newmat.setObjectName(_fromUtf8("flt_newmat"))
        self.verticalLayout_3.addWidget(self.flt_newmat)
        self.label_3 = QtGui.QLabel(self.FilterConfiguration_groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_3.addWidget(self.label_3)
        self.flt_newthick = QtGui.QLineEdit(self.FilterConfiguration_groupBox)
        self.flt_newthick.setObjectName(_fromUtf8("flt_newthick"))
        self.verticalLayout_3.addWidget(self.flt_newthick)
        self.flt_remove = QtGui.QPushButton(self.FilterConfiguration_groupBox)
        self.flt_remove.setObjectName(_fromUtf8("flt_remove"))
        self.verticalLayout_3.addWidget(self.flt_remove)
        spacerItem3 = QtGui.QSpacerItem(20, 78, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_12.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_14.addWidget(self.FilterConfiguration_groupBox)
        self.verticalLayout_15.addLayout(self.horizontalLayout_14)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.splitter = QtGui.QSplitter(self.layoutWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.Options_groupBox = QtGui.QGroupBox(self.splitter)
        self.Options_groupBox.setObjectName(_fromUtf8("Options_groupBox"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.Options_groupBox)
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.power_power = QtGui.QRadioButton(self.Options_groupBox)
        self.power_power.setObjectName(_fromUtf8("power_power"))
        self.verticalLayout_6.addWidget(self.power_power)
        self.power_density = QtGui.QRadioButton(self.Options_groupBox)
        self.power_density.setChecked(True)
        self.power_density.setObjectName(_fromUtf8("power_density"))
        self.verticalLayout_6.addWidget(self.power_density)
        self.power_both = QtGui.QRadioButton(self.Options_groupBox)
        self.power_both.setObjectName(_fromUtf8("power_both"))
        self.verticalLayout_6.addWidget(self.power_both)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.OutputFileName_label = QtGui.QLabel(self.Options_groupBox)
        self.OutputFileName_label.setObjectName(_fromUtf8("OutputFileName_label"))
        self.horizontalLayout_8.addWidget(self.OutputFileName_label)
        self.title = QtGui.QLineEdit(self.Options_groupBox)
        self.title.setObjectName(_fromUtf8("title"))
        self.horizontalLayout_8.addWidget(self.title)
        self.verticalLayout_6.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_10.addLayout(self.verticalLayout_6)
        self.config_go = QtGui.QPushButton(self.splitter)
        self.config_go.setObjectName(_fromUtf8("config_go"))
        self.config_abort = QtGui.QPushButton(self.splitter)
        self.config_abort.setObjectName(_fromUtf8("config_abort"))
        self.verticalLayout_7.addWidget(self.splitter)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.status_bar = QtGui.QProgressBar(self.layoutWidget)
        self.status_bar.setProperty("value", 0)
        self.status_bar.setTextVisible(False)
        self.status_bar.setInvertedAppearance(False)
        self.status_bar.setObjectName(_fromUtf8("status_bar"))
        self.verticalLayout_5.addWidget(self.status_bar)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        spacerItem4 = QtGui.QSpacerItem(198, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem4)
        self.status_label = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_label.sizePolicy().hasHeightForWidth())
        self.status_label.setSizePolicy(sizePolicy)
        self.status_label.setFrameShape(QtGui.QFrame.StyledPanel)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setObjectName(_fromUtf8("status_label"))
        self.horizontalLayout_9.addWidget(self.status_label)
        spacerItem5 = QtGui.QSpacerItem(218, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem5)
        self.verticalLayout_5.addLayout(self.horizontalLayout_9)
        self.verticalLayout_7.addLayout(self.verticalLayout_5)
        self.verticalLayout_15.addLayout(self.verticalLayout_7)
        #MainWindow.setCentralWidget(self.HeatLoadMatrix_2)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 660, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSpectral_Data = QtGui.QMenu(self.menubar)
        self.menuSpectral_Data.setObjectName(_fromUtf8("menuSpectral_Data"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuRun = QtGui.QMenu(self.menubar)
        self.menuRun.setObjectName(_fromUtf8("menuRun"))
        #MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        #MainWindow.setStatusBar(self.statusbar)
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionSave_Parameters = QtGui.QAction(MainWindow)
        self.actionSave_Parameters.setObjectName(_fromUtf8("actionSave_Parameters"))
        self.actionOpen_Parameters = QtGui.QAction(MainWindow)
        self.actionOpen_Parameters.setObjectName(_fromUtf8("actionOpen_Parameters"))
        self.actionSave_Spectral_Data = QtGui.QAction(MainWindow)
        self.actionSave_Spectral_Data.setObjectName(_fromUtf8("actionSave_Spectral_Data"))
        self.actionSave_Spectral_Data_2 = QtGui.QAction(MainWindow)
        self.actionSave_Spectral_Data_2.setObjectName(_fromUtf8("actionSave_Spectral_Data_2"))
        self.actionImport_Spectral_Data = QtGui.QAction(MainWindow)
        self.actionImport_Spectral_Data.setObjectName(_fromUtf8("actionImport_Spectral_Data"))
        self.actionSave_spectrum = QtGui.QAction(MainWindow)
        self.actionSave_spectrum.setObjectName(_fromUtf8("actionSave_spectrum"))
        self.actionImport_Spectrum = QtGui.QAction(MainWindow)
        self.actionImport_Spectrum.setObjectName(_fromUtf8("actionImport_Spectrum"))
        self.actionHelp = QtGui.QAction(MainWindow)
        self.actionHelp.setObjectName(_fromUtf8("actionHelp"))
        self.actionPaper = QtGui.QAction(MainWindow)
        self.actionPaper.setObjectName(_fromUtf8("actionPaper"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionGo = QtGui.QAction(MainWindow)
        self.actionGo.setObjectName(_fromUtf8("actionGo"))
        self.actionAbort = QtGui.QAction(MainWindow)
        self.actionAbort.setObjectName(_fromUtf8("actionAbort"))
        self.actionView_Results = QtGui.QAction(MainWindow)
        self.actionView_Results.setObjectName(_fromUtf8("actionView_Results"))
        self.actionConfigure_XOP = QtGui.QAction(MainWindow)
        self.actionConfigure_XOP.setObjectName(_fromUtf8("actionConfigure_XOP"))
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Parameters)
        self.menuFile.addAction(self.actionOpen_Parameters)
        self.menuSpectral_Data.addAction(self.actionSave_spectrum)
        self.menuSpectral_Data.addAction(self.actionImport_Spectrum)
        self.menuSpectral_Data.addAction(self.actionConfigure_XOP)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionPaper)
        self.menuHelp.addAction(self.actionAbout)
        self.menuRun.addAction(self.actionGo)
        self.menuRun.addAction(self.actionAbort)
        self.menuRun.addAction(self.actionView_Results)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.menubar.addAction(self.menuSpectral_Data.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.ObjectMaterial_label.setBuddy(self.mat)
        self.DistancetotheSource_label.setBuddy(self.dist)
        self.InclinationtotheBeam_label.setBuddy(self.deg)
        self.label.setBuddy(self.flt_newmat)
        self.label_3.setBuddy(self.flt_newthick)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.source_und, self.source_wig)
        MainWindow.setTabOrder(self.source_wig, self.source_bend)
        MainWindow.setTabOrder(self.source_bend, self.config_source)
        MainWindow.setTabOrder(self.config_source, self.mat)
        MainWindow.setTabOrder(self.mat, self.dist)
        MainWindow.setTabOrder(self.dist, self.deg)
        MainWindow.setTabOrder(self.deg, self.config_region)
        MainWindow.setTabOrder(self.config_region, self.mesh_uniform)
        MainWindow.setTabOrder(self.mesh_uniform, self.mesh_progressive)
        MainWindow.setTabOrder(self.mesh_progressive, self.ConfigureMesh_pushButton_2)
        MainWindow.setTabOrder(self.ConfigureMesh_pushButton_2, self.mesh_level)
        MainWindow.setTabOrder(self.mesh_level, self.power_power)
        MainWindow.setTabOrder(self.power_power, self.power_density)
        MainWindow.setTabOrder(self.power_density, self.power_both)
        MainWindow.setTabOrder(self.power_both, self.imported_source)
        MainWindow.setTabOrder(self.imported_source, self.flt_list)
        MainWindow.setTabOrder(self.flt_list, self.flt_add)
        MainWindow.setTabOrder(self.flt_add, self.flt_remove)
        MainWindow.setTabOrder(self.flt_remove, self.config_go)
        MainWindow.setTabOrder(self.config_go, self.config_abort)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Heat Load Matrix 3.0", None, QtGui.QApplication.UnicodeUTF8))
        self.SourceConfiguration_groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Source Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.source_und.setText(QtGui.QApplication.translate("MainWindow", "Undulator", None, QtGui.QApplication.UnicodeUTF8))
        self.source_wig.setText(QtGui.QApplication.translate("MainWindow", "Wiggler", None, QtGui.QApplication.UnicodeUTF8))
        self.source_bend.setText(QtGui.QApplication.translate("MainWindow", "Bend Magnet", None, QtGui.QApplication.UnicodeUTF8))
        self.config_source.setText(QtGui.QApplication.translate("MainWindow", "Configure Source", None, QtGui.QApplication.UnicodeUTF8))
        self.SelectedSource_Label.setText(QtGui.QApplication.translate("MainWindow", "Selected Source:", None, QtGui.QApplication.UnicodeUTF8))
        self.imported_source.setText(QtGui.QApplication.translate("MainWindow", "No Source Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.ObjectConfiguration_groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Object Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.ObjectMaterial_label.setText(QtGui.QApplication.translate("MainWindow", "Material:", None, QtGui.QApplication.UnicodeUTF8))
        self.DistancetotheSource_label.setText(QtGui.QApplication.translate("MainWindow", "Distance to the Source (m):", None, QtGui.QApplication.UnicodeUTF8))
        self.InclinationtotheBeam_label.setText(QtGui.QApplication.translate("MainWindow", "Inclination to the Beam (deg):", None, QtGui.QApplication.UnicodeUTF8))
        self.config_region.setText(QtGui.QApplication.translate("MainWindow", "Configure Region", None, QtGui.QApplication.UnicodeUTF8))
        self.ObjectMeshConfiguration_groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Object Mesh Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.mesh_uniform.setText(QtGui.QApplication.translate("MainWindow", "Uniform Meshing", None, QtGui.QApplication.UnicodeUTF8))
        self.mesh_progressive.setText(QtGui.QApplication.translate("MainWindow", "Progressive Meshing", None, QtGui.QApplication.UnicodeUTF8))
        self.ConfigureMesh_pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Configure Mesh", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Mesh Levels", None, QtGui.QApplication.UnicodeUTF8))
        self.FilterConfiguration_groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Filter Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.flt_list.setSortingEnabled(True)
        self.flt_list.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Material", None, QtGui.QApplication.UnicodeUTF8))
        self.flt_list.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Thickness (µm)", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.flt_list.isSortingEnabled()
        self.flt_list.setSortingEnabled(False)
        self.flt_list.setSortingEnabled(__sortingEnabled)
        self.flt_add.setText(QtGui.QApplication.translate("MainWindow", "Add New Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Material", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Thickness", None, QtGui.QApplication.UnicodeUTF8))
        self.flt_remove.setText(QtGui.QApplication.translate("MainWindow", "Remove Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.Options_groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Output Options", None, QtGui.QApplication.UnicodeUTF8))
        self.power_power.setText(QtGui.QApplication.translate("MainWindow", "Power (W)", None, QtGui.QApplication.UnicodeUTF8))
        self.power_density.setText(QtGui.QApplication.translate("MainWindow", "Power Density (W/m^3)", None, QtGui.QApplication.UnicodeUTF8))
        self.power_both.setText(QtGui.QApplication.translate("MainWindow", "Both", None, QtGui.QApplication.UnicodeUTF8))
        self.OutputFileName_label.setText(QtGui.QApplication.translate("MainWindow", "Output File Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.config_go.setText(QtGui.QApplication.translate("MainWindow", "Go", None, QtGui.QApplication.UnicodeUTF8))
        self.config_abort.setText(QtGui.QApplication.translate("MainWindow", "Abort", None, QtGui.QApplication.UnicodeUTF8))
        self.status_label.setText(QtGui.QApplication.translate("MainWindow", "Ready to Start", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSpectral_Data.setTitle(QtGui.QApplication.translate("MainWindow", "Spectral Data", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuRun.setTitle(QtGui.QApplication.translate("MainWindow", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Parameters.setText(QtGui.QApplication.translate("MainWindow", "Save Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Parameters.setText(QtGui.QApplication.translate("MainWindow", "Open Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Spectral_Data.setText(QtGui.QApplication.translate("MainWindow", "Save Spectral Data", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Spectral_Data_2.setText(QtGui.QApplication.translate("MainWindow", "Save Spectral Data", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_Spectral_Data.setText(QtGui.QApplication.translate("MainWindow", "Import Spectral Data", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_spectrum.setText(QtGui.QApplication.translate("MainWindow", "Save Spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_Spectrum.setText(QtGui.QApplication.translate("MainWindow", "Import Spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setText(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaper.setText(QtGui.QApplication.translate("MainWindow", "Paper", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGo.setText(QtGui.QApplication.translate("MainWindow", "Go", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbort.setText(QtGui.QApplication.translate("MainWindow", "Abort", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_Results.setText(QtGui.QApplication.translate("MainWindow", "View Results", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfigure_XOP.setText(QtGui.QApplication.translate("MainWindow", "Configure XOP", None, QtGui.QApplication.UnicodeUTF8))

