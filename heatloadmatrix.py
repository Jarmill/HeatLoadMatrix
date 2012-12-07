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
import json
from math import pi
#heatbump layout
from ui.heatloadmatrix_ui import Ui_MainWindow

#import other functions of heatbump.
import region
import undulator
import wiggler
import backend
import xop_config

class HMainWindow(QtGui.QWidget, backend.Back):
    def __init__(self):
        super(HMainWindow,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.flt_load()
        self.main_load_values()
        
        #gui linkage
        self.connect(self.ui.config_source,QtCore.SIGNAL("clicked()"),self.source_set)
        self.connect(self.ui.config_region,QtCore.SIGNAL("clicked()"),self.region_set)
        self.connect(self.ui.config_go,QtCore.SIGNAL("clicked()"),self.run_begin)
        self.connect(self.ui.config_abort,QtCore.SIGNAL("clicked()"),self.guipass)
        self.connect(self.ui.flt_remove,QtCore.SIGNAL("clicked()"),self.flt_del)
        self.connect(self.ui.flt_add,QtCore.SIGNAL("clicked()"),self.flt_add)
        
        #menu linkage
        self.connect(self.ui.action_go, QtCore.SIGNAL("triggered()"), self.run_begin)
        self.connect(self.ui.action_abort, QtCore.SIGNAL("triggered()"), self.guipass)
        self.connect(self.ui.action_view_results, QtCore.SIGNAL("triggered()"), self.guipass)
        self.connect(self.ui.action_param_save, QtCore.SIGNAL("triggered()"), self.guipass)
        self.connect(self.ui.action_param_open, QtCore.SIGNAL("triggered()"), self.guipass)
        self.connect(self.ui.action_xop_config, QtCore.SIGNAL("triggered()"), self.xop_set)
        self.connect(self.ui.action_help, QtCore.SIGNAL("triggered()"), self.guipass)
        self.connect(self.ui.action_paper, QtCore.SIGNAL("triggered()"), self.guipass)
        self.connect(self.ui.action_about, QtCore.SIGNAL("triggered()"), self.guipass)

    def guipass(self):
        pass
    
    def flt_save(self):
        """save qtreewidget data"""
        flt=[]
        root=self.ui.flt_list.invisibleRootItem()
        child_count=root.childCount()
        for i in range(0,child_count):
            item=root.child(i)
            mat=item.text(0)
            thick=float(item.text(1))
            flt.append([mat,thick])
        with open("pickle\\flt.json","w") as f:
            json.dump(flt, f, indent=2)
            
    def flt_load(self):
        """load values in flt.json into the filter qtreewidget"""
        flt=json.load(open("pickle\\flt.json","r"))
        
        for i in flt:
            if (i[0]and i[1])!=("" or None):
                item=QtGui.QTreeWidgetItem([i[0], str(i[1])])
                self.ui.flt_list.addTopLevelItem(item)
    
    def flt_add(self):
        """adds widget to filter list"""
        mat=self.ui.flt_newmat.text()
        thick=self.ui.flt_newthick.text()
        if (mat and thick)!=("" or None):
            item=QtGui.QTreeWidgetItem([mat, thick])
            self.ui.flt_list.addTopLevelItem(item)
        self.flt_save()
                
    def flt_del(self):
        """deletes selected value from filter list"""
        item=self.ui.flt_list.currentItem()
        if not item: return #None selected, do nothing
        
        #Finally delete the task
        self.ui.flt_list.takeTopLevelItem(self.ui.flt_list.indexOfTopLevelItem(item))
        self.flt_save()
        
    def region_set(self):
        reg=region.RDialog()
        reg.exec_()
    
    def xop_set(self):
        xop=xop_config.XDialog()
        xop.exec_()
    
    def source_set(self):
        if self.ui.source_und.isChecked():
            und=undulator.UDialog()
            und.exec_()
        elif self.ui.source_wig.isChecked():
            wig=wiggler.WDialog()
            wig.exec_()

    def run_begin(self):
        run=json.load(open("pickle\\run.json","r"))
        #run={}
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
        
        json.dump(run,open("pickle\\run.json","w"), indent=2)
        
        self.back_values()
        self.heat_load_matrix()
        
    def main_load_values(self):
        run=json.load(open("pickle\\run.json","r"))
        
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