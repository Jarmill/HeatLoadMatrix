#import basic and PyQt module-s
from PyQt4 import QtGui, QtCore
import advancedoptions
import _pickle as pickle
import os

#import undulator layout
from undulator_ui_xop import Ui_Dialog

#import backend functionality
import backend

class UDialog(QtGui.QDialog, backend.Back):
    """Undulator functionailty"""
    def __init__(self):
        #GUI Setup
        super(UDialog,self).__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.connect(self.ui.advanced_button,QtCore.SIGNAL("clicked()"),self.adv_new_window)
        
        #Button Box connections (OK/Cancel)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.buildusmatrix2)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        
        #set "global" values, hopefully dodge diamond of death
        #self.back_values("und")
        
    def buildusmatrix2(self):
        """Builds the xop-formatted matrix from user-entered values"""
        #user input (undulator)
        title=self.ui.und_title.text()
        energy=self.ui.und_energy.text()
        current=self.ui.und_current.text()
        period=self.ui.und_period.text()
        num=self.ui.und_nperiods.text()
        sigx=self.ui.und_sigx.text()
        sigy=self.ui.und_sigy.text()
        sigx1=self.ui.und_sigx1.text()
        sigy1=self.ui.und_sigy1.text()
        kx=self.ui.und_kx.text()
        ky=self.ui.und_ky.text()
        estart=self.ui.und_estart.text()
        eend=self.ui.und_eend.text()
        ediv=self.ui.und_edivisions.text()
        distance=self.ui.und_distance.text()
        xpos=self.ui.und_xposition.text()
        xdiv=self.ui.und_xintpoints.text()
        xslit=self.ui.und_xslit.text()
        ypos=self.ui.und_yposition.text()
        ydiv=self.ui.und_yintpoints.text()
        yslit=self.ui.und_yslit.text()
        
        #pickled data
        advf=open("adv.pkl","rb")
        adv=pickle.load(advf)
        advf.close()
        
        matrix=[[title,"0","0","0","0","0","0"],\
                [energy, current, "0","0","0","0","0"],\
                [sigx,sigy,sigx1,sigy1,"0","0","0"],\
                [period,num,kx,ky,"0","0","0"],\
                [estart,eend,ediv,"0","0","0","0"],\
                [distance,xpos,ypos,xslit,yslit,xdiv,ydiv],\
                [adv["mode"],adv["method"],adv["harmonic"],"0","0","0","0"],\
                [adv["nphi"],adv["nalpha"],adv["calpha2"],adv["nomega"],adv["comega"],adv["nsigma"],"0"]]
        self.us2(matrix)
    
    def reject(self):
        QtGui.QDialog.reject(self)
        
    def us2(self,matrix):
            """writes the matrix to us.inp, runs ws.exe, and processes the result"""
            
            s=""
            for i in matrix: 
                s+=",".join(map(str,i))
                s+="\n"
            
            #writes data into ws.inp
            f=open("us.inp", "w")
            f.write(s)
            f.close()
            
            #runs xop
            os.system("C:\\Users\\Public\\Documents\\xop2.3\\bin.x86\\us.exe")
            
            #reads results
            us_data=[]
            f2=open("us.out","r")
            for i, line in enumerate(f2):
                if i>=23:
                    g=line[0:26].split()
                    us_data.append([float(x) for x in g])        
            f2.close()
            
            #pickle results to file
            f3=open("us_data.pkl","wb")
            pickle.dump(us_data, f3)
            f3.close()
            
            #export clean results for testing
            st=""
            for i in us_data:
                st+=(str(i[0])+","+str(i[1]))
                st+="\n"
            f4=open("us.csv","w")
            f4.write(st)
            f4.close()
                
    def adv_new_window(self):
        """Pops up Advanced Options"""
        adv=advancedoptions.ADialog()
        adv.exec_()
