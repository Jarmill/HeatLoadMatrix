#import backend_pre_loop_optimize as backend
import backend as backend
from multiprocessing import cpu_count
from basic_functions import cell1, cell2, cell3, mult, mu3, depth, matchdim, print_sum_matrix_by_layer, print_number, print_sum_matrix
from os import path, makedirs

class MassTest(backend.Back):
    def __init__(self, f_name,source):
        print("Beginning mass test of heatbump with: ",f_name)
        self.source=source
        if f_name==None:
            self.no_file_param()
        else:
            self.file_param(f_name)
        self.rect_setup()
        
    def no_file_param(self):
        #debugging
        #self.print_matrix_sums = True
        self.print_matrix_sums = False
        
        #multiprocessing parameters
        self.XOP_Processes = []
        self.XOP_run_at_one_time = cpu_count()
        
        self.title="20x20 range test"
        
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
        self.thickness=[70]
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
        self.d=10**-6
        #set up rectangle handling
        self.rect_setup()
        
        #THE NUCLEAR OPTION. Do you want to enable rmtree to wipe the "job" folder after each run?
        #self.NUKE_JOBS=True
        self.NUKE_VARS=True
        self.MATHEMATICA_OUTPUT=True
        
        
        #file path (only good for specuser). First time setup will need to be implemented in order for this to work universally
        self.xop_path="C:\\xop2.3\\bin.x86\\"
        #self.pout=adv["power"]
        self.pout="both"
    def file_param(self,f_name):
        print("Hi! You are using ",f_name,".")
    def back_gui_values(self):
        print("NO GUI ALLOWED!")
    def source_flux_2(self):
        """finds the energy flux in a region, through multiple calls to xop. ->3d"""
        if self.LIP==True:
            s_flux=cell2(self.hd+2,self.vd+2)
            uncorrected_flux=cell2(self.hd+2,self.vd+2)
        else:
            s_flux=cell2(self.hd,self.vd)
            uncorrected_flux=cell2(self.hd,self.vd)
        
        pc=self.rect_centers()
        dimensions = self.rect_dimensions()
        ea=self.generate_energy_axis()
        dE=ea[1]-ea[0]
        
        if self.LIP==True:
            ilimit=self.vd+2
            jlimit=self.hd+2
        else:
            ilimit=self.vd
            jlimit=self.hd
        #print(depth(pc),[ilimit,len(pc)],[jlimit,len(pc[0]),])
        
        self.jobs_to_run = ilimit * jlimit
        self.jobs_completed = 0
        self.jobs_overcommit_at_end = 1.5
                
        jobdirroot = '.\\job'
        if not path.exists(jobdirroot):
            makedirs(jobdirroot)

        # Phase 1 - Generate input files for XOP programs          
        for i in range(0,ilimit):
            for j in range(0,jlimit):
                x_offset=pc[j][i][0]
                y_offset=pc[j][i][1]
                x_dim=dimensions[j][i][0]
                y_dim=dimensions[j][i][1]
                jobdir = jobdirroot + '\\' + str(i) + '-' + str(j)
                if not path.exists(jobdir):
                    makedirs(jobdir)
                self.patch_flux(x_offset,y_offset, 1, jobdir, x_dim, y_dim)

        # Phase 2 - Run XOP programs, multi-processing           
        for i in range(0,ilimit):
            for j in range(0,jlimit):
                x_offset=pc[j][i][0]
                y_offset=pc[j][i][1]
                jobdir = jobdirroot + '\\' + str(i) + '-' + str(j)
                x_dim=dimensions[j][i][0]
                y_dim=dimensions[j][i][1]
                self.patch_flux(x_offset,y_offset, 2, jobdir, x_dim, y_dim)

        self.patch_flux(0, 0, 2, 'waitforall')  # wait for remaining jobs to finish              

        # Phase 3 - Read output files from XOP programs and incorporate data            
        for i in range(0,ilimit):
            for j in range(0,jlimit):
                x_offset=pc[j][i][0]
                y_offset=pc[j][i][1]
                jobdir = jobdirroot + '\\' + str(i) + '-' + str(j)
                x_dim=dimensions[j][i][0]
                y_dim=dimensions[j][i][1]
                s_flux[i][j]=self.patch_flux(x_offset,y_offset, 3, jobdir, x_dim, y_dim)
                uncorrected_flux[i][j]=s_flux[i][j]

                print((i,j), len(s_flux),len(s_flux[i]),len(s_flux[i][j]),len(ea))
                
                assert depth(s_flux)==3
                if self.LIP:
                    assert ilimit==self.vd+2
                    assert jlimit==self.hd+2 
                else:
                    assert ilimit==self.vd 
                    assert jlimit==self.hd 
                assert ilimit==len(s_flux)
                assert jlimit==len(s_flux[i])
                #assert len(ea)==len(s_flux[i][j])

                #for m in range(0,len(ea)):
                    #convert from bandpass to raw flux(ph/s/.1%BW -> ph/s)
                    #GOTCHA! Bug, i found you!
                    #s_flux[i][j][m]*=1000*dE/ea[m]
                    #s_flux[i][j][k]=s_flux[i][j][k]*1000*dE/ea[k]
        #self.write_uncorrected_flux(uncorrected_flux)
        
        return s_flux
if __name__=="__main__":
    mt=MassTest(None,"wig")
    #mt.heat_load_matrix()
    mt.source_flux_2()
