#import basic and PyQt modules
from PyQt4 import QtGui, QtCore
import _pickle as pickle
import sys

#wiggler layout
from ui.wiggler_w_ui import Ui_Wiggler

import workflow.advancedoptions_w

class WDialog(QtGui.QDialog):
    """Wiggler Functionailty"""
    def __init__(self):
        #set up GUI
        super(WDialog,self).__init__()
        self.ui=Ui_Wiggler()
        self.ui.setupUi(self)
        #may be phased out by self.load_values
        self.wig_load_values()
        #set "global" values
        #self.back_values("wig")
        #Button Box connections (OK/Cancel)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.wig_pickle)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QObject.connect(self.ui.advanced_button,QtCore.SIGNAL("clicked()"),self.adv_new_window)
        QtCore.QObject.connect(self.ui.default_button,QtCore.SIGNAL("clicked()"),self.wig_load_values)

        #set "global" values, hopefully dodge diamond of death
        
    def adv_new_window(self):
        """Pops up Advanced Options"""
        adv=workflow.advancedoptions_w.ADialog()
        adv.exec_()
        
    def wig_pickle(self):
        """write wiggler parameters into .pkl for storage"""
        #wig=pickle.load(open("..\\pickle\\wig.pkl","rb"))
        #ignore the title coming from wig, it is relevant to the old model
        wig={}
        wig["energy"]=self.ui.wig_energy.text()
        wig["current"]=self.ui.wig_current.text()
        wig["period"]=self.ui.wig_periods.text()
        wig["num"]=self.ui.wig_nperiods.text()
        wig["kx"]=self.ui.wig_kx.text()
        wig["ky"]=self.ui.wig_ky.text()
        pickle.dump(wig,open("..\\pickle\\wig.pkl","wb"))
        self.reject()
        
    def wig_load_values(self):
        """Loads default values from file, need to implement recalling numbers from last run"""
        f=open("..\\pickle\\wig.pkl","rb")
        wig=pickle.load(f)
        f.close()
        
        self.ui.wig_energy.setText(wig["energy"])
        self.ui.wig_current.setText(wig["current"])
        self.ui.wig_kx.setText(wig["kx"])
        self.ui.wig_ky.setText(wig["ky"])
        self.ui.wig_nperiods.setText(wig["num"])
        self.ui.wig_periods.setText(wig["period"])

def main():
    """Runs wiggler without heatbump"""
    app=QtGui.QApplication(sys.argv)
    wd=WDialog()
    wd.exec_()
    sys.exit(app.exec_())

if __name__=="__main__":
    #runs only when directly called
    main()