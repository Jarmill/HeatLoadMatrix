import sys
from PyQt4 import QtGui

class Hub(QtGui.QWidget):
    def __init__(self):
        super(Hub,self).__init__()
        self.initUI()
    def initUI(self):
        self.show()
        
def main():
    app=QtGui.QApplication(sys.argv)
    h=Hub()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()