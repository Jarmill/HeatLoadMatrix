                                                                         
#The big import block
#basic algorithms/operations
from basic_functions import cell1, cell2, cell3, mult, mu3, depth, matchdim, print_sum_matrix_by_layer, print_number, print_sum_matrix
import math
from time import time, sleep
from copy import deepcopy
#reading and writing data
import _pickle as pickle
#grid functionality
import rectangle_grid
#subprocess modules
from multiprocessing import cpu_count
import subprocess
from os import path, makedirs
#THE NUCLEAR OPTION
from shutil import rmtree

"""
Always remember to check that total power=power absorbed+power transmitted. If it does not, sign of a deep error in computation. now abbreviated as p=a+t

Version 1.0
The centipede has been caught! This error turned values of source_flux from 10^12 --> 10^-21, due to a "=" instead of a "==" in region_filtered flux
Version 1.1
Interpolation guard is now implemented. The previous implementation did not work well, working on now. Created a new class and rectangle handling function to deal with this error.
Version 1.2
A speed boost was added while filtering (instead of using a sequential search to find mu values, a binary search is now used) cut processing time in python from 300s to 5s
Version 2.0
Multiprocessing added. This update later included "overdrive", where if half the cores are finished, a new dispatch occurs. Instead of time being cut by a factor of N, now it is cut by 1.5N (N=number of cores)
There were a series of numerical errors, which included large errors in p=a+t, when multiple slices were implemented. There was also a difference in power values when the slices were (100,10)mm,(110)mm,(10,100)mm, or (10)mmx11. This was due to reference errors, and fixed by using deepcopy
The write_slice_to_table function was rehauled, in order to implement changes as due to rectangle_grid.
There are still some index naming errors, these are of low priority and will be fixed in next release.

Next Release:
Creating/figuring out progress bar
Progressive meshing
"""

class Back(rectangle_grid.pc):
    """This class contains all the misc functions that allow heatbump to run. The main event is heat_load_matrix()"""
    def back_values(self,source):
        """pseudoglobal values. These are initialized as part of WDialog and UDialog's __init__() method, to avoid the diamond of death"""

        #region values
        advf=open("pickle\\adv.pkl","rb")
        adv=pickle.load(advf)
        advf.close()
        
        freg=open("pickle\\reg.pkl","rb")
        reg=pickle.load(freg)
        freg.close()

        #debugging
        #self.print_matrix_sums = True
        self.print_matrix_sums = False
        
        #multiprocessing parameters
        self.XOP_Processes = []
        self.XOP_run_at_one_time = cpu_count()
        
        self.h=float(reg["xlen"])
        self.v=float(reg["ylen"])
        self.hd=int(reg["xdiv"])
        self.vd=int(reg["ydiv"])
        self.mat=reg["mat"]
        self.thickness=[float(i) for i in reg["thickness"]]
        self.dist=float(reg["dist"])
        
        #scan values
        self.estart=int(adv["estart"])
        self.eend=int(adv["eend"])
        self.ediv=int(adv["ediv"])
        
        #other        
        self.source=source
        
        #Interpolation guard/rectangle handling
        #interpolation guard on
        
        self.LIP=True #TURN ON AFTER TESTING!
        #self.LIP=False #TURN ON AFTER TESTING!
        
        #intepolation guard length
        self.d=10**-9
        #set up rectangle handling
        self.rect_setup()
        
        #THE NUCLEAR OPTION. Do you want to enable rmtree to wipe the "job" folder after each run?
        self.NUKE_JOBS=True
        
        #file path (only good for specuser). First time setup will need to be implemented in order for this to work universally
        self.xop_path="C:\\xop2.3\\bin.x86\\"
        #self.pout=adv["power"]
        self.pout="testing"
    def buildusmatrix(self,x_offset=0,y_offset=0):
        """Builds the xop-formatted undulator matrix from user-entered values"""
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
        xpos=str(x_offset)
        ypos=str(y_offset)

        #pickled data        
        freg=open("pickle\\reg.pkl","rb")
        reg=pickle.load(freg)
        freg.close()

        advf=open("pickle\\adv.pkl","rb")
        adv=pickle.load(advf)
        advf.close()
        
        matrix=[[title,"0","0","0","0","0","0"],\
                [energy, current, "0","0","0","0","0"],\
                [sigx,sigy,sigx1,sigy1,"0","0","0"],\
                [period,num,kx,ky,"0","0","0"],\
                #stand back, i'm trying science! hopefully this will kill the off-by-one error.
                [str(adv["estart"]),str(adv["eend"]),str(int(adv["ediv"])-1),"0","0","0","0"],\
                [str(reg["dist"]),xpos,ypos,str(self.h/self.hd),str(self.v/self.vd),str(adv["xint"]),str(adv["yint"])],\
                [adv["mode"],adv["method"],adv["harmonic"],"0","0","0","0"],\
                [adv["nphi"],adv["nalpha"],adv["calpha2"],adv["nomega"],adv["comega"],adv["nsigma"],"0"]]
        
        return matrix
    
    def buildwsmatrix(self,x_offset=0,y_offset=0):
        """Builds the xop-formatted wiggler matrix from user-entered values"""
        title=self.ui.wig_title.text()
        energy=self.ui.wig_energy.text()
        current=self.ui.wig_current.text()
        period=self.ui.wig_periods.text()
        num=self.ui.wig_nperiods.text()
        kx=self.ui.wig_kx.text()
        ky=self.ui.wig_ky.text()
        xpos=str(x_offset)
        ypos=str(y_offset)
        
        #pickled data        
        freg=open("pickle\\reg.pkl","rb")
        reg=pickle.load(freg)
        freg.close()

        advf=open("pickle\\adv.pkl","rb")
        adv=pickle.load(advf)
        advf.close()
        
        
        matrix=[[title,"0","0","0","0","0","0"],\
                [energy, current,"0","0","0","0","0"],\
                [period,num,kx,ky,"0","0","0"],\
                [str(adv["estart"]),str(adv["eend"]),str(adv["ediv"]),"0","0","0","0"],\
                [str(reg["dist"]),xpos,ypos,str(self.h/self.hd),str(self.v/self.vd),str(adv["xint"]),str(adv["yint"])],\
                ["4","0","0","0","0","0","0"]]
        
        return matrix

    def calc_slice_volumes(self):
        """Calculates the volume of each cell/voxel"""
        
        #define the width and height of each cell. Progressive meshing will involve non-constant measurements.
        #patch_height=self.v/self.vd
        #patch_width=self.h/self.hd
        
        areas=self.rect_areas()
        #highly inefficient method to find slice volumes               
                
        
        #patch_area=patch_width*patch_height
        #print(area)
        #define indices
        klimit=len(self.thickness)
        if self.LIP==True:
            ilimit=self.vd+2
            jlimit=self.hd+2  
        else:
            ilimit=self.vd
            jlimit=self.hd  
        #slice_volumes=cell3(ilimit,jlimit,klimit)
        slice_volumes=cell3(jlimit,ilimit,klimit)  ### TESTING CODE
        #print((klimit,ilimit,jlimit))
        #print(len(slice_volumes),len(slice_volumes[0]),len(slice_volumes[0][0]))
        for k in range(0,klimit):
            for i in range(0,ilimit):
                for j in range(0,jlimit):
                    #W/mm^2->W/m^2
                    #slice_volumes[k][i][j]=patch_area*self.thickness[k]*10*(10**-9)
                    slice_volumes[k][i][j]=areas[i][j]*self.thickness[k]*10*(10**-9)        

        if self.print_matrix_sums:
            print_sum_matrix_by_layer(slice_volumes, 'calc_slice_volumes')
            if len(self.thickness) > 1:
                print_sum_matrix(slice_volumes, 'calc_slice_volumes')
            
        return slice_volumes
        
    
    def filter_flux(self,s_flux):
        """Finds the transmission through a filter,#I=I0*e^(-mu*t). 3d->3d"""

        if self.print_matrix_sums:
            print_sum_matrix(s_flux, 'filter_flux s_flux')
        
        #find the user submitted filters       
        ff=open("pickle\\flt.pkl","rb")
        flt_old=pickle.load(ff)
        ff.close()
        
        ea=self.generate_energy_axis()
        

        flt=[i for i in flt_old if i[0]!=None and i[1]!=None]
        
        #calculate filtered flux through layer
        f_flux=deepcopy(s_flux)
        assert len(ea)==len(s_flux[0][0])
        
        #This handles multiple filters. Filters multiply together, and order does not matter
        #This calculation is as slow as hell, but there is no way around it
        for p in range(0,len(flt)):
            mat=flt[p][0]
            matthick=flt[p][1]/10000
            f=open("mu_data\\"+mat+".pkl","rb")
            edata=pickle.load(f)
            f.close()
            elem_energy=[i[0] for i in edata]
            elem_flux=[i[1] for i in edata]
            for i in range(0,len(s_flux)):
                for j in range(0,len(s_flux[0])):
                    #I=I0*e^(-mu*t)
                    for k in range(0,len(ea)):
                        f_flux[i][j][k]*=math.exp(-1*mu3(elem_energy,elem_flux,ea[k])*(matthick))             

        if self.print_matrix_sums:
            print_sum_matrix_by_layer(f_flux, 'filter_flux f_flux')
            if len(self.thickness) > 1:
                print_sum_matrix(f_flux, 'filter_flux f_flux')

        return f_flux
           
    def generate_energy_axis(self):
        """returns x axis energy values"""
        
        if self.source=="wig":
            sdata=pickle.load(open("pickle\\ws_data.pkl","rb"))
        elif self.source=="und":
            sdata=pickle.load(open("pickle\\us_data.pkl","rb"))
        else:
            raise NameError("unknown source")
        
        #sdata=pickle.load(open("mu_data//Xx.pkl","rb"))   
        return [i[0] for i in sdata] 
        """
        return frange(self.estart,self.eend,self.ediv)
        """

    def heat_load_matrix(self):
        """function wrapper"""
        
        tstart=time()
        
        if self.source=="wig":
            title=self.ui.wig_title.text()
        elif self.source=="und":
            title=self.ui.und_title.text()
        else:
            raise NameError("Invalid Source")

        s_flux=self.source_flux() #calculate flux in each pixel before filtering

        integrated_s_power=self.integrated_source_power(s_flux)

        #print("s_flux assignment " ,time()-tstart)
        s="\nIntegrated Source Power without filtering: "+str(integrated_s_power)+" W\n"
        
        #export f_flux resutlts for testing

        f_flux=self.filter_flux(s_flux)

        integrated_power_after_filtering=self.integrated_source_power(f_flux)

        s+="Integrated source power after filtering: "+str(integrated_power_after_filtering)+" W\n"
        #print("f_flux assignment ",time()-tstart)
        #DINGDINGDING! The bug is in one of these two functions. Phil thinks there is a faulty comparision somewhere, a = instead of an ==

        region_filtered_fluxv=self.region_filtered_flux(f_flux)        

        slice_transmissionv=self.slice_transmission()
		
        voxel_absorbed_fluxv=self.voxel_absorbed_flux(f_flux,slice_transmissionv)

        #print("voxel_absorbed_fluxv ",time()-tstart)

        voxel_absorbed_powerv=self.voxel_flux_to_power(voxel_absorbed_fluxv)

        #print("voxel_absorbed_power ",time()-tstart)        

        slice_volumesv=self.calc_slice_volumes()        

        #print("calc_slice_volume ",time()-tstart)

        voxel_absorbed_power_densityv=self.voxel_absorbed_power_density(voxel_absorbed_powerv, slice_volumesv)

        #print("voxel_absorbed_power_density ",time()-tstart)
        #print("line 263\tvoxel series")
        #print(s_flux[self.vd-1][self.hd-1][3000:3005])
        
        if self.pout=="density":
            self.write_slice_to_table(voxel_absorbed_power_densityv,title)
        elif self.pout=="power":
            self.write_slice_to_table(voxel_absorbed_powerv, title)
        elif self.pout=="testing":
            #custom testing
            self.write_slice_to_table(voxel_absorbed_power_densityv, title+"_density")
            self.write_slice_to_table(voxel_absorbed_powerv,title+"_power")
        #print("write_slice_to_table ",time()-tstart)
        
        # Problem here with multiple layers
        total_integrated_absorbed_power=self.total_integrated_power(voxel_absorbed_powerv)        

        integrated_power_after_region=self.integrated_source_power(region_filtered_fluxv)

        #print("final power integrals ",time()-tstart)
        
        #print("line 275\twriting files")
        #print(s_flux[self.vd-1][self.hd-1][3000:3005])
        tend=time()
        dt=tend-tstart
        
        s+="Integrated power absorbed in the object: "+str(total_integrated_absorbed_power)+" W\n"
        s+="Integrated power transmitted through the object: "+str(integrated_power_after_region)+" W\n"

        s+= "Integrated power error: "+str(integrated_power_after_filtering - total_integrated_absorbed_power - integrated_power_after_region)+" W\n"
        
        s+="Elapsed time: "+str(dt)+" s\n"
        
        #temporary samples
        
        f=open("heatbump_result.txt","w")
        f.write(s)
        f.close()
        print(s)
        sleep(2.0)
        if self.NUKE_JOBS==True:
            rmtree(".\\job")
        
    def integrated_source_power(self,s_flux):
        """Finds total power in region, triple integral of power flux. 3d->scalar. Only uses interior points for power calculation. Exterior points used for interpolation correction"""

        if self.print_matrix_sums:
            print_sum_matrix(s_flux, 'integrated_source_power s_flux')

        intpow=0
        ea=self.generate_energy_axis()
        areas=self.rect_areas()
        full_area=(self.h/self.hd)*(self.v/self.vd) #area of a complete center cell
        for i in range(0,len(s_flux)):
            for j in range(0,len(s_flux[0])):
                for m in range(0, len(ea)):
                    intpow+=(s_flux[i][j][m]*ea[m]*1.60217646E-19)*(areas[i][j]/full_area)#the dA element of the integral

        if self.print_matrix_sums:
            print_number(intpow, 'integrated_source_power intpow')

        return intpow
    
    
    def patch_flux(self,x_offset=0,y_offset=0, phase=0, jobdir=''):
        """Runs ws() and us() depending upon the source, outputs intensity data vector"""
        #should i keep the ws and build matrix functions in wig and und, or move them here? decisions, decisions. resolved, moved to backend.
        if self.source=="wig":
            return self.ws(x_offset,y_offset, phase, jobdir)
        elif self.source=="und":
            return self.us(x_offset,y_offset, phase, jobdir)
        else: 
            raise NameError("unknown source")
        return
    
    def region_filtered_flux(self,s_flux):
        """Finds the flux through the filtered region, accounts for materials"""

        if self.print_matrix_sums:
            print_sum_matrix(s_flux, 'region_filtered_flux s_flux')

        #Strong Feeling there is a big fat bug somewhere around here
        thickness=sum(self.thickness) #in cm

        mat=self.mat        
        ea=self.generate_energy_axis()        
        
        reg_flux=matchdim(s_flux)
        
        f=open("mu_data\\"+mat+".pkl","rb")
        edata=pickle.load(f)
        f.close()
        elem_energy=[i[0] for i in edata]
        elem_flux=[i[1] for i in edata]
        #you knew it, absurdly slow code below. Really no way to get around it though. Filtering sucks, O(n^3)
        for i in range(0, len(s_flux)):
            for j in range(0,len(s_flux[0])):
                for k in range(0, len(ea)):
                    reg_flux[i][j][k]=s_flux[i][j][k]*math.exp(-1*thickness*mu3(elem_energy,elem_flux,ea[k]))
        
        if self.print_matrix_sums:
            print_sum_matrix(s_flux, 'region_filtered_flux reg_flux')
            
        return reg_flux
    
    def run_xop(self, xop_pgm, x_offset=0,y_offset=0, phase=0, jobdir=''):
        """writes the matrix, runs xop program, and processes the result"""
        if phase==1:
            #Builds matrix/.inp file 
            if xop_pgm == 'us':
                matrix=self.buildusmatrix(x_offset,y_offset)
            elif xop_pgm == 'ws':
                 matrix=self.buildwsmatrix(x_offset,y_offset)
                 
            s=""
            for i in matrix: 
                s+=",".join(i)
                s+="\n"
            
            #writes data into .inp file
            f=open(jobdir+'\\'+ xop_pgm + ".inp", "w")
            f.write(s)
            f.close()
            return
        
        # runs xop
        #   self.XOP_Processes holds the popen objects of the running processes
        #   self.XOP_run_at_one_time is the maximum number to run at once

        if phase==2:
            
            if jobdir != 'waitforall':
                # Update list of processes
                self.update_process_list()
                # We wait for an open slot to process the next one
    
                jobs_remaining = self.jobs_to_run - self.jobs_completed
    
                if jobs_remaining <= (self.XOP_run_at_one_time * self.jobs_overcommit_at_end):
                    max_to_run = self.XOP_run_at_one_time * self.jobs_overcommit_at_end
                else:
                    max_to_run = self.XOP_run_at_one_time
    
                while(len(self.XOP_Processes) >= max_to_run):  # Consider a timeout
                    sleep(0.25)
                    self.update_process_list()
                    
                p=subprocess.Popen(self.xop_path+xop_pgm+".exe", cwd=jobdir)
                p.jobdir = jobdir
                print('Starting %s for jobdir %s' % (xop_pgm, jobdir))
                self.XOP_Processes.append(p)
                
            else:  # Wait for all jobs to finish
                while(len(self.XOP_Processes) > 0):  # Consider a timeout
                    sleep(0.25)
                    self.update_process_list()
                return
        
        #reads results
        if phase == 3:
            #read output from each job's .out file
            xop_data=[]
            f2=open(jobdir+'\\'+xop_pgm+".out","r")
            for i, line in enumerate(f2):
                if (xop_pgm == 'us' and i>=23) or (xop_pgm == 'ws' and i>=18):
                    g=line[0:26].split()
                    xop_data.append(float(g[1]))
            f2.close()
            return xop_data 

        return "Invalid phase"
    
    def slice_transmission(self):
        """Finds the amount of flux that passes though a each slice. slice_t[i][j] j direction: energies, i direction: thickness 2d. Energy divisions are locked into 5000""" 
        slice_t=[]
        #returns mu values for particular element (y values). Equivalent of filter_flux for region
        f=open("mu_data\\"+self.mat+".pkl","rb")
        mu_data=pickle.load(f)
        f.close()
        mu_raw=[i[1] for i in mu_data]
        for layer in self.thickness:
            #locked into scan parameter of 500 min 100000 max 5000 div
            #slow as hell. is there a trend here?
            slice_t.append([math.exp(-1*layer*k) for k in mu_raw])
            
        if self.print_matrix_sums:
            print_sum_matrix_by_layer(slice_t, 'slice_transmission slice_t')
            if len(self.thickness) > 1:
                print_sum_matrix(slice_t, 'slice_transmission slice_t')
            
        return slice_t
    
    def source_flux(self):
        """finds the energy flux in a region, through multiple calls to xop. ->3d"""
        if self.LIP==True:
            s_flux=cell2(self.hd+2,self.vd+2)
            uncorrected_flux=cell2(self.hd+2,self.vd+2)
        else:
            s_flux=cell2(self.hd,self.vd)
            uncorrected_flux=cell2(self.hd,self.vd)
        
        pc=self.rect_centers()
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
                x_offset=pc[i][j][0]
                y_offset=pc[i][j][1]
                jobdir = jobdirroot + '\\' + str(i) + '-' + str(j)
                if not path.exists(jobdir):
                    makedirs(jobdir)
                self.patch_flux(x_offset,y_offset, 1, jobdir)

        # Phase 2 - Run XOP programs, multi-processing           
        for i in range(0,ilimit):
            for j in range(0,jlimit):
                x_offset=pc[i][j][0]
                y_offset=pc[i][j][1]
                jobdir = jobdirroot + '\\' + str(i) + '-' + str(j)
                self.patch_flux(x_offset,y_offset, 2, jobdir)

        self.patch_flux(0, 0, 2, 'waitforall')  # wait for remaining jobs to finish              

        # Phase 3 - Read output files from XOP programs and incorporate data            
        for i in range(0,ilimit):
            for j in range(0,jlimit):
                x_offset=pc[i][j][0]
                y_offset=pc[i][j][1]
                jobdir = jobdirroot + '\\' + str(i) + '-' + str(j)
                s_flux[i][j]=self.patch_flux(x_offset,y_offset, 3, jobdir)
                uncorrected_flux[i][j]=s_flux[i][j]
                
                assert depth(s_flux)==3
                if self.LIP:
                    assert ilimit==self.vd+2
                    assert jlimit==self.hd+2 
                else:
                    assert ilimit==self.vd 
                    assert jlimit==self.hd 
                assert ilimit==len(s_flux)
                assert jlimit==len(s_flux[0])
                assert len(ea)==len(s_flux[0][0])

                for k in range(0,len(ea)):
                    #convert from bandpass to raw flux(ph/s/.1%BW -> ph/s)
                    #GOTCHA! Bug, i found you!
                    s_flux[i][j][k]*=1000*dE/ea[k]
                    #s_flux[i][j][k]=s_flux[i][j][k]*1000*dE/ea[k]
        #self.write_uncorrected_flux(uncorrected_flux)

        if self.print_matrix_sums:
            print_sum_matrix(s_flux, 'source_flux s_flux')
        
        return s_flux     

    def total_integrated_power(self,v_power):
        """Find total power in object"""
        
        #index limits
        assert depth(v_power)==3
        
        if self.print_matrix_sums:
            print_sum_matrix_by_layer(v_power, 'total_integrated_power v_power')
            if len(self.thickness) > 1:
                print_sum_matrix(v_power, 'total_integrated_power v_power')


        areas=self.rect_areas()
        full_area=(self.h/self.hd)*(self.v/self.vd)
        total_integrated_power=0
        sumthick=sum(self.thickness)
        
        klimit=len(v_power)
        ilimit=len(v_power[0])
        jlimit=len(v_power[0][0])

        for k in range(0,klimit):
            for i in range(0,ilimit):
                for j in range(0,jlimit):
                    #total_integrated_power+=v_power[k][i][j]*(areas[i][j]/full_area)*self.thickness[k]/sumthick #dV element
                    total_integrated_power+=v_power[k][i][j]*(areas[i][j]/full_area) ### *self.thickness[k]/sumthick ### TESTING FIX
                    #print(v_power[k][i][j], areas[i][j], full_area, self.thickness[k], sumthick, total_integrated_power)
                    
        #This takes the sum of all elements in total_integrated_power, equivalent to the above triple integral.
        #Inaccurate, does not account for area.
        #total_integrated_power=sum(sum(sum(v_power,[]),[]))
        
        if self.print_matrix_sums:
            print_number(total_integrated_power, 'total_integrated_power returns')

        return total_integrated_power
    
    def update_process_list(self):
        new_process_list = []
        for p in self.XOP_Processes:
            if p.poll() == None:
                new_process_list.append(p)
            else:
                print('Ending jobdir %s code %s' % (p.jobdir, p.poll()))
                self.jobs_completed += 1
                pass   # Process if error
        self.XOP_Processes = new_process_list
    
    def us(self,x_offset=0,y_offset=0,phase=0, jobdir=""):
        """writes the matrix to us.inp, runs ws.exe, and processes the result"""
        return self.run_xop('us', x_offset, y_offset, phase, jobdir)
    
    def voxel_absorbed_flux(self,s_flux, slice_t):
        """Finds the power flux from source and transmission through each layer. s_flux=3d, slice_t=2d"""

        if self.print_matrix_sums:
            print_sum_matrix(s_flux, 'voxel_absorbed_flux s_flux')
            print_sum_matrix(slice_t, 'voxel_absorbed_flux slice_t')
        
        #This is a troublesome, fickle beast (when processing undulators)
        voxel_impinging_flux=matchdim(slice_t)            #4d, eventually
        assert len(slice_t)==len(voxel_impinging_flux)
        #calculate cumulative transmission through each layer
        
        cumulative_transmission=matchdim(slice_t)             #2d
        cumulative_transmission[0]=matchdim(slice_t[0],1)
        
        slice_absorption=deepcopy(slice_t)
        assert len(slice_absorption)==len(slice_t)==len(voxel_impinging_flux)
        #absorption+transmission=1, 2d
        for i in range(0, len(slice_t)):
            for j in range(0, len(slice_t[0])):
                slice_absorption[i][j]=1-slice_t[i][j]

        if self.print_matrix_sums:
            print_sum_matrix(slice_absorption, 'voxel_absorbed_flux slice_absorption')

        #print("slice_absorption, slice_t:")
        #print(slice_absorption, slice_t)
        
        for i in range(0,len(self.thickness)):
            j=i
            temp_transmission=matchdim(slice_t[0],1)
            
            while j>0:
                assert len(temp_transmission)==len(slice_t[j])
                #temp_transmission=mult(temp_transmission,slice_t[j]) 
                temp_transmission=mult(temp_transmission,slice_t[j-1])  ### TESTING FIX
                j-=1
            cumulative_transmission[i]=temp_transmission

        if self.print_matrix_sums:
            print_sum_matrix_by_layer(cumulative_transmission, 'voxel_absorbed_flux cumulative_transmission')
            if len(self.thickness) > 1:
                print_sum_matrix(cumulative_transmission, 'voxel_absorbed_flux cumulative_transmission')
        
        #print("\ncumulative_transmission:")
        #print(cumulative_transmission)
        
        for k in range(0, len(slice_t)):
            temp_surface=deepcopy(s_flux)
            #for i in range(0,len(s_flux[0])):
            #    for j in range(0, len(s_flux)-1):
            for i in range(0,len(s_flux)):         ### TESTING FIX
                for j in range(0, len(s_flux[0])): ### TESTING FIX
                    #temp_surface[i][j]=mult(s_flux[i][j],cumulative_transmission[k])
                    temp_surface[i][j]=mult(temp_surface[i][j],cumulative_transmission[k])  ### TESTING FIX
            voxel_impinging_flux[k]=temp_surface
        
        if self.print_matrix_sums:
            print_sum_matrix_by_layer(voxel_impinging_flux, 'voxel_absorbed_flux voxel_impinging_flux')
            if len(self.thickness) > 1:
                print_sum_matrix(voxel_impinging_flux, 'voxel_absorbed_flux voxel_impinging_flux')

        #print("\nvoxel_impinging_flux")
        #print(voxel_impinging_flux)
        voxel_absorbed_flux=matchdim(voxel_impinging_flux)
        
        assert depth(slice_absorption)==2
        assert depth(voxel_impinging_flux)==4
        
        
        for k in range(0, len(voxel_impinging_flux)):
            #temp_surface 3d, initialize as empty 2d
            #temp_surface=cell2(len(voxel_impinging_flux[0]),len(voxel_impinging_flux[0][0]))
            temp_surface=cell2(len(voxel_impinging_flux[0][0]),len(voxel_impinging_flux[0]))  #### TESTING FIX
            for i in range(0,len(voxel_impinging_flux[0])):
                for j in range(0,len(voxel_impinging_flux[0][0])):
                    #print([len(voxel_impinging_flux),len(voxel_impinging_flux[k]),len(voxel_impinging_flux[k][i]),len(voxel_impinging_flux[k][i][j])])
                    #print([len(slice_absorption),len(slice_absorption[0])])
                    #assert len(voxel_impinging_flux[k][i][j])==len(slice_absorption[k])
                    temp_surface[i][j]=[voxel_impinging_flux[k][i][j][m]*slice_absorption[k][m] for m in range(0, len(slice_absorption[k]))]
            voxel_absorbed_flux[k]=temp_surface
        #print("\nvoxel_absorbed_flux")
        #print(voxel_absorbed_flux) 
        #4d

        if self.print_matrix_sums:
            print_sum_matrix_by_layer(voxel_absorbed_flux, 'voxel_absorbed_flux voxel_absorbed_flux')
            if len(self.thickness) > 1:
                print_sum_matrix(voxel_absorbed_flux, 'voxel_absorbed_flux voxel_absorbed_flux')
            
        return voxel_absorbed_flux

    def voxel_absorbed_power_density(self,v_power,slice_volumes):
        """Divide power by volume to get power density. 3d->3d"""
        assert matchdim(v_power)==matchdim(slice_volumes)
        
        if self.print_matrix_sums:
            print_sum_matrix_by_layer(v_power, 'voxel_absorbed_power_density v_power')
            if len(self.thickness) > 1:
                print_sum_matrix(v_power, 'voxel_absorbed_power_density v_power')

            print_sum_matrix_by_layer(slice_volumes, 'voxel_absorbed_power_density slice_volumes')
            if len(self.thickness) > 1:
                print_sum_matrix(slice_volumes, 'voxel_absorbed_power_density slice_volumes')
       
        v_power_density=matchdim(v_power)
        
        for k in range(0,len(v_power)):
            for j in range(0,len(v_power[0])):
                for i in range(0,len(v_power[0][0])):
                    #v_power_density[k][i][j]=v_power[k][i][j]/slice_volumes[k][i][j]
                    v_power_density[k][j][i]=v_power[k][j][i]/slice_volumes[k][j][i]  ### TESTING FIX
                    
        if self.print_matrix_sums:
            print_sum_matrix_by_layer(v_power_density, 'voxel_absorbed_power_density v_power_density')
            if len(self.thickness) > 1:
                print_sum_matrix(v_power_density, 'voxel_absorbed_power_density v_power_density')
        
        return v_power_density
        
    def voxel_flux_to_power(self,v_flux):
        """Transforms the power flux load into power. 4d->3d"""
        
        if self.print_matrix_sums:
            print_sum_matrix_by_layer(v_flux, 'voxel_flux_to_power v_flux')
            if len(self.thickness) > 1:
                print_sum_matrix(v_flux, 'voxel_flux_to_power v_flux')
       
        #v_flux[slice][y][x][energy]
        v_power=matchdim(v_flux)
        ea=self.generate_energy_axis()
        #initialize index limits
        klimit=len(self.thickness) #thickness, z
        #i:y
        #j:x
        if self.LIP==True:
            ilimit=self.vd+2
            jlimit=self.hd+2
        else:
            ilimit=self.vd
            jlimit=self.hd
        mlimit=len(ea)             #energy
        #dE=self.ea[2]-self.ea[1]
        
        #massive time draining calculations! Woohoo!
        for k in range(0,klimit):
            for j in range(0,jlimit):
                for i in range(0, ilimit):
                    for m in range(0,mlimit):
                        v_power[k][i][j][m]=v_flux[k][i][j][m]*ea[m]*1.60217646e-19
                        
        #int_v_power=cell3(ilimit,jlimit,klimit)
        int_v_power=cell3(jlimit,ilimit,klimit)  ### TESTING CODE
        
        #Quadruple integral!
        for k in range(0,klimit):
            for j in range(0,jlimit):
                for i in range(0,ilimit):
                    temp_power=0
                    for m in range(0,mlimit):
                        temp_power+=v_power[k][i][j][m]
                    #There seems to be a factor of about 4 between the true power/density and the heatbump-produced.
                    int_v_power[k][i][j]=temp_power #/3.985473468
                    
        if self.print_matrix_sums:
            print_sum_matrix_by_layer(int_v_power, 'voxel_flux_to_power int_v_power')
            if len(self.thickness) > 1:
                print_sum_matrix(int_v_power, 'voxel_flux_to_power int_v_power')
        
        return int_v_power
        
    def write_uncorrected_flux(self,uncorrected_flux):
        """writes each power slice to the file output.csv. 3d->file"""
        #There might be an error here in the cube writing to file, y instead of z split.
        #screw it, 4d array to 3d file doesn't work well.
        st=""
        u_flux=uncorrected_flux
        
        #voxel dimensions
        zlen=len(u_flux)
        ylen=len(u_flux[0])
        xlen=len(u_flux[0][0])
        
        for k in range(0,zlen):
            s=""
            power_temp=cell2(xlen,ylen)        
            for i in range(0,ylen):
                for j in range(0,xlen):
                    #flipdim unnecesary
                    power_temp[i][j]=u_flux[k][i][j]
            
            
            power_temp_s=[list(map(str,i)) for i in power_temp]
            
            s+="\n".join([",".join(i) for i in power_temp_s])
            
            
            if k==0:
                st+=s
            else:
                st+="\n\n"+s
      
        f=open("raw_flux.csv","w")
        f.write(st)
        f.close()
        
        f2=open("pickle\\raw_flux.pkl","wb")
        pickle.dump(u_flux,f2)
        f2.close()
    
    def write_slice_to_table(self,voxel_absorbed_power_density,title):
        """writes each power slice to the file output.csv. 3d->file"""
        #There might be an error here in the cube writing to file, y instead of z split.
        st=""
        vd=voxel_absorbed_power_density
        
        #axis setup
        pc=self.rect_centers()
        #Bug Fix:
        #If the xdiv or ydiv values were 1, the program would blow up. this was due to i[1] rather than i[0]
        #X axis output fixed, improper hr definition
        hr=[0]+self.rect_center_x()+[self.h]
        vr=[0]+self.rect_center_y()+[self.v]

        if title=="":
            title="output"
        
        #voxel dimensions
        zlen=len(vd)
        ylen=len(vd[0])
        xlen=len(vd[0][0])
        
        for k in range(0,zlen):
            #thickness loop
            s=""
            power_temp=cell2(xlen,ylen)        
            for i in range(0,ylen):
                for j in range(0,xlen):
                    #flipdim unnecesary
                    power_temp[i][j]=vd[k][i][j]
            
        
            #vertical zero padding
            for i in range(0,ylen):
                power_temp[i].insert(0,0)
                power_temp[i].append(0)
                
        
            #horizantal zero padding
            power_temp.append(cell1(xlen+2))
            power_temp.insert(0,cell1(xlen+2))
            
            if (len(power_temp) < len(vr)):
                print('len(power_temp) >= i', k, len(power_temp), i, len(vr))

            for i in range(0,len(vr)):
                power_temp[i].insert(0,vr[i])  ### BUG
            
            hr.insert(0,10*self.thickness[k])
            power_temp.insert(0,hr)
            power_temp_s=[list(map(str,i)) for i in power_temp]
            
            s+="\n".join([",".join(i) for i in power_temp_s])
            
            
            if k==0:
                st+=s
            else:
                st+="\n\n"+s
            del hr[0]
        outputfile="heatbump_output\\"+title+".csv"
        
        outputfile_d=path.dirname(outputfile)
        
        if not path.exists(outputfile_d):
            makedirs(outputfile_d)
        
        f=open(outputfile,"w")
        f.write(st)
        f.close()

    def ws(self,x_offset=0,y_offset=0,phase=0,jobdir=""):
        return self.run_xop('ws', x_offset, y_offset, phase, jobdir)
        
if __name__=="__main__":
    print("Please, don't run me from here! Run heatbump through heatbump.py")