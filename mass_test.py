#import backend_pre_loop_optimize as backend
import backend as backend
from multiprocessing import cpu_count

class MassTest(backend.Back):
    def __init__(self, f_name=None,source="wig"):
        print("Beginning mass test of heatbump with: ",f_name)
        self.source=source
        if f_name==None:
            self.no_file_param()
        else:
            self.file_param(f_name)
        
        
    def no_file_param(self):
        #debugging
        #self.print_matrix_sums = True
        self.print_matrix_sums = False
        
        #multiprocessing parameters
        self.XOP_Processes = []
        self.XOP_run_at_one_time = cpu_count()
        
        self.title="wiggler 2x2mm 8x8 l div"
        
        self.source="wig"
        
        self.flt_list=[["Be",.0100]]
        
        if self.source=="und":
            self.energy=5.3
            self.current=10
            self.period=2.44
            self.num=40
            self.sigx=1.070
            self.sigy=.081
            self.sigx1=.1433
            self.sigy1=.0135
            self.kx=0
            self.ky=2.350
        
        elif self.source=="wig":
            self.energy=5.3
            self.current=250
            self.period=12
            self.num=49
            self.kx=0
            self.ky=9
        
        else:
            raise NameError("Invalid source (not undulator nor wiggler)")
        
        self.h=2
        self.v=2
        self.hd=8
        self.vd=8
        self.mat="Si"
        self.thickness=[110.0]
        self.dist=20.0
        
        #scan values
        self.estart=500
        self.eend=100000
        self.ediv=5000
        self.xint=10
        self.yint=10
        
        #intrinsic parameters DO NOT TOUCH!
        self.mode=4
        self.method=4
        self.harmonic=0
        self.nphi=0
        self.nalpha=0
        self.calpha2=0
        self.nomega=64
        self.comega=8
        self.nsigma=0
        
        #Interpolation guard/rectangle handling
        #interpolation guard on
        
        self.LIP=True #TURN ON AFTER TESTING!
        #self.LIP=False #TURN ON AFTER TESTING!
        
        #intepolation guard length
        self.d=10**-9
        #set up rectangle handling
        self.rect_setup()
        
        #THE NUCLEAR OPTION. Do you want to enable rmtree to wipe the "job" folder after each run?
        #self.NUKE_JOBS=True
        self.NUKE_VARS=True
        self.MATHEMATICA_OUTPUT=False

        self.rect_setup()
        
        #file path (only good for specuser). First time setup will need to be implemented in order for this to work universally
        self.xop_path="C:\\xop2.3\\bin.x86\\"
        #self.pout=adv["power"]
        self.pout="both"
    def file_param(self,f_name):
        print("Hi! You are using ",f_name,".")
    def back_gui_values(self):
        print("NO GUI ALLOWED!")
if __name__=="__main__":
    mt=MassTest(None,"wig")
    mt.heat_load_matrix()
    
