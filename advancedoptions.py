#import sys
from PyQt4 import QtGui, QtCore
from ui.advancedoptions_ui import Ui_AdvancedOptions
import _pickle as pickle
import sys

class ADialog(QtGui.QDialog):
    """sets up advanced options function, activiated through undulator"""
    def __init__(self):
        super(ADialog,self).__init__()
        self.ui=Ui_AdvancedOptions()
        self.ui.setupUi(self)
        self.adv_load_values()
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
        
        #power output preference
        if self.ui.power_1.isChecked():     power="power"
        elif self.ui.power_2.isChecked():   power="density"
        else:   power="density"
        
        #scan parameters
        estart=self.ui.estart.text()
        eend=self.ui.eend.text()
        ediv=self.ui.ediv.text()
        xint=self.ui.xint.text()
        yint=self.ui.yint.text()
        
        #write into file
        f=open("pickle\\adv.pkl","wb")
        adv_data={"power":str(power),"nphi":str(nphi), "nalpha":str(nalpha), "calpha2":str(calpha2), "nomega":str(nomega), "comega":str(comega),"nsigma":str(nsigma), "method":str(method), "mode":str(mode),"harmonic":str(harmonic), "estart":str(estart), "eend":str(eend),"ediv":str(ediv),"xint":str(xint),"yint":str(yint)}
        pickle.dump(adv_data, f)
        f.close()
        self.reject()
        
    def adv_load_values(self):
        f=open("pickle\\adv.pkl","rb")
        adv=pickle.load(f)
        f.close()
        
        #intrinsic paramters
        self.ui.nphi.setText(adv["nphi"])
        self.ui.nalpha.setText(adv["nalpha"])
        self.ui.calpha.setText(adv["calpha2"])
        self.ui.nomega.setText(adv["nomega"])
        self.ui.comega.setText(adv["comega"])
        self.ui.nsigma.setText(adv["nsigma"])
        
        #scan parameters
        self.ui.estart.setText(adv["estart"])
        self.ui.eend.setText(adv["eend"])
        self.ui.ediv.setText(adv["ediv"])
        self.ui.xint.setText(adv["xint"])
        self.ui.yint.setText(adv["yint"])
        
        #loading values
        method=int(adv["method"])
        mode=int(adv["mode"])
        power=adv["power"]
        harmonic=int(adv["harmonic"])
        
        #method
        if method==2:    self.ui.method_1.setChecked(True)
        elif method==3:  self.ui.method_2.setChecked(True)
        else:            self.ui.method_3.setChecked(True)
        
        #mode
        if mode==1:     self.ui.mode_1.setChecked(True)
        elif mode==2:   self.ui.mode_2.setChecked(True)
        elif mode==3:   self.ui.mode_3.setChecked(True)
        elif mode==4:   self.ui.mode_4.setChecked(True)
        elif mode==5:   self.ui.mode_5.setChecked(True)
        elif mode==6:   self.ui.mode_6.setChecked(True)
        else:           self.ui.mode_4.setChecked(True)
        
        #power
        if power=="power":      self.ui.power_1.setChecked(True)
        elif power=="density":  self.ui.power_2.setChecked(True)
        else:                   self.ui.power_2.setChecked(True)
        
        #harmonic
        if harmonic==0:     self.ui.harmonic_1.setChecked(True)
        elif harmonic==1:   self.ui.harmonic_2.setChecked(True)
        elif harmonic==-1:  self.ui.harmonic_3.setChecked(True)
        elif harmonic>1:    
            self.ui.harmonic_4.setChecked(True)
            self.ui.harmonic_4_custom.setText(str(harmonic))
        else:               self.ui.harmonic_1.setChecked(True)
        
def main():
    app=QtGui.QApplication(sys.argv)
    ad=ADialog()
    ad.exec_()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()