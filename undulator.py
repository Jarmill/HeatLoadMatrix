#import basic and PyQt modules
from PyQt4 import QtGui, QtCore
import advancedoptions
import _pickle as pickle
import sys

#undulator layout
from ui.undulator_ui import Ui_Dialog

#back-end functionality
import backend

class UDialog(QtGui.QDialog, backend.Back):
    """Undulator functionailty"""
    def __init__(self):
        #GUI Setup
        super(UDialog,self).__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        #may be phased out by self.load_values
        self.default_values()
        #Button Box connections (OK/Cancel)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.heat_load_matrix)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QObject.connect(self.ui.advanced_button, QtCore.SIGNAL("clicked()"), self.adv_new_window)
        QtCore.QObject.connect(self.ui.default_button, QtCore.SIGNAL("clicked()"), self.default_values)
        
        #set "global" values
        self.back_values("und")
        
    def adv_new_window(self):
        """Pops up Advanced Options"""
        adv=advancedoptions.ADialog()
        adv.exec_()
    
    def default_values(self):
        """Loads default values from file, need to implement recalling numbers from last run"""
        f=open("pickle\\und_default.pkl","rb")
        und=pickle.load(f)
        f.close()
        
        self.ui.und_energy.setText(und["energy"])
        self.ui.und_current.setText(und["current"])
        self.ui.und_kx.setText(und["kx"])
        self.ui.und_ky.setText(und["ky"])
        self.ui.und_nperiods.setText(und["num"])
        self.ui.und_period.setText(und["period"])
        self.ui.und_title.setText(und["title"])
        self.ui.und_sigx.setText(und["sigx"])
        self.ui.und_sigx1.setText(und["sigx1"])
        self.ui.und_sigy.setText(und["sigy"])
        self.ui.und_sigy1.setText(und["sigy1"])

def main():
    """Runs undulator without heatbump"""
    app=QtGui.QApplication(sys.argv)
    ud=UDialog()
    ud.exec_()
    sys.exit(app.exec_())

if __name__=="__main__":
    #runs only when directly called
    main()