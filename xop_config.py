#import basic and PyQt modules
from PyQt4 import QtGui, QtCore
import json
import sys

#xop_config layout
from ui.xop_config_ui import Ui_Dialog

class XDialog(QtGui.QDialog):
    def __init__(self):
        """xop constructor"""
        super(XDialog, self).__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        
        f=open("pickle\\run.json","r")
        run=json.load(f)
        f.close()
        self.ui.xop_name.setText(run["xop_path"])
        
        QtCore.QObject.connect(self.ui.xop_box, QtCore.SIGNAL("accepted()"), self.xopset)
        QtCore.QObject.connect(self.ui.xop_box, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QObject.connect(self.ui.xop_submit, QtCore.SIGNAL("clicked()"), self.xopsetup)
        
    def xopsetup(self):
        f=open("pickle\\run.json","r")
        run=json.load(f)
        f.close()
        filename=str(QtGui.QFileDialog.getExistingDirectory(self,"Select Directory"))
        print(run)
        self.ui.xop_name.setText(filename)
    
    def xopset(self):
        filename=self.ui.xop_name.text()
        f=open("pickle\\run.json", "r")
        run=json.load(f)
        f.close()
        
        run["xop_path"]=filename
        
        f=open("pickle\\run.json","w")
        json.dump(run,f)
        f.close()
        
def main():
    app=QtGui.QApplication(sys.argv)
    ad=XDialog()
    ad.exec_()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()