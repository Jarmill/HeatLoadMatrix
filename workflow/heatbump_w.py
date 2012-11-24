"""
This program wraps together the various functions of the heatbump program.
Abbreviations used:
abt-about
adv-advancedoptions
flt-filters
reg-region
und-undulator
wig-wiggler

ws is always faster than us, though processing is the same
this is the workflow variant of the ui
"""
#import basic and PyQt modules
import sys
from PyQt4 import QtGui, QtCore

#other functions
import _pickle as pickle
from math import pi
#heatbump layout
from ui.heatbump_w_ui import Ui_MainWindow

#import other functions of heatbump.
import workflow.region_w as region
import workflow.undulator_w as undulator
import workflow.wiggler_w as wiggler
import workflow.backend_w as backend

class HMainWindow(QtGui.QWidget, backend.Back):
    def __init__(self):
        super(HMainWindow,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Heat Load Matrix 3.0")
        self.main_load_values()
        #back_values?
        #connecting buttons to open up other windows
        
        self.connect(self.ui.config_source,QtCore.SIGNAL("clicked()"),self.source_set)
        self.connect(self.ui.config_region,QtCore.SIGNAL("clicked()"),self.region_set)
        self.connect(self.ui.config_go,QtCore.SIGNAL("clicked()"),self.run_begin)
        self.connect(self.ui.config_abort,QtCore.SIGNAL("clicked()"),self.guipass)
    
    def guipass(self):
        pass
    
    def region_set(self):
        reg=region.RDialog()
        reg.exec_()
    
    def source_set(self):
        if self.ui.source_und.isChecked():
            und=undulator.UDialog()
            und.exec_()
        elif self.ui.source_wig.isChecked():
            wig=wiggler.WDialog()
            wig.exec_()

    def run_begin(self):
        run=pickle.load(open("..\\pickle\\run.pkl","rb"))
        #source
        if self.ui.source_und.isChecked(): run["source"]="und"
        elif self.ui.source_wig.isChecked(): run["source"]="wig"
        
        #object
        run["mat"]=self.ui.mat.text()
        run["dist"]=float(self.ui.dist.text())
        if self.ui.deg.text()=="": run["deg"]=pi/2
        else: run["deg"]=float(self.ui.deg.text())
        
        #mesh
        if self.ui.mesh_progressive.isChecked(): run["mesh"]=int(self.ui.mesh_level.text())
        else: run["mesh"]=0
        
        run["title"]=self.ui.title.text()
        
        #power
        if self.ui.power_power.isChecked():     run["power"]="power"
        elif self.ui.power_density.isChecked():   run["power"]="density"
        elif self.ui.power_both.isChecked():   run["power"]="both"
        else:   run["power"]="density"
        
        pickle.dump(run,open("..\\pickle\\run.pkl","wb"))
        
        self.back_values()
        self.heat_load_matrix()
        
    def main_load_values(self):
        run=pickle.load(open("..\\pickle\\run.pkl","rb"))
        
        #source
        if run["source"]=="und": self.ui.source_und.setChecked(True)
        else: self.ui.source_wig.setChecked(True)
        
        self.ui.mat.setText(run["mat"])
        self.ui.dist.setText(str(run["dist"]))
        self.ui.deg.setText(str(run["deg"]))
        
        #mesh
        if run["mesh"]==0: self.ui.mesh_uniform.setChecked(True)
        else: 
            self.ui.mesh_progressive.setChecked()
            self.ui.mesh_level.setText(str(run["mesh"]))
        
        #power output
        if run["power"]=="power": self.ui.power_power.setChecked(True)
        elif run["power"]=="both": self.ui.power_both.setChecked(True)
        else: self.ui.power_density.setChecked(True)
        
def main():
    app=QtGui.QApplication(sys.argv)
    hd=HMainWindow()
    hd.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()