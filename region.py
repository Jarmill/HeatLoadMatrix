#import basic and PyQt modules
from PyQt4 import QtGui, QtCore
import _pickle as pickle
import sys

#region layout
from ui.region_ui import Ui_Dialog

class RDialog(QtGui.QDialog):
    def __init__(self):
        """Region constructor"""
        super(RDialog,self).__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        #Button Box connections (OK/Cancel)
        self.regloadvalues()
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.regpickle)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        
    def regpickle(self):
        """Reads the value of the region data, and serializes it into a file"""
        xlen=self.ui.reg_xlength.text()
        ylen=self.ui.reg_ylength.text()
        xdiv=self.ui.reg_xdivisions.text()
        ydiv=self.ui.reg_ydivisions.text()
        mat=self.ui.reg_material.text()
        dist=self.ui.reg_distance.text()
        thickness=self.ui.reg_thickness.text()
        thickness2=[.1* float(i) for i in thickness.split()] #unit conversion, mm->cm in order to agree with mu units
        
        f=open("pickle\\reg.pkl","wb")
        reg_data={"mat": mat, "xlen": xlen, "ylen": ylen, "xdiv" : xdiv,"ydiv": ydiv,"thickness" : thickness2,"dist":dist}
        pickle.dump(reg_data, f)
        f.close()
        #close window after submit is pressed
        self.reject()
    
    def regloadvalues(self):
        """Reads the values of the most recent region data, loads values"""
        f=open("pickle\\reg.pkl","rb")
        reg=pickle.load(f)
        f.close()

        thickness=" ".join([str(10*i) for i in reg["thickness"]])
        self.ui.reg_material.setText(reg["mat"])
        self.ui.reg_distance.setText(reg["dist"])
        self.ui.reg_thickness.setText(thickness)
        self.ui.reg_xdivisions.setText(reg["xdiv"])
        self.ui.reg_xlength.setText(reg["xlen"])
        self.ui.reg_ydivisions.setText(reg["ydiv"])
        self.ui.reg_ylength.setText(reg["ylen"])
        
def main():
    app=QtGui.QApplication(sys.argv)
    ad=RDialog()
    ad.exec_()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()