#basic and PyQt modules
import sys
from PyQt4 import QtGui, QtCore
import _pickle as pickle

#filter layout
from ui.filters_ui import Ui_Dialog

class FDialog(QtGui.QDialog):
    def __init__(self):
        """Filter constructor, loads ui layout, values, and button connections"""
        super(FDialog,self).__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.flt_load_values()
        self.show()
        #Button Box connections (OK/Cancel)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.flt_pickle)

    """def dropdown_grey(self): Need to find a way to make more than 5 filters, very low priority"""
    
    def flt_pickle(self):
        """Saves submitted filter values into pickled file for storage"""
        #all filter thickness are in microns. Need to be converted to cm to be used in transmission calculations
        #Filter (material, thickness) pairs are only saved to file if both of them are nonempty
        if self.ui.material_1.text() and self.ui.thickness_1.text() != "":
            mat1=self.ui.material_1.text()
            thick1=float(self.ui.thickness_1.text())
        else: mat1=thick1=None    
        
        if self.ui.material_2.text() and self.ui.thickness_2.text() != "":
            mat2=self.ui.material_2.text()
            thick2=float(self.ui.thickness_2.text())
        else: mat2=thick2=None    
        
        if self.ui.material_3.text() and self.ui.thickness_3.text() != "":
            mat3=self.ui.material_3.text()
            thick3=float(self.ui.thickness_3.text())
        else: mat3=thick3=None    
        
        if self.ui.material_4.text() and self.ui.thickness_4.text() != "":
            mat4=self.ui.material_4.text()
            thick4=float(self.ui.thickness_4.text())
        else: mat4=thick4=None    
        
        if self.ui.material_5.text() and self.ui.thickness_5.text() != "":
            mat5=self.ui.material_5.text()
            thick5=float(self.ui.thickness_5.text())
        else: mat5=thick5=None    
        
        #construct pair-list, and pickle to file
        l=[[mat1, thick1],[mat2,thick2],[mat3,thick3],[mat4,thick4],[mat5,thick5]]
        f=open("pickle\\flt.pkl","wb")
        pickle.dump(l, f)
        f.close()
        self.reject()
        
    def flt_load_values(self):
        """Recalls values from last entry"""
        f=open("pickle\\flt.pkl","rb")
        flt=pickle.load(f)
        f.close()
        
        for i in range(0,len(flt)):
            #DANGERDANGERDANGER TURN BACK NOW BEFORE IT'S TOO LATE (eval being used)
            if flt[i][0]==None or flt[i][1]==None:
                flt[i][0]=""
                flt[i][1]=""
            eval("self.ui.material_"+str(i+1)+".setText(\""+str(flt[i][0])+"\")")
            eval("self.ui.thickness_"+str(i+1)+".setText(\""+str(flt[i][1])+"\")")
            
def main():
    #can run without heatbump
    app=QtGui.QApplication(sys.argv)
    fd=FDialog()
    fd.exec_()
    sys.exit(app.exec())
    
if __name__=="__main__":
    #runs indirectly
    main()