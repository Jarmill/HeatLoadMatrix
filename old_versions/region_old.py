#import sys
from PyQt4 import QtGui, QtCore
from regionparam_ui import Ui_Dialog

class RDialog(QtGui.QDialog):
    def __init__(self):
        super(RDialog,self).__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.filetest)
        
    def filetest(self):
        xlen=self.ui.reg_xlength.text()
        ylen=self.ui.reg_ylength.text()
        xdiv=self.ui.reg_xdivisions.text()
        ydiv=self.ui.reg_ydivisions.text()
        mat=self.ui.reg_material.text()
        
        f=open("filtertest.txt","w")
        f.write(xlen+"    "+xdiv+"\n"+ylen+"    "+ydiv+"\n"+mat)
        f.close()
        self.fileopen()
    def fileopen(self):
        f=open("filtertest.txt","r")
        print("".join(f.readlines()))
        f.close()
        #print("Hello World!")
        
        self.show()
"""
def main():
    app=QtGui.QApplication(sys.argv)
    rd=RDialog()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()
"""