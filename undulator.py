#import basic and PyQt modules
from PyQt4 import QtGui, QtCore
import _pickle as pickle
import sys

#undulator layout
from ui.undulator_ui import Ui_Dialog
import advancedoptions

class UDialog(QtGui.QDialog):
    """Undulator functionailty"""
    def __init__(self):
        #GUI Setup
        super(UDialog,self).__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        #may be phased out by self.load_values
        self.und_load_values()
        #Button Box connections (OK/Cancel)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.und_pickle)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QObject.connect(self.ui.advanced_button, QtCore.SIGNAL("clicked()"), self.adv_new_window)
        QtCore.QObject.connect(self.ui.default_button, QtCore.SIGNAL("clicked()"), self.und_load_values)
        
    def adv_new_window(self):
        """Pops up Advanced Options"""
        adv=workflow.advancedoptions_w.ADialog()
        adv.exec_()
        
    def und_pickle(self):
        """write undulator parameters into .pkl for storage"""
        
        und=pickle.load(open("pickle\\und.pkl","rb"))
        und["energy"]=self.ui.und_energy.text()
        und["current"]=self.ui.und_current.text()
        und["period"]=self.ui.und_period.text()
        und["num"]=self.ui.und_nperiods.text()
        und["sigx"]=self.ui.und_sigx.text()
        und["sigy"]=self.ui.und_sigy.text()
        und["sigx1"]=self.ui.und_sigx1.text()
        und["sigy1"]=self.ui.und_sigy1.text()
        und["kx"]=self.ui.und_kx.text()
        und["ky"]=self.ui.und_ky.text()
        
        pickle.dump(und,open("pickle\\und.pkl","wb"))
        self.reject()
        
    def und_load_values(self):
        """Loads default values from file, need to implement recalling numbers from last run"""
        f=open("pickle\\und.pkl","rb")
        und=pickle.load(f)
        f.close()
        
        self.ui.und_energy.setText(und["energy"])
        self.ui.und_current.setText(und["current"])
        self.ui.und_kx.setText(und["kx"])
        self.ui.und_ky.setText(und["ky"])
        self.ui.und_nperiods.setText(und["num"])
        self.ui.und_period.setText(und["period"])
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