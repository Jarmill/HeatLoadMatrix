#import sys
from PyQt4 import QtGui, QtCore
from ui.advancedoptions_ui import Ui_Dialog
import _pickle as pickle

class ADialog(QtGui.QDialog):
    """sets up advanced options function, activiated through undulator"""
    def __init__(self):
        super(ADialog,self).__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        #Button Box connections (OK/Cancel)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.optpickle)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
    
    def optpickle(self):
        """Reads input from options dialog, and serializes results into dictionary in adv.pkl"""
        #intrinsic parameters
        nphi=self.ui.nphi.text()
        nalpha=self.ui.nalpha.text()
        calpha2=self.ui.calpha.text()
        nomega=self.ui.nomega.text()
        comega=self.ui.comega.text()
        nsigma=self.ui.nsigma.text()
        
        #method
        if self.ui.method_1.isChecked():   method=2
        elif self.ui.method_2.isChecked(): method=3
        else: method=4
        
        #mode
        if self.ui.mode_1.isChecked():  mode=1
        elif self.ui.mode_2.isChecked(): mode=2
        elif self.ui.mode_3.isChecked(): mode=3
        elif self.ui.mode_4.isChecked(): mode=4
        elif self.ui.mode_5.isChecked(): mode=5
        elif self.ui.mode_6.isChecked(): mode=6
        else:mode=4
        
        #harmonic
        if self.ui.harmonic_1.isChecked():   harmonic=0
        elif self.ui.harmonic_2.isChecked(): harmonic=-1
        elif self.ui.harmonic_3.isChecked(): harmonic=1
        elif self.ui.harmonic_4.isChecked(): harmonic=self.ui.harmonic_4_custom.text()
        else: harmonic=0
        
        #scan parameters
        estart=self.ui.estart.text()
        eend=self.ui.eend.text()
        ediv=self.ui.ediv.text()
        xint=self.ui.xint.text()
        yint=self.ui.yint.text()
        
        #write into file
        f=open("adv.pkl","wb")
        adv_data={"nphi":str(nphi), "nalpha":str(nalpha), "calpha2":str(calpha2), "nomega":str(nomega), "comega":str(comega),"nsigma":str(nsigma), "method":str(method), "mode":str(mode),"harmonic":str(harmonic), "estart":str(estart), "eend":str(eend),"ediv":str(ediv),"xint":str(xint),"yint":str(yint)}
        pickle.dump(adv_data, f)
        f.close()
        self.reject()