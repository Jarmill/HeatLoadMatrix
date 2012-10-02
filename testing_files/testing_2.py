"""Gigantic Function Testing File!"""
#imports 
from basic_functions import cell2
import _pickle as pickle
from os import system

#pseudoglobal values
hd=2
vd=2
h=2
v=2
source="wig"

def patch_centers(x_offset=0,y_offset=0):
    """Calculates Centers of rectangular cells"""
    #create empty array
    patch=cell2(hd,vd)
            
    for i in range(0,vd):
        for j in range(0,hd):
            x=(2*j-1)*h/(2*hd)+x_offset
            y=v+y_offset+(3-2*i)*v/(2*vd)
            patch[i][j]=[x,y]        
    return patch

#x values           

def buildusmatrix(self,x_offset=0,y_offset=0):
    """Builds the xop-formatted undulator matrix from user-entered values"""
    #user input (undulator)
    title="Megatest!"
    energy="5.3"
    current="250"
    period="3.3"
    num="70"
    sigx=".3"
    sigy=".06"
    sigx1=".025"
    sigy1=".0053"
    kx="0"
    ky="2.76"
    xpos=str(x_offset)
    ypos=str(y_offset)

    #pickled data        
    freg=open("reg.pkl","rb")
    reg=pickle.load(freg)
    freg.close()

    advf=open("adv.pkl","rb")
    adv=pickle.load(advf)
    advf.close()
    
    matrix=[[title,"0","0","0","0","0","0"],\
            [energy, current, "0","0","0","0","0"],\
            [sigx,sigy,sigx1,sigy1,"0","0","0"],\
            [period,num,kx,ky,"0","0","0"],\
            [str(adv["estart"]),str(adv["eend"]),str(adv["ediv"]),"0","0","0","0"],\
            [str(reg["dist"]),xpos,ypos,str(reg["xlen"]),str(reg["ylen"]),str(reg["xdiv"]),str(reg["ydiv"])],\
            [adv["mode"],adv["method"],adv["harmonic"],"0","0","0","0"],\
            [adv["nphi"],adv["nalpha"],adv["calpha2"],adv["nomega"],adv["comega"],adv["nsigma"],"0"]]
    
    return matrix

def buildwsmatrix(self,x_offset=0,y_offset=0):
    """Builds the xop-formatted wiggler matrix from user-entered values"""
    title="Megatest!"
    energy="5.3"
    current="250"
    period="3.3"
    num="70"
    kx="0"
    ky="2.76"
    xpos=str(x_offset)
    ypos=str(y_offset)
    
    #pickled data        
    freg=open("reg.pkl","rb")
    reg=pickle.load(freg)
    freg.close()

    advf=open("adv.pkl","rb")
    adv=pickle.load(advf)
    advf.close()
    
    
    matrix=[[title,"0","0","0","0","0","0"],\
            [energy, current,"0","0","0","0","0"],\
            [period,num,kx,ky,"0","0","0"],\
            [str(adv["estart"]),str(adv["eend"]),str(adv["ediv"]),"0","0","0","0"],\
            [str(reg["dist"]),xpos,ypos,str(reg["xlen"]),str(reg["ylen"]),str(reg["xdiv"]),str(reg["ydiv"])],\
            ["4","0","0","0","0","0","0"]]
    
    return matrix

def generate_energy_axis(self):
    """returns x axis energy values"""
    if source=="wig":
        sdata=pickle.load(open("ws_data.pkl","rb"))
    elif source=="und":
        sdata=pickle.load(open("us_data.pkl","rb"))
    else:
        raise NameError("unknown source")
        
    g=[sdata[i][0] for i in range(0,len(sdata))]
    return g

def us(self,x_offset=0,y_offset=0):
    """writes the matrix to us.inp, runs ws.exe, and processes the result"""
    matrix=buildusmatrix(x_offset,y_offset)
    s=""
    for i in matrix: 
        s+=",".join(i)
        s+="\n"
    
    #writes data into ws.inp
    f=open("us.inp", "w")
    f.write(s)
    f.close()
    
    #runs xop
    system(self.xop_path+"us.exe")
    
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
    
def patch_flux(self,x_offset=0,y_offset=0):
    """Runs ws() and us() depending upon the source"""
    #should i keep the ws and build matrix functions in wig and und, or move them here? decisions, decisions. resolved, moved to backend.
    if source=="wig":
        ws(x_offset,y_offset)
    elif self.source=="und":
        us(x_offset,y_offset)
    else: 
        raise NameError("unknown source")

def ws(self,x_offset=0,y_offset=0):
        """writes the matrix to ws.inp, runs ws.exe, and processes the result"""
        matrix=buildwsmatrix(x_offset,y_offset)
        s=""
        for i in matrix: 
            s+=",".join(i)
            s+="\n"
        #writes data into ws.inp
        f=open("ws.inp", "w")
        f.write(s)
        f.close()
        
        #runs xop
        system(self.xop_path+"ws.exe")
        
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

def source_flux(self):
    """finds the energy flux in a region, through multiple calls to xop"""
    s_flux=uncorrected_flux=cell2(self.hd,self.vd)
    
    pc=patch_flux()
    ea=self.generate_energy_axis()
    #number_of_patches=str(self.vd*self.hd)
    
    for i in range(0,self.vd):
        for j in range(0, self.hd):
            x_offset=pc[i][j][0]
            y_offset=pc[i][j][1]
            s_flux[i][j]=self.patch_flux(x_offset,y_offset)
            
            uncorrected_flux[i][j]=s_flux[i][j]
            
            if i==0 and j==0:
                dE=ea[1]-ea[0]
            
            for k in range(0,len(ea)):
                s_flux[i][j][k]=s_flux[i][j][k]*1000*dE/ea[k]
    return s_flux   
patch=patch_centers()
patch_s=[list(map(str,i)) for i in patch]
            
s="\n".join([",".join(i) for i in patch_s])
print(s)