#imports
import sys
from PyQt4 import QtGui, QtCore
from wiggler_ui_xop import Ui_Dialog
import os
import pickle

#import back-end functionailty
import backend 

class WDialog(QtGui.QDialog,backend.Back):
    """Wiggler Functionailty"""
    def __init__(self):
        #set up GUI
        super(WDialog,self).__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        
        #Button Box connections (OK/Cancel)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.buildwsmatrix2)
        
        #set "global" values, hopefully dodge diamond of death
        #self.back_values("wig")
        
        
        
    def buildwsmatrix2(self):
        """Builds the xop-formatted matrix from user-entered values"""
        title=self.ui.wig_title.text()
        energy=self.ui.wig_energy.text()
        current=self.ui.wig_current.text()
        period=self.ui.wig_periods.text()
        num=self.ui.wig_nperiods.text()
        kx=self.ui.wig_kx.text()
        ky=self.ui.wig_ky.text()
        estart=self.ui.wig_estart.text()
        eend=self.ui.wig_eend.text()
        ediv=self.ui.wig_edivisions.text()
        distance=self.ui.wig_distance.text()
        xpos=self.ui.wig_xposition.text()
        xdiv=self.ui.wig_xintpoints.text()
        xslit=self.ui.wig_xslit.text()
        ypos=self.ui.wig_yposition.text()
        ydiv=self.ui.wig_yintpoints.text()
        yslit=self.ui.wig_yslit.text()
        
        matrix=[[title,"0","0","0","0","0","0"],\
                [energy, current,"0","0","0","0","0"],\
                [period,num,kx,ky,"0","0","0"],\
                [estart,eend,ediv,"0","0","0","0"],\
                [distance,xpos,ypos,xslit,yslit,xdiv,ydiv],\
                ["4","0","0","0","0","0","0"]]
        self.ws2(matrix)
    
    def ws2(self,matrix):
        """writes the matrix to ws.inp, runs ws.exe, and processes the result"""
        
        s=""
        for i in matrix: 
            s+=",".join(i)
            s+="\n"
        #writes data into ws.inp
        f=open("ws.inp", "w")
        f.write(s)
        f.close()
        
        #runs xop
        os.system("C:\\xop2.3\\bin.x86\\ws.exe")
        
        #reads results
        ws_data=[]
        f2=open("ws.out","r")
        #For some reason, some of the x data is being truncated.
        for i, line in enumerate(f2):
            if i>=18:
                g=line[0:26].split()
                ws_data.append([float(x) for x in g])        
        f2.close()
        f3=open("ws_data.pkl","wb")
        pickle.dump(ws_data, f3)
        f3.close()
        
        #export clean results for testing
         
        st=""
        for i in ws_data:
            st+=(str(i[0])+","+str(i[1]))
            st+="\n"
        print(st[0:50])
        f4=open("ws.csv","w")
        f4.write(st)
        f4.close()

def main():
    app=QtGui.QApplication(sys.argv)
    wd=WDialog()
    wd.exec_()
    sys.exit(app.exec_())