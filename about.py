from PyQt4 import QtGui, QtCore
from ui.about_ui import Ui_Dialog
import sys

class AbDialog(QtGui.QDialog):
    def __init__(self):
        super(AbDialog,self).__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        #Button Box connections (OK/Cancel)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.reject)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        
    def reject(self):
        QtGui.QDialog.reject(self)
        
def main():
    """Runs About without Heatbump"""
    app=QtGui.QApplication(sys.argv)
    abd=AbDialog()
    abd.exec_()
    sys.exit(app.exec_())

if __name__=="__main__":
    #only runs when directly called
    main()