"""
This program wraps together the various functions of the heatbump program.
Abbreviations used:
abt-about
adv-advancedoptions
flt-filters
reg-region
und-undulator
wig-wiggler
"""
#import basic and PyQt modules
import sys
from PyQt4 import QtGui, QtCore

#GUI heatbump layout
from heatbump_ui import Ui_MainWindow

#import other functions of heatbump.
import about
import filters
import region_old
import undulator_old
import wiggler_old

class HMainWindow(QtGui.QWidget):
    def __init__(self):
        super(HMainWindow,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        #connecting buttons to windows
        
        self.connect(self.ui.aboutButton,QtCore.SIGNAL("clicked()"),self.abt_new_window)
        self.connect(self.ui.filterButton,QtCore.SIGNAL("clicked()"),self.flt_new_window)
        self.connect(self.ui.regionButton,QtCore.SIGNAL("clicked()"),self.reg_new_window)
        self.connect(self.ui.undButton,QtCore.SIGNAL("clicked()"),self.und_new_window)
        self.connect(self.ui.wigButton,QtCore.SIGNAL("clicked()"),self.wig_new_window)
        
        self.show()
        
    def abt_new_window(self):
        abt=about.AbDialog()
        abt.exec_()
        
    def flt_new_window(self):
        flt=filters.FDialog()
        flt.exec_()
    

    def reg_new_window(self):
        reg=region_old.RDialog()
        reg.exec_()
    
    def und_new_window(self):
        und=undulator_old.UDialog()
        und.exec_()
        
    def wig_new_window(self):
        wig=wiggler_old.WDialog()
        wig.exec_()

def main():
    app=QtGui.QApplication(sys.argv)
    hd=HMainWindow()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()