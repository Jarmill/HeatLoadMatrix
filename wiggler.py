#import basic and PyQt modules
from PyQt4 import QtGui, QtCore
import _pickle as pickle
import sys

#wiggler layout
from ui.wiggler_ui import Ui_Dialog

#import back-end functionailty. rectangle_grid is included.
import backend as backend

import advancedoptions

class WDialog(QtGui.QDialog,backend.Back):
    """Wiggler Functionailty"""
    def __init__(self):
        #set up GUI
        super(WDialog,self).__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        #may be phased out by self.load_values
        self.default_values()
        #set "global" values
        self.back_values("wig")
        #Button Box connections (OK/Cancel)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.heat_load_matrix)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QObject.connect(self.ui.advanced_button,QtCore.SIGNAL("clicked()"),self.adv_new_window)
        QtCore.QObject.connect(self.ui.default_button,QtCore.SIGNAL("clicked()"),self.default_values)

        #set "global" values, hopefully dodge diamond of death
        
    def adv_new_window(self):
        """Pops up Advanced Options"""
        adv=advancedoptions.ADialog()
        adv.exec_()
    
    def default_values(self):
        """Loads default values from file, need to implement recalling numbers from last run"""
        f=open("pickle\\wig_default.pkl","rb")
        wig=pickle.load(f)
        f.close()
        
        self.ui.wig_energy.setText(wig["energy"])
        self.ui.wig_current.setText(wig["current"])
        self.ui.wig_kx.setText(wig["kx"])
        self.ui.wig_ky.setText(wig["ky"])
        self.ui.wig_nperiods.setText(wig["num"])
        self.ui.wig_periods.setText(wig["period"])
        self.ui.wig_title.setText(wig["title"])

def main():
    """Runs wiggler without heatbump"""
    app=QtGui.QApplication(sys.argv)
    wd=WDialog()
    wd.exec_()
    sys.exit(app.exec_())

if __name__=="__main__":
    #runs only when directly called
    main()