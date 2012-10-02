"""
This program wraps together the various functions of the heatbump program.
Abbreviations used:
abt-about
adv-advancedoptions
flt-filters
reg-region
und-undulator
wig-wiggler

all wig functions run faster than und functions (3.11s vs. 145.08s, now .15s vs. 6.67s average time)
"""
#import basic and PyQt modules
import sys
from PyQt4 import QtGui, QtCore

#heatbump layout
from ui.heatbump_ui import Ui_MainWindow

#import other functions of heatbump.
import about
import filters
import region
import undulator
import wiggler

class HMainWindow(QtGui.QWidget):
    def __init__(self):
        super(HMainWindow,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        #connecting buttons to open up other windows
        
        self.connect(self.ui.aboutButton,QtCore.SIGNAL("clicked()"),self.abt_new_window)
        self.connect(self.ui.filterButton,QtCore.SIGNAL("clicked()"),self.flt_new_window)
        self.connect(self.ui.regionButton,QtCore.SIGNAL("clicked()"),self.reg_new_window)
        self.connect(self.ui.undButton,QtCore.SIGNAL("clicked()"),self.und_new_window)
        self.connect(self.ui.wigButton,QtCore.SIGNAL("clicked()"),self.wig_new_window)
        
    def abt_new_window(self):
        abt=about.AbDialog()
        abt.exec_()
        
    def flt_new_window(self):
        flt=filters.FDialog()
        flt.exec_()
    
    def reg_new_window(self):
        reg=region.RDialog()
        reg.exec_()
    
    def und_new_window(self):
        und=undulator.UDialog()
        und.exec_()
        
    def wig_new_window(self):
        wig=wiggler.WDialog()
        wig.exec_()

def main():
    app=QtGui.QApplication(sys.argv)
    hd=HMainWindow()
    hd.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()