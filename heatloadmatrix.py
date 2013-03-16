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
from os import path, makedirs, getcwd
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
import backend_worker as backend
import xop_config

class HMainWindow(QtGui.QWidget):
    def __init__(self):
        super(HMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.flt_load()
        self.main_load_values()
        self.changed = False
        self.ui.config_abort.setEnabled(False)
        self.ui.action_abort.setEnabled(False)
        self.ui.config_go.setEnabled(True)
        self.LastValue = -1

        #gui linkage
        self.connect(self.ui.config_source, QtCore.SIGNAL("clicked()"), self.source_set)
        self.connect(self.ui.config_region, QtCore.SIGNAL("clicked()"), self.region_set)
        self.connect(self.ui.config_go, QtCore.SIGNAL("clicked()"), self.run_begin)
        self.connect(self.ui.config_abort, QtCore.SIGNAL("clicked()"), self.trigger_abort)
        self.connect(self.ui.flt_remove, QtCore.SIGNAL("clicked()"), self.flt_del)
        self.connect(self.ui.flt_add, QtCore.SIGNAL("clicked()"), self.flt_add)

        #menu linkage
        self.connect(self.ui.action_go, QtCore.SIGNAL("triggered()"), self.run_begin)
        self.connect(self.ui.action_abort, QtCore.SIGNAL("triggered()"), self.trigger_abort)
        self.connect(self.ui.action_view_results, QtCore.SIGNAL("triggered()"), self.guipass)
        self.connect(self.ui.action_param_save, QtCore.SIGNAL("triggered()"), self.param_save)
        self.connect(self.ui.action_param_open, QtCore.SIGNAL("triggered()"), self.param_open)
        self.connect(self.ui.action_xop_config, QtCore.SIGNAL("triggered()"), self.xop_set)
        self.connect(self.ui.action_help, QtCore.SIGNAL("triggered()"), self.guipass)
        self.connect(self.ui.action_paper, QtCore.SIGNAL("triggered()"), self.guipass)
        self.connect(self.ui.action_about, QtCore.SIGNAL("triggered()"), self.guipass)

        #current working directory, used to initialize files
        #self.cwd=s="\\".join(getcwd().split("\\")[:-1])+"\\"
        self.cwd = getcwd() + "\\"

    def guipass(self):
        pass

    def trigger_abort(self):
        self.workthread.abort = True
        print("Quit pressed")

    def param_save(self):
        """Save source data"""
        dirroot = ".\\source_parameters"
        if not path.exists(dirroot):
            makedirs(dirroot)
        fdia = QtGui.QFileDialog()
        fdia.setDirectory(self.cwd + "source_parameters")
        filename = str(fdia.getSaveFileName(self, "Save File", "", "JSON Data (*.json)"))

        #print(filename)
        if filename == "": return

        basename = path.basename(filename).split(".")[0]
        self.ui.imported_source.setText(basename)

        #name=self.ui.imported_source.text()
        #s=json.load(open("pickle\\run.json","r"))["source"]
        #s=json.load(open("pickle\\run.json"),"r")["source"]

        if self.ui.source_wig.isChecked():
            source = json.load(open("pickle\\wig.json", "r"))
            s = "wig"
        else:
            source = json.load(open("pickle\\und.json", "r"))
            s = "und"

        source["source"] = s
        f = open(filename, "w")
        json.dump(source, f, indent=2)
        f.close()
        self.changed = False

    def param_open(self):
        """Open source data"""
        dirroot = ".\\source_parameters"
        if not path.exists(dirroot):
            makedirs(dirroot)
        fdia = QtGui.QFileDialog()
        fdia.setDirectory(self.cwd + "source_parameters")
        filename = str(fdia.getOpenFileName(self, "Open File", "", "JavaScript Object Notation (*.json)"))
        self.param_load(filename)

    def param_load(self, filename):
        """load values from file"""
        if filename == "": return
        
        f = json.load(open("pickle\\run.json", "r"))
        f["filename"] = filename
        json.dump(f, open("pickle\\run.json", "w"), indent=2)

        source = json.load(open(filename, "r"))

        #change back to wig and und, wig2/und2 for testing only
        if source["source"] == "wig":
            del source["source"]
            json.dump(source, open("pickle\\wig.json", "w"), indent=2)
            json.dump(source, open("pickle\\wigload.json", "w"), indent=2)
            self.ui.source_wig.setChecked(True)
        elif source["source"] == "und":
            del source["source"]
            json.dump(source, open("pickle\\und.json", "w"), indent=2)
            json.dump(source, open("pickle\\undload.json", "w"), indent=2)
            self.ui.source_und.setChecked(True)

        #find the file name without extensions
        self.changed = False
        basename = path.basename(filename).split(".")[0]
        self.ui.imported_source.setText(basename)
        
    def flt_save(self):
        """save qtreewidget data"""
        flt = []
        root = self.ui.flt_list.invisibleRootItem()
        child_count = root.childCount()
        for i in range(0, child_count):
            item = root.child(i)
            if (item.text(0) and item.text(1)) != "":
                mat = item.text(0)
                thick = float(item.text(1))
                flt.append([mat, thick])
        with open("pickle\\flt.json", "w") as f:
            json.dump(flt, f, indent=2)

    def flt_load(self):
        """load values in flt.json into the filter qtreewidget"""
        flt = json.load(open("pickle\\flt.json", "r"))
        for i in flt:
            if (i[0]and i[1]) != ("" or None):
                item = QtGui.QTreeWidgetItem([i[0], str(i[1])])
                self.ui.flt_list.addTopLevelItem(item)

    def flt_add(self):
        """adds widget to filter list"""
        mat = self.ui.flt_newmat.text()
        thick = self.ui.flt_newthick.text()
        if (mat and thick) != ("" or None):
            item = QtGui.QTreeWidgetItem([mat, thick])
            self.ui.flt_list.addTopLevelItem(item)
        self.flt_save()

    def flt_del(self):
        """deletes selected value from filter list"""
        item = self.ui.flt_list.currentItem()
        if not item: return #None selected, do nothing

        #Finally delete the task
        self.ui.flt_list.takeTopLevelItem(self.ui.flt_list.indexOfTopLevelItem(item))
        self.flt_save()

    def region_set(self):
        reg = region.RDialog()
        reg.exec_()

    def xop_set(self):
        xop = xop_config.XDialog()
        xop.exec_()

    def source_set(self):
        """Opens wiggler/undulator dialog box, and marks that the file is unsaved"""
        if self.ui.source_und.isChecked():
            prev = json.load(open("pickle\\undload.json", "r"))
            und = undulator.UDialog()
            und.exec_()
            curr = json.load(open("pickle\\und.json", "r"))
            changed = (prev != curr)
        elif self.ui.source_wig.isChecked():
            prev = json.load(open("pickle\\wigload.json", "r"))
            wig = wiggler.WDialog()
            wig.exec_()
            curr = json.load(open("pickle\\wig.json", "r"))
            changed = (prev != curr)
        if changed and not self.changed:
            self.ui.imported_source.setText("(unsaved) " + self.ui.imported_source.text())
            self.changed = True
        if not changed and self.changed:
            self.changed = False
            self.ui.imported_source.setText(self.ui.imported_source.text()[10:])

    def run_begin(self):
        run = json.load(open("pickle\\run.json", "r"))
        #run={}
        #source
        if self.ui.source_und.isChecked(): run["source"] = "und"
        elif self.ui.source_wig.isChecked(): run["source"] = "wig"

        #object
        run["mat"] = self.ui.mat.text()
        run["dist"] = float(self.ui.dist.text())
        if self.ui.deg.text() == "": run["deg"] = 90
        else: run["deg"] = float(self.ui.deg.text())
        
        #mesh
        if self.ui.mesh_progressive.isChecked(): run["mesh"] = int(self.ui.mesh_level.text())
        else: run["mesh"] = 0
        
        run["title"] = self.ui.title.text()
        
        #power
        if self.ui.power_power.isChecked():     run["power"] = "power"
        elif self.ui.power_density.isChecked():   run["power"] = "density"
        elif self.ui.power_both.isChecked():   run["power"] = "both"
        else:   run["power"] = "density"

        json.dump(run, open("pickle\\run.json", "w"), indent=2)
        self.workthread = backend.Back()
        #self.connect(self.workthread, QtCore.SIGNAL("testsignal"), self.proglabbeltest)
        self.connect(self.workthread, QtCore.SIGNAL("update(QString)"), self.proglabel)
        self.connect(self.workthread, QtCore.SIGNAL("progvalue"), self.progvalue)
        self.connect(self.workthread, QtCore.SIGNAL("endofrun"), self.endofrun)
        self.connect(self.workthread, QtCore.SIGNAL("startofrun"), self.startofrun)

        self.ui.status_bar.setMinimum(0)
        self.ui.status_bar.setMaximum(100)
        self.ui.status_bar.setValue(0)

        self.workthread.run_heat_load_matrix()

    def proglabel(self, text):
        if text != self.ui.status_label.text():
            print(text)
            self.ui.status_label.setText(text)

    def progvalue(self, val):
        if val != self.LastValue:
            self.LastValue = val
            print(str(round(val, 2)) + "% done")
            self.ui.status_bar.setValue(val)

    ##enabledObjects = []

    def startofrun(self):
        self.ui.config_abort.setEnabled(True)
        self.ui.action_abort.setEnabled(True)
        self.ui.config_go.setEnabled(False)
        self.ui.action_go.setEnabled(False)
        self.ui.status_bar.setTextVisible(True)


    def endofrun(self):
        self.ui.config_abort.setEnabled(False)
        self.ui.action_abort.setEnabled(False)
        self.ui.config_go.setEnabled(True)
        self.ui.action_go.setEnabled(True)
        self.ui.status_bar.setTextVisible(False)


    def main_load_values(self):
        run = json.load(open("pickle\\run.json", "r"))

        #source
        if run["source"] == "und": self.ui.source_und.setChecked(True)
        else: self.ui.source_wig.setChecked(True)
        
        if "filename" in run:
            filename = run["filename"]
        else: filename = ""

        if filename != "":
            self.param_load(filename)
        
        self.ui.mat.setText(run["mat"])
        self.ui.dist.setText(str(run["dist"]))
        self.ui.deg.setText(str(run["deg"]))

        #mesh
        if run["mesh"] == 0: self.ui.mesh_uniform.setChecked(True)
        else:
            self.ui.mesh_progressive.setChecked()
            self.ui.mesh_level.setText(str(run["mesh"]))

        #power output
        if run["power"] == "power": self.ui.power_power.setChecked(True)
        elif run["power"] == "both": self.ui.power_both.setChecked(True)
        else: self.ui.power_density.setChecked(True)

        #set values of change files
        json.dump(json.load(open("pickle\\und.json", "r")), open("pickle\\undload.json", "w"), indent=2)
        json.dump(json.load(open("pickle\\wig.json", "r")), open("pickle\\wigload.json", "w"), indent=2)

def main():
    app = QtGui.QApplication(sys.argv)
    hd = HMainWindow()
    hd.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
