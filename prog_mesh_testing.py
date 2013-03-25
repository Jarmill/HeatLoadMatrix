#===============================================================================
# This code is designed to test and develop the progressive mesh code.
# These functions will be transferred to a format compatible with heat_load_matrix
# The testing function will be of the form k(i) E^((x/a)^2 + (y/b)^2) (gaussian) for each energy value
# This roughly approximates the shape of the actual beam profile, and is much easier on system resources.
# Right now, a "stupid mesh" is used, in which the splitting function works for as many times as there
# are levels, without regard for distributions of additional points or maxumum grid sizes. 
#===============================================================================
from rect_partition import pc
from math import exp, log
import os
from basic_functions import depth, matchdim, cell2, cell3
import _pickle as pickle
from shutil import rmtree
class gauss_mesh(pc):
    def __init__(self, h, v, hd, vd):
        """set up parameters for the mesh"""
        self.h=h
        self.v=v
        self.hd=hd
        self.vd=vd
        self.d=.01
        self.LIP=True
        self.thickness=[1]
        self.title="gauss testing"
        self.rect_setup()
        self.mesh_level=0
        self.ea=[500+(100000-500)/(5000)*i for i in range(5000)]
        self.x_tolerance=20.0
        self.y_tolerance=30.0
    def gauss(self, x, y, energy):
        """The value of the 'flux' at the specific point"""
        return log(energy, 10)*exp(-(x/8)**2-(y/1.2)**2)
    
    def source_flux(self, old_flux=[]):
        """Find flux at points that have not already been evaluated"""
        if old_flux==[]:
            s_flux=self.blank()
        else: s_flux=old_flux
        pc=self.rect_centers()
        dimensions=self.rect_centers()
        ea=self.ea
        dE=ea[1]-ea[0]
        jobdirroot=".\\job"
        #Phase 1 - generate folders------------------------------------------------------------------------------ 
        for i in range(0, len(s_flux)):
            for j in range(0, len(s_flux[0])):
                if depth(s_flux[i][j])==0:
                    jobdir=jobdirroot+"\\"+str(i)+'-'+str(j)
                    if not os.path.exists(jobdir):
                        os.makedirs(jobdir)
        #Phase 2 - run gauss on each folder, create "out.pkl" on each------------------------------------------------------------------------------ 
        samp_points=[x for x in list(os.walk(".\\job"))[0][1]]
        for p in samp_points:
            i=int(p[0])
            j=int(p[2])
            filedir=jobdirroot+"\\"+p+"\\"
            self.gen_flux(pc[i][j][0], pc[i][j][1], filedir, dimensions[i][j][0], dimensions[i][j][1])
        #Phase 3 - read in  "out.pkl" for each point------------------------------------------------------------------------------
        for p in samp_points:
            i=int(p[0])
            j=int(p[2])
            filename=jobdirroot+"\\"+p+"\\out.pkl"
            with open(filename, "rb") as f2:
                s_flux[i][j]=pickle.load(f2)
            # for m in range(0, len(ea)):
            #     s_flux[i][j][m] *= 1000 * dE / ea[m]
        
        if os.path.exists("job"): 
            rmtree("job")
        
        return s_flux
    
    def gen_flux(self, x_offset, y_offset, filedir, x_len, y_len):
        """replicates functionality of patch_flux, generates flux at each point"""
        with open(filedir+"\\out.pkl", "wb") as f:
            flist=[self.gauss(x_offset, y_offset, energy) for energy in self.ea]
            pickle.dump(flist, f)
            
    
    def read_flux(self, filename):
        """temporary, only for reading flux of format in gauss"""
        with open(filename, "rb") as f:
            l=pickle.load(f)
        return l
    
    def voxel_flux_to_power(self, v_flux):
        """Transforms the power flux load into power. 4d->3d"""

        # v_flux[slice][y][x][energy]
        v_power=matchdim(v_flux)
        ea=self.ea
        dE=ea[1]-ea[0]
        # initialize index limits
        klimit=len(self.thickness)  # thickness, z
        # i:y
        # j:x
        klimit=len(v_flux)
        ilimit=len(v_flux[0])
        jlimit=len(v_flux[0][0])
        # mlimit=len(ea)
        # dE=self.ea[2]-self.ea[1]
        
        # massive time draining calculations! Woohoo!
        # Not used in gauss testing!
        """
        for k in range(0, klimit):
            vk = v_flux[k]
            for i in range(0, ilimit):
                vki = vk[i]
                for j in range(0, jlimit):
                    vkij = vki[j] 
                    for m in range(0, mlimit):
                        v_power[k][i][j][m] = vkij[m] * ea[m] * 1.60217646e-19
        """             
        # int_v_power=cell3(ilimit,jlimit,klimit)
        int_v_power=cell3(jlimit, ilimit, klimit)  # ## TESTING CODE
        
        # Quadruple integral!
        for k in range(0, klimit):
            vk=v_flux[k]
            for i in range(0, ilimit):
                vki=vk[i]
                for j in range(0, jlimit):
                    vkij=vki[j]
                    temp_power=0
                    mlimit=len(vkij)
                    for m in range(0, mlimit):
                        temp_power+=vkij[m]*dE
                    int_v_power[k][i][j]=temp_power
        return int_v_power
    
    def find_split(self, pdiff, tolerance):
        """Determines how many times to split a cell"""
        return round(log(pdiff, tolerance))
    
    def rect_flux_split(self, s_flux, s_power):
        """this is the splitting function, how the progressive mesh works"""
        # shitload of inefficient array insertions to follow.
        xlen=len(s_power[0])
        ylen=len(s_power)
        dim=self.dimensions
        # px = percent change
        px=[[-(s_power[i][j+1]-s_power[i][j])/s_power[i][j+1]*100 for j in range(xlen-1)] for i in range(ylen)]
        py=[[-(s_power[i+1][j]-s_power[i][j])/s_power[i+1][j]*100 for j in range(xlen)] for i in range(ylen-1)]
        """
        domy=[max(i) for i in py]
            
        for i in range(xlen-1):
            domx[i]=max([px[j][i] for j in range(ylen-1)]) 
        
        x_split=[self.find_split(i, self.x_tolerance) for i in domy]
        y_split=[self.find_split(i, self.y_tolerance) for i in domx]
        """
        x_split=[1]*(xlen-1)
        y_split=[1]*(ylen-1)
        print("X split:\n", x_split, "\nY split:\n", y_split)
        # rest of code goes here
        
        #Split on x axis------------------------------------------------------------------------------
        x_index=0
        for x_control in range(xlen-1):
            curr_split_x=x_split[x_control]
            new_par_dist=(self.xpar[x_index+1]-self.xpar[x_index])/(curr_split_x+1)
            par_initial=self.xpar[x_index]
            for i in range(curr_split_x):
                for j in s_flux:
                    j.insert(x_index, 0)
                self.xpar.insert(x_index, par_initial+new_par_dist*(i+1))
                x_index+=1
            x_index+=1
        
        #Split on y axis------------------------------------------------------------------------------ 
        y_index=0
        for y_control in range(ylen-1):
            curr_split_y=y_split[y_control]
            new_par_dist=(self.ypar[y_index+1]-self.ypar[y_index])/(curr_split_y+1)
            par_initial=self.ypar[y_index]
            listlen=len(s_flux[0])
            for i in range(curr_split_y):
                s_flux.insert(y_index, [0]*listlen)
                self.ypar.insert(y_index, par_initial+new_par_dist*(i+1))
                y_index+=1
            y_index+=1
            
        # print(self.voxel_flux_to_power([s_flux])[0])
        # also generate all areas/dimensions/centers
        self.rect_param()
        # return modified source flux
        return s_flux      
        
        
    def integrated_total_power(self, s_power):
        """Finds total power in region, triple integral of power flux. 3d->scalar. Only uses interior points for power calculation. Exterior points used for interpolation correction"""
        intpow=0
        full_area=(self.h/self.hd)*(self.v/self.vd)  # area of a complete center cell
        for i in range(0, len(s_power)):
            for j in range(0, len(s_power[0])):
                intpow+=s_power[i][j]*self.areas[i][j]
        return intpow

    
    def run_gauss(self):
        jobdirroot=".\\job"
        if not os.path.exists("job"):
            os.makedirs("job")
        
        s_flux=self.source_flux()
        s_power=self.voxel_flux_to_power([s_flux])[0]
        s_flux=self.rect_flux_split(s_flux, s_power)
        """
        while self.mesh_level>0:
            s_flux=self.rect_flux_split(s_flux, s_power)
            # find a way to handle filtering, hopefully already done.
            # maybe incorporate filtering into s_flux definition.
            s_flux=self.source_flux(s_flux)
            s_power=self.voxel_flux_to_power([s_flux])[0]
            self.mesh_level-=1
    
        if os.path.exists("job"):
            os.rmtree("job")
        """
        return s_power

if __name__=="__main__":
    g=gauss_mesh(17, 4, 4, 4)
    gpower=g.run_gauss()
    print(gpower)
    print(g.integrated_total_power(gpower))
