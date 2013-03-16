# The big import block
# basic algorithms/operations
from basic_functions import  cell1, cell2, cell3, mult, mu3, depth, matchdim, print_sum_matrix_by_layer, print_number, print_sum_matrix
import math
from time import time, sleep
from copy import deepcopy
# reading and writing data
import _pickle as pickle
import json
# grid functionality
import rect_partition
# subprocess modules
from multiprocessing import cpu_count
import subprocess
from os import path, makedirs
# THE NUCLEAR OPTION
from shutil import rmtree
import gc
from PyQt4 import QtCore, QtGui


"""
Always remember to check that total power=power absorbed+power transmitted.
If it does not, sign of a deep error in computation. now abbreviated as p=a+t

Version 1.0
The centipede has been caught! This error turned values of source_flux from
10^12 --> 10^-21, due to a "=" instead of a "==" in region_filtered flux

Version 1.1
Interpolation guard is now implemented. The previous implementation did not
work well, working on now. Created a new class and rectangle handling function
to deal with this error.

Version 1.2
A speed boost was added while filtering (instead of using a sequential search
to find mu values, a binary search is now used) cut processing time in python
from 300s to 5s

Version 2.0
Multiprocessing added. This update later included "overdrive", where if half
the cores are finished, a new dispatch occurs. Instead of time being cut by a
factor of N, now it is cut by 1.5N (N=number of cores)

There were a series of numerical errors, which included large errors in p=a+t,
when multiple slices were implemented. There was also a difference in power
values when the slices were (100,10)mm,(110)mm,(10,100)mm, or (10)mmx11.
This was due to reference errors, and fixed by using deepcopy
The write_slice_to_table function was rehauled, in order to implement changes
as due to rectangle_grid.
There are still some index naming errors, these are of low priority and will
be fixed in next release.
Inner loop optimization has been added. This cuts down the time through less
indexing.
Memory errors are present, for a 102x102 matrix (100x100 with lip), the
source_flux array is about 396 MB. Broke my laptop. Need big machine.

Version 2.1
There were several unnecessary deepcopies of s_flux that have been removed.
In the filter_flux function, s_flux gets edited and destroyed, cannot be recovered.
Attempted numpy handling, does not work on laptop. Will try harder, had to use
unofficial binaries.
Fixed a series of bugs, finally got good results. The density is finally a smooth
function, while the power is properly discontinuous. This was due to the composition
of two bugs, not changing the width and height of cells in build?matrix, and a series
of other computation errors in s_flux.

Version 2.1.2
Mathematica output
Fixing the "both" dialog in adv
other optimizations/tests

Version 2.5
Importing and Exporting run data
Importing and Exporting source data
The workflow ui has been added
Most pickle data have been replaced with json format

Version 3.0
Adding the Abort Button
The GUI and the Backend run on separate QThreads
Progress bar implementation

Future Features:
Preserving the index convention for the grid, without using the transpose cheat
Progressive meshing
Inclination formula
Bending magnet supprot
"""

class UserAbortException(Exception):
    pass

class Back(QtCore.QThread, rect_partition.pc2):
    """This class contains all the misc functions that allow heatloadmatrix to run. The main event is heat_load_matrix()"""
    def __init__(self):
        super(Back, self).__init__()
        self.back_values()
        self.abort=False

    def __del__(self):
        self.wait()

    def updateStatus(self, section, pctdoneinsection, msg=""):

        QtGui.qApp.processEvents(QtCore.QEventLoop.AllEvents)

        if self.abort:
            raise UserAbortException()

        if section==1:
            pctdone=0+(pctdoneinsection*0.10)
        elif section==2:
            pctdone=10+(pctdoneinsection*0.65)
        else:
            pctdone=75+(pctdoneinsection*0.25)

        # print("updateStatus(" + str(section) + "," + str(pctdoneinsection) + ") --> " + str(pctdone) + "%")

        self.emit(QtCore.SIGNAL("progvalue"), pctdone)

        if msg!="":
            self.emit(QtCore.SIGNAL("update(QString)"), msg)

        # self.yieldCurrentThread()

    def back_values(self):
        """pseudoglobal values. These are initialized as part of WDialog and UDialog's __init__() method, to avoid the diamond of death"""

        # advanced  values
        advf=open("pickle\\adv.json", "r")
        adv=json.load(advf)
        advf.close()
        
        # region values
        freg=open("pickle\\reg.json", "r")
        reg=json.load(freg)
        freg.close()
        
        # run parameters
        frun=open("pickle\\run.json", "r")
        run=json.load(frun)
        frun.close()
        
        # user submitted filters
        ff=open("pickle\\flt.json", "r")
        flt_list_old=json.load(ff)
        ff.close()
        self.flt_list=[i for i in flt_list_old if i[0]!=None and i[1]!=None]
        # debugging
        # self.print_matrix_sums = True
        self.print_matrix_sums=False
        
        # multiprocessing parameters
        self.XOP_Processes=[]
        self.XOP_run_at_one_time=cpu_count()
        
        self.h=float(reg["xlen"])
        self.v=float(reg["ylen"])
        self.hd=int(reg["xdiv"])
        self.vd=int(reg["ydiv"])
        self.thickness=[float(i) for i in reg["thickness"]]
        
        # scan values
        self.estart=int(adv["estart"])
        self.eend=int(adv["eend"])
        self.ediv=int(adv["ediv"])
        self.xint=int(adv["xint"])
        self.yint=int(adv["yint"])
        
        # other        
        self.source=run["source"]
        
        # energy axis(default)
        self.ea=self.generate_energy_axis()
        
        # run (main) parameters
        self.pout=run["power"]
        self.mat=run["mat"]
        self.dist=run["dist"]
        self.deg=run["deg"]
        self.mesh=run["mesh"]
        if run["title"]=="": self.title="output"
        else: self.title=run["title"]
        
        # intrinsic parameters DO NOT TOUCH! Only for undulators
        self.mode=int(adv["mode"])
        self.method=int(adv["method"])
        self.harmonic=int(adv["harmonic"])
        self.nphi=float(adv["nphi"])
        self.nalpha=float(adv["nalpha"])
        self.calpha2=float(adv["calpha2"])
        self.nomega=float(adv["nomega"])
        self.comega=float(adv["comega"])
        self.nsigma=float(adv["nsigma"])
        
        # xop path
        self.xop_path=run["xop_path"]
        
        # source parameters
        if self.source=="und":
            und=json.load(open("pickle\\und.json", "r"))
            self.energy=und["energy"]
            self.current=und["current"]
            self.period=und["period"]
            self.num=und["num"]
            self.sigx=und["sigx"]
            self.sigy=und["sigy"]
            self.sigx1=und["sigx1"]
            self.sigy1=und["sigy1"]
            self.kx=und["kx"]
            self.ky=und["ky"]
        
        elif self.source=="wig":
            wig=json.load(open("pickle\\wig.json", "r"))
            self.energy=wig["energy"]
            self.current=wig["current"]
            self.period=wig["period"]
            self.num=wig["period"]
            self.kx=wig["kx"]
            self.ky=wig["ky"]
        
        # Interpolation guard/rectangle handling
        # interpolation guard on
        
        self.LIP=True  # TURN ON AFTER TESTING!
        
        # intepolation guard length
        self.d=10**-6
        # set up rectangle handling
        self.rect_setup()
        
        # THE NUCLEAR OPTION. Do you want to enable rmtree to wipe the "job" folder after each run?
        self.NUKE_JOBS_AT_END=True
        
        # output to mathematica
        self.MATHEMATICA_OUTPUT=False
        self.mathematica_sampling=[0, 111, 222, 333, 444, 555, 666, 999, 1999, 2999, 3999, 4999]

        
    def buildusmatrix(self, x_offset=0, y_offset=0, x_dim=0, y_dim=0):
        """Builds the xop-formatted undulator matrix from user-entered values"""
        xpos=str(x_offset)
        ypos=str(y_offset)
        xdim=str(x_dim)
        ydim=str(y_dim)

        matrix=[[str(self.title), "0", "0", "0", "0", "0", "0"], \
                [str(self.energy), str(self.current), "0", "0", "0", "0", "0"], \
                [str(self.sigx), str(self.sigy), str(self.sigx1), str(self.sigy1), "0", "0", "0"], \
                [str(self.period), str(self.num), str(self.kx), str(self.ky), "0", "0", "0"], \
                # ediv-1 Must replace ediv, that's the way xop wants undulator formatting.
                [str(self.estart), str(self.eend), str(int(self.ediv)-1), "0", "0", "0", "0"], \
                # [str(self.dist),xpos,ypos,str(self.h/self.hd),str(self.v/self.vd),str(self.xint),str(self.yint)],\
                [str(self.dist), xpos, ypos, xdim, ydim, str(self.xint), str(self.yint)], \
                [str(self.mode), str(self.method), str(self.harmonic), "0", "0", "0", "0"], \
                [str(int(self.nphi)), str(int(self.nalpha)), str(self.calpha2), str(int(self.nomega)), str(int(self.comega)), str(int(self.nsigma)), "0"]]
        
        return matrix
    
    def buildwsmatrix(self, x_offset=0, y_offset=0, x_dim=0, y_dim=0):
        """Builds the xop-formatted wiggler matrix from user-entered values"""
        xpos=str(x_offset)
        ypos=str(y_offset)
        xdim=str(x_dim)
        ydim=str(y_dim)
        
        matrix=[[str(self.title), "0", "0", "0", "0", "0", "0"], \
                [str(self.energy), str(self.current), "0", "0", "0", "0", "0"], \
                [str(self.period), str(self.num), str(self.kx), str(self.ky), "0", "0", "0"], \
                [str(self.estart), str(self.eend), str(self.ediv), "0", "0", "0", "0"], \
                # [str(self.dist),xpos,ypos,str(self.h/self.hd),str(self.v/self.vd),str(self.xint),str(self.yint)],\
                [str(self.dist), xpos, ypos, xdim, ydim, str(self.xint), str(self.yint)], \
                ["4", "0", "0", "0", "0", "0", "0"]]
        
        return matrix

    def calc_slice_volumes(self):
        """Calculates the volume of each cell/voxel"""
        
        # define the width and height of each cell. Progressive meshing will involve non-constant measurements.
        # patch_height=self.v/self.vd
        # patch_width=self.h/self.hd
        
        areas=self.areas
        # highly inefficient method to find slice volumes               
                
        
        # patch_area=patch_width*patch_height
        # print(area)
        # define indices
        klimit=len(self.thickness)
        if self.LIP==True:
            ilimit=self.vd+2
            jlimit=self.hd+2  
        else:
            ilimit=self.vd
            jlimit=self.hd  
        # slice_volumes=cell3(ilimit,jlimit,klimit)
        slice_volumes=cell3(jlimit, ilimit, klimit)  # ## TESTING CODE
        # print((klimit,ilimit,jlimit))
        # print(len(slice_volumes),len(slice_volumes[0]),len(slice_volumes[0][0]))
        for k in range(0, klimit):
            sk=slice_volumes[k]
            thickness=self.thickness[k]
            for i in range(0, ilimit):
                sik=sk[i]
                for j in range(0, jlimit):
                    # W/mm^2->W/m^2
                    # slice_volumes[k][i][j]=patch_area*self.thickness[k]*10*(10**-9)
                    sik[j]=areas[j][i]*thickness*10*(10**-9)        

        if self.print_matrix_sums:
            print_sum_matrix_by_layer(slice_volumes, 'calc_slice_volumes')
            if len(self.thickness)>1:
                print_sum_matrix(slice_volumes, 'calc_slice_volumes')
            
        return slice_volumes
          
    def filter_flux(self, s_flux):
        """Finds the transmission through a filter,#I=I0*e^(-mu*t). 3d->3d"""
        # WARNING! s_flux will be destroyed coming out of this function. 
        # This prevents the time-intensive deepcopy of s_flux->f_flux, though.

        if self.print_matrix_sums:
            print_sum_matrix(s_flux, 'filter_flux s_flux')
        
        ea=self.ea
        

        flt=self.flt_list
        
        # calculate filtered flux through layer
        # deepcopy required, may lead to issues with memory management. f
        f_flux=s_flux  # deepcopy(s_flux)  -- Need to delete after usage
        assert len(ea)==len(s_flux[0][0])
        
        # This handles multiple filters. Filters multiply together, and order does not matter
        # Binary search is used in mu3 in order to speed up computation
        for p in range(0, len(flt)):
            mat=flt[p][0]
            matthick=float(flt[p][1])/10000  # here is the conversion from micron to centimeter
            f=open("mu_data\\"+mat+".pkl", "rb")
            edata=pickle.load(f)
            f.close()
            elem_energy=[i[0] for i in edata]
            elem_flux=[i[1] for i in edata]
            for i in range(0, len(f_flux)):
                fi=f_flux[i]
                for j in range(0, len(f_flux[0])):
                    fij=fi[j]
                    # I=I0*e^(-mu*t)
                    mua=[-1*mu3(elem_energy, elem_flux, ea[m]) for m in range(0, len(ea))]
                    for m in range(0, len(ea)):
                        fij[m]*=math.exp(mua[m]*(matthick))             

        if self.print_matrix_sums:
            print_sum_matrix_by_layer(f_flux, 'filter_flux f_flux')
            if len(self.thickness)>1:
                print_sum_matrix(f_flux, 'filter_flux f_flux')

        return f_flux

    def generate_energy_axis(self):
        """returns x axis energy values. Xx is a testing element, any element can be used to generate the divisions."""

        sdata=pickle.load(open("mu_data\\Xx.pkl", "rb"))
        pickle.dump(sdata, open("pickle\\energy_axis.pkl", "wb"))
        return [i[0] for i in sdata]


    def run_heat_load_matrix(self):

        try:
            self.emit(QtCore.SIGNAL("startofrun"))
            self.updateStatus(1, 0)
            self.heat_load_matrix()
        except UserAbortException:
            self.emit(QtCore.SIGNAL("update(QString)"), "Run aborted")
            print("Run aborted")
            if path.exists(".\\job"):
                rmtree(".\\job")
            self.emit(QtCore.SIGNAL("progvalue"), 0)
        finally:
             self.emit(QtCore.SIGNAL("endofrun"))


    def heat_load_matrix(self):
        """function wrapper"""
        # if path.exists("mathematica_output"):
        #    rmtree("mathematica_output")

        self.abort=False

        self.updateStatus(1, 0, "Beginning run")

        self.emit(QtCore.SIGNAL("update(QString)"), "Processing job...")
        tstart=time()
        if path.exists(".\\job"):
            self.updateStatus(1, 2, "Removing old job files")
            rmtree(".\\job")

        self.updateStatus(1, 70, "Calculating slice volumes")

        slice_volumesv=self.calc_slice_volumes()

        self.updateStatus(1, 90)

        s_flux=self.source_flux()  # calculate flux in each pixel before filtering, xop

        if self.MATHEMATICA_OUTPUT:
            self.updateStatus(3, 5, "Mathematica output - source_flux")
            self.mathematica_output(s_flux, "source_flux")
            self.mathematica_output(self.voxel_absorbed_power_density(self.voxel_flux_to_power([s_flux]), slice_volumesv), "source_power_density")

        self.updateStatus(3, 10, "Integrated source power")

        txop=time()-tstart
        
        integrated_s_power=self.integrated_source_power(s_flux)

        s="Title: "+self.title
        s+="\nIntegrated source power without filtering: "+str(integrated_s_power)+" W\n"

        self.updateStatus(3, 20, "Filter flux")
        f_flux=self.filter_flux(s_flux)


        if self.MATHEMATICA_OUTPUT:
            self.updateStatus(3, 30, "Mathematica output - filter_flux and filter_power_density")
            self.mathematica_output(f_flux, "filter_flux")
            filter_power_densityv=self.voxel_absorbed_power_density(self.voxel_flux_to_power([f_flux]), slice_volumesv)
            self.mathematica_output(filter_power_densityv, "filter_power_density")
        s_flux=None
        gc.collect()

        self.updateStatus(3, 40, "Integrated source power")

        integrated_power_after_filtering=self.integrated_source_power(f_flux)

        s+="Integrated source power after filtering: "+str(integrated_power_after_filtering)+" W\n"

        self.updateStatus(3, 45, "Region filtered flux")

        region_filtered_fluxv=self.region_filtered_flux(f_flux)

        self.updateStatus(3, 50, "Slice transmission")

        slice_transmissionv=self.slice_transmission()

        self.updateStatus(3, 55, "Voxel absorbed flux")

        voxel_absorbed_fluxv=self.voxel_absorbed_flux(f_flux, slice_transmissionv)
        # if self.MATHEMATICA_OUTPUT: self.mathematica_output(voxel_absorbed_fluxv, "absorbed_flux")

        f_flux=None
        gc.collect()

        self.updateStatus(3, 60, "Voxel flux to power")
        voxel_absorbed_powerv=self.voxel_flux_to_power(voxel_absorbed_fluxv)

        if self.MATHEMATICA_OUTPUT:
            self.updateStatus(3, 65, "Mathematica - Voxel absorbed powerv")
            self.mathematica_output(voxel_absorbed_powerv, "power")

        self.updateStatus(3, 70, "Voxel absorbed power density")

        voxel_absorbed_power_densityv=self.voxel_absorbed_power_density(voxel_absorbed_powerv, slice_volumesv)

        if self.MATHEMATICA_OUTPUT:
            self.updateStatus(3, 70, "Mathematica - absorbed and transmitted power density")
            self.mathematica_output(voxel_absorbed_power_densityv, "absorbed_power_density")
            transmitted_power_densityv=matchdim(voxel_absorbed_power_densityv)
            for k in range(0, len(transmitted_power_densityv)):
                fk=filter_power_densityv[k]
                vk=voxel_absorbed_power_densityv[k]
                for i in range(0, len(transmitted_power_densityv[0])):
                    fki=fk[i]
                    vki=vk[i]
                    for j in range(0, len(transmitted_power_densityv[0][0])):
                        # will not index transmitted_power_densityv, not sure about reference agreement
                        transmitted_power_densityv[k][i][j]=fki[j]-vki[j]
            self.mathematica_output(transmitted_power_densityv, "transmitted_power_density")
        print("\n")

        self.updateStatus(3, 75, "Write outputs")

        if self.pout=="density":
            self.write_slice_to_table(voxel_absorbed_power_densityv, self.title)
            # display_chart("heatbump_output\\"+self.title+".csv")

        elif self.pout=="power":
            self.write_slice_to_table(voxel_absorbed_powerv, self.title)
            # display_chart("heatbump_output\\"+self.title+".csv")

        elif self.pout=="both":
            # custom testing
            self.write_slice_to_table(voxel_absorbed_power_densityv, self.title+"_density")
            self.write_slice_to_table(voxel_absorbed_powerv, self.title+"_power")

            # display_chart("heatbump_output\\"+self.title+"_density"+".csv")

            # display_chart("heatbump_output\\"+self.title+"_power"+".csv")

        self.updateStatus(3, 80, "Integrating Total Power")

        total_integrated_absorbed_power=self.total_integrated_power(voxel_absorbed_powerv)

        # self.updateStatus(3, 85, "Integrated source power")

        integrated_power_after_region=self.integrated_source_power(region_filtered_fluxv)

        tend=time()
        dt=tend-tstart
        tpython=dt-txop

        self.updateStatus(3, 90, "Final summaries")

        s+="Integrated power absorbed in the object: "+str(total_integrated_absorbed_power)+" W\n"
        s+="Integrated power transmitted through the object: "+str(integrated_power_after_region)+" W\n"

        s+="Integrated power error: "+str(abs(integrated_power_after_filtering-total_integrated_absorbed_power-integrated_power_after_region))+" W\n"

        s+="XOP/Flux time: "+str(txop)+" s\n"
        s+="Processing time: "+str(tpython)+" s\n"
        s+="Elapsed time: "+str(dt)+" s"
        
        # temporary samples
        
        f=open("heatload_results.txt", "w")
        f.write(s)
        f.close()
        print(s)
        sleep(2.0)
        
        if self.NUKE_JOBS_AT_END and path.exists("job"):
            rmtree(".\\job")
        gc.collect()

        self.updateStatus(3, 100, "Done!")


    def integrated_source_power(self, s_flux):
        """Finds total power in region, triple integral of power flux. 3d->scalar. Only uses interior points for power calculation. Exterior points used for interpolation correction"""

        if self.print_matrix_sums:
            print_sum_matrix(s_flux, 'integrated_source_power s_flux')

        intpow=0
        ea=self.ea
        areas=self.areas
        full_area=(self.h/self.hd)*(self.v/self.vd)  # area of a complete center cell
        for i in range(0, len(s_flux)):
            si=s_flux[i]
            for j in range(0, len(s_flux[0])):
                sij=si[j]
                for m in range(0, len(ea)):
                    intpow+=(sij[m]*ea[m]*1.60217646E-19)*(areas[j][i]/full_area)  # the dA element of the integral

        if self.print_matrix_sums:
            print_number(intpow, 'integrated_source_power intpow')

        return intpow
    
    def mathematica_output(self, data, name):
        """Output as a mathematica-compatible .dat file. 2d data (power, power density) is done straight, 3d data (source flux, filter flux etc.) takes sample points"""
        print("evaluating "+name)
        root="mathematica_output"
        if not path.exists(root):
            makedirs(root)
            
        hr=self.rect_center_x()
        vr=self.rect_center_y()
        ea=self.ea
        print(name+" "+str(depth(data)))
        
        # if depth(data)==2:
        if len(data[0][0])==len(hr):
            # 2d data like power and power density
            assert len(vr)==len(data[0])
            assert len(hr)==len(data[0][0])
            s=("\n".join([str(hr[i])+"\t"+str(vr[j])+"\t"+str(data[0][j][i]) for i in range(0, len(hr)-1) for j in range(0, len(vr))]))
            f=open(root+"\\"+name+".dat", "w")
            f.write(s)
            f.close()
                
        # elif depth(data)==3:
        elif len(data[0][0])==len(ea):
            # source_flux and related energy boxes
            print([len(vr), len(data), len(hr), len(data[0]), len(ea), len(data[0][0])])
            assert len(vr)==len(data)
            assert len(hr)==len(data[0])
            assert len(ea)==len(data[0][0])
            area=self.areas
            for m in self.mathematica_sampling:
                s=("\n".join([str(hr[i])+"\t"+str(vr[j])+"\t"+str(data[j][i][m]) for i in range(1, len(hr)-1) for j in range(1, len(vr)-1)]))
                f=open(root+"\\"+name+"_"+str(m)+".dat", "w")
                f.write(s)
                f.close()
                
                s2=("\n".join([str(hr[i])+"\t"+str(vr[j])+"\t"+str(data[j][i][m]/area[i][j]) for i in range(1, len(hr)-1) for j in range(1, len(vr)-1)]))
                f2=open(root+"\\"+name+"_"+str(m)+"unit.dat", "w")
                f2.write(s2)
                f2.close()
                
    def patch_flux(self, x_offset=0, y_offset=0, phase=0, jobdir='', x_dim=0, y_dim=0):
        """Runs ws() and us() depending upon the source, outputs intensity data vector"""
        # should i keep the ws and build matrix functions in wig and und, or move them here? decisions, decisions. resolved, moved to backend.
        if self.source=="wig":
            return self.ws(x_offset, y_offset, phase, jobdir, x_dim, y_dim)
        elif self.source=="und":
            return self.us(x_offset, y_offset, phase, jobdir, x_dim, y_dim)
        else:
            raise NameError("unknown source")
        return

    def region_filtered_flux(self, s_flux):
        """Finds the flux through the filtered region, accounts for materials"""

        if self.print_matrix_sums:
            print_sum_matrix(s_flux, 'region_filtered_flux s_flux')

        # Strong Feeling there is a big fat bug somewhere around here
        thickness=sum(self.thickness)  # in cm

        mat=self.mat
        ea=self.ea

        reg_flux=matchdim(s_flux)
        
        f=open("mu_data\\"+mat+".pkl", "rb")
        edata=pickle.load(f)
        f.close()
        elem_energy=[i[0] for i in edata]
        elem_flux=[i[1] for i in edata]
        # you knew it, absurdly slow code below. Really no way to get around it though. Filtering sucks, O(n^3)
        for i in range(0, len(s_flux)):
            si=s_flux[i]
            for j in range(0, len(s_flux[0])):
                sij=si[j]
                muexp=[-1*thickness*mu3(elem_energy, elem_flux, ea[m]) for m in range(0, len(ea))]
                for m in range(0, len(ea)):
                    reg_flux[i][j][m]=sij[m]*math.exp(muexp[m])
        
        if self.print_matrix_sums:
            print_sum_matrix(s_flux, 'region_filtered_flux reg_flux')
            
        return reg_flux
    
    def run_xop(self, xop_pgm, x_offset=0, y_offset=0, phase=0, jobdir='', x_dim=0, y_dim=0):
        """writes the matrix, runs xop program, and processes the result"""
        if phase==1:
            # Builds matrix/.inp file 
            if xop_pgm=='us':
                matrix=self.buildusmatrix(x_offset, y_offset, x_dim, y_dim)
            elif xop_pgm=='ws':
                matrix=self.buildwsmatrix(x_offset, y_offset, x_dim, y_dim)
                 
            s=""
            for i in matrix: 
                s+=",".join(i)
                s+="\n"
            
            # writes data into .inp file
            f=open(jobdir+'\\'+xop_pgm+".inp", "w")
            f.write(s)
            f.close()
            return
        
        # runs xop
        #   self.XOP_Processes holds the popen objects of the running processes
        #   self.XOP_run_at_one_time is the maximum number to run at once

        if phase==2:
            
            if jobdir!='waitforall':
                # Update list of processes
                self.update_process_list()
                # We wait for an open slot to process the next one

                jobs_remaining=self.jobs_to_run-self.jobs_completed

                self.updateStatus(2, 20+(80*(self.jobs_completed/self.jobs_to_run)), str(len(self.XOP_Processes))+" jobs running --- "+str(jobs_remaining)+" jobs remaining")

                if jobs_remaining<=(self.XOP_run_at_one_time*self.jobs_overcommit_at_end):
                    max_to_run=self.XOP_run_at_one_time*self.jobs_overcommit_at_end
                else:
                    max_to_run=self.XOP_run_at_one_time

                while(len(self.XOP_Processes)>=max_to_run):  # Consider a timeout
                    sleep(0.25)
                    self.update_process_list()

                jobs_remaining=self.jobs_to_run-self.jobs_completed
                self.updateStatus(2, 20+(80*(self.jobs_completed/self.jobs_to_run)), str(len(self.XOP_Processes))+" jobs running --- "+str(jobs_remaining)+" jobs remaining")

                p=subprocess.Popen(self.xop_path+"\\"+xop_pgm+".exe", cwd=jobdir)
                p.jobdir=jobdir
                print('Starting %s for jobdir %s'%(xop_pgm, jobdir))
                self.XOP_Processes.append(p)

            else:  # Wait for all jobs to finish
                while(len(self.XOP_Processes)>0):  # Consider a timeout
                    sleep(0.25)
                    oldVal=len(self.XOP_Processes)
                    self.update_process_list()
                    if len(self.XOP_Processes)!=oldVal:
                        jobs_remaining=self.jobs_to_run-self.jobs_completed
                        self.updateStatus(2, 20+(80*(self.jobs_completed/self.jobs_to_run)), str(len(self.XOP_Processes))+" jobs running --- "+str(jobs_remaining)+" jobs remaining")
                return

        # reads results
        if phase==3:
            # read output from each job's .out file
            xop_data=[]
            f2=open(jobdir+'\\'+xop_pgm+".out", "r")
            for i, line in enumerate(f2):
                if (xop_pgm=='us' and i>=23) or (xop_pgm=='ws' and i>=18):
                    g=line[0:26].split()
                    nbr=g[1]
                    # Sometimes, XOP does not put the 'E' in, so if it is not there, we do it
                    if nbr.find('E')==-1:
                        if nbr.find('-')!=-1:
                            nbr=nbr.replace('-', 'E-')
                        else:
                            nbr=nbr.replace('+', 'E+')
                    xop_data.append(float(nbr))
            f2.close()
            return xop_data 

        return "Invalid phase"
    
    def slice_transmission(self):
        """Finds the amount of flux that passes though a each slice. slice_t[i][j] j direction: energies, i direction: thickness 2d. Energy divisions are locked into 5000""" 
        slice_t=[]
        # returns mu values for particular element (y values). Equivalent of filter_flux for region
        f=open("mu_data\\"+self.mat+".pkl", "rb")
        mu_data=pickle.load(f)
        f.close()
        mu_raw=[i[1] for i in mu_data]
        for layer in self.thickness:
            # locked into scan parameter of 500 min 100000 max 5000 div
            # slow as hell. is there a trend here?
            slice_t.append([math.exp(-1*layer*k) for k in mu_raw])
            
        if self.print_matrix_sums:
            print_sum_matrix_by_layer(slice_t, 'slice_transmission slice_t')
            if len(self.thickness)>1:
                print_sum_matrix(slice_t, 'slice_transmission slice_t')
            
        return slice_t
    
    def source_flux(self):
        """finds the energy flux in a region, through multiple calls to xop. ->3d"""

        self.updateStatus(2, 0, "Preparing jobs")

        if self.LIP==True:
            s_flux=cell2(self.hd+2, self.vd+2)
            uncorrected_flux=cell2(self.hd+2, self.vd+2)
        else:
            s_flux=cell2(self.hd, self.vd)
            uncorrected_flux=cell2(self.hd, self.vd)
        
        pc=self.rect_centers()
        dimensions=self.rect_dimensions()
        ea=self.ea
        dE=ea[1]-ea[0]
        
        if self.LIP==True:
            ilimit=self.vd+2
            jlimit=self.hd+2
        else:
            ilimit=self.vd
            jlimit=self.hd
        # print(depth(pc),[ilimit,len(pc)],[jlimit,len(pc[0]),])
        
        self.jobs_to_run=ilimit*jlimit
        self.jobs_completed=0
        self.jobs_overcommit_at_end=1.5
                
        jobdirroot=".\\job"
        if not path.exists(jobdirroot):
            makedirs(jobdirroot)

        self.updateStatus(2, 10, "Generating input files for XOP")

        # Phase 1 - Generate input files for XOP programs

        numPoints=ilimit*jlimit

        numPointsPerStatusUpdate=numPoints/10

        pointsProcessed=0

        for i in range(0, ilimit):
            for j in range(0, jlimit):
                x_offset=pc[j][i][0]
                y_offset=pc[j][i][1]
                x_dim=dimensions[j][i][0]
                y_dim=dimensions[j][i][1]
                jobdir=jobdirroot+'\\'+str(i)+'-'+str(j)
                if not path.exists(jobdir):
                    makedirs(jobdir)
                self.patch_flux(x_offset, y_offset, 1, jobdir, x_dim, y_dim)
                pointsProcessed+=1
                if pointsProcessed%numPointsPerStatusUpdate==0:
                    self.updateStatus(2, 10+(pointsProcessed/numPointsPerStatusUpdate))

        # Phase 2 - Run XOP programs, multi-processing           
        for i in range(0, ilimit):
            for j in range(0, jlimit):
                x_offset=pc[j][i][0]
                y_offset=pc[j][i][1]
                jobdir=jobdirroot+'\\'+str(i)+'-'+str(j)
                x_dim=dimensions[j][i][0]
                y_dim=dimensions[j][i][1]
                self.patch_flux(x_offset, y_offset, 2, jobdir, x_dim, y_dim)

        self.patch_flux(0, 0, 2, 'waitforall')  # wait for remaining jobs to finish              

        pointsProcessed=0
        self.updateStatus(2, 90, "Processing output files from XOP")

        # Phase 3 - Read output files from XOP programs and incorporate data
        for i in range(0, ilimit):
            for j in range(0, jlimit):
                x_offset=pc[j][i][0]
                y_offset=pc[j][i][1]
                jobdir=jobdirroot+'\\'+str(i)+'-'+str(j)
                x_dim=dimensions[j][i][0]
                y_dim=dimensions[j][i][1]
                s_flux[i][j]=self.patch_flux(x_offset, y_offset, 3, jobdir, x_dim, y_dim)
                uncorrected_flux[i][j]=s_flux[i][j]

                # print(len(s_flux),len(s_flux[i]),len(s_flux[i][j]),len(ea))
                
                assert depth(s_flux)==3
                if self.LIP:
                    assert ilimit==self.vd+2
                    assert jlimit==self.hd+2 
                else:
                    assert ilimit==self.vd 
                    assert jlimit==self.hd 
                assert ilimit==len(s_flux)
                assert jlimit==len(s_flux[i])
                assert len(ea)==len(s_flux[i][j])

                for m in range(0, len(ea)):
                    # convert from bandpass to raw flux(ph/s/.1%BW -> ph/s)
                    # GOTCHA! Bug, i found you!
                    s_flux[i][j][m]*=1000*dE/ea[m]
                    # s_flux[i][j][k]=s_flux[i][j][k]*1000*dE/ea[k]
        # self.write_uncorrected_flux(uncorrected_flux)

                if pointsProcessed%numPointsPerStatusUpdate==0:
                    self.updateStatus(2, 90+(pointsProcessed/numPointsPerStatusUpdate))


        if self.print_matrix_sums:
            print_sum_matrix(s_flux, 'source_flux s_flux')
        return s_flux     

    def total_integrated_power(self, v_power):
        """Find total power in object"""
        
        # index limits
        assert depth(v_power)==3
        
        if self.print_matrix_sums:
            print_sum_matrix_by_layer(v_power, 'total_integrated_power v_power')
            if len(self.thickness)>1:
                print_sum_matrix(v_power, 'total_integrated_power v_power')


        areas=self.areas
        full_area=(self.h/self.hd)*(self.v/self.vd)
        total_integrated_power=0
        
        klimit=len(v_power)
        ilimit=len(v_power[0])
        jlimit=len(v_power[0][0])

        for k in range(0, klimit):
            vk=v_power[k]
            for i in range(0, ilimit):
                vki=vk[i]
                for j in range(0, jlimit):
                    # total_integrated_power+=v_power[k][i][j]*(areas[j][i]/full_area)*self.thickness[k]/sumthick #dV element
                    total_integrated_power+=vki[j]*(areas[j][i]/full_area)  # ## *self.thickness[k]/sumthick ### TESTING FIX
                    # print(v_power[k][i][j], areas[j][i], full_area, self.thickness[k], sumthick, total_integrated_power)
                    
        # This takes the sum of all elements in total_integrated_power, equivalent to the above triple integral.
        # Inaccurate, does not account for area.
        # total_integrated_power=sum(sum(sum(v_power,[]),[]))
        
        if self.print_matrix_sums:
            print_number(total_integrated_power, 'total_integrated_power returns')

        return total_integrated_power
    
    def update_process_list(self):
        new_process_list=[]
        for p in self.XOP_Processes:
            if p.poll()==None:
                new_process_list.append(p)
            else:
                print('Ending jobdir %s code %s'%(p.jobdir, p.poll()))
                self.jobs_completed+=1
                pass  # Process if error
        self.XOP_Processes=new_process_list

        jobs_remaining=self.jobs_to_run-self.jobs_completed
        self.updateStatus(2, 20+(80*(self.jobs_completed/self.jobs_to_run)), str(len(self.XOP_Processes))+" jobs running --- "+str(jobs_remaining)+" jobs remaining")

    def us(self, x_offset=0, y_offset=0, phase=0, jobdir="", x_dim=0, y_dim=0):
        """writes the matrix to us.inp, runs ws.exe, and processes the result"""
        return self.run_xop('us', x_offset, y_offset, phase, jobdir, x_dim, y_dim)
    
    def voxel_absorbed_flux(self, f_flux, slice_t):
        """Finds the power flux from source and transmission through each layer. s_flux=3d, slice_t=2d"""

        if self.print_matrix_sums:
            print_sum_matrix(f_flux, 'voxel_absorbed_flux s_flux')
            print_sum_matrix(slice_t, 'voxel_absorbed_flux slice_t')
        
        # This is a troublesome, fickle beast (when processing undulators)
        voxel_impinging_flux=matchdim(slice_t)  # 4d, eventually
        assert len(slice_t)==len(voxel_impinging_flux)
        # calculate cumulative transmission through each layer
        
        cumulative_transmission=matchdim(slice_t)  # 2d
        cumulative_transmission[0]=matchdim(slice_t[0], 1)
        
        slice_absorption=deepcopy(slice_t)
        assert len(slice_absorption)==len(slice_t)==len(voxel_impinging_flux)
        # absorption+transmission=1, 2d
        for i in range(0, len(slice_t)):
            for j in range(0, len(slice_t[0])):
                slice_absorption[i][j]=1-slice_t[i][j]

        if self.print_matrix_sums:
            print_sum_matrix(slice_absorption, 'voxel_absorbed_flux slice_absorption')

        # print("slice_absorption, slice_t:")
        # print(slice_absorption, slice_t)
        
        for i in range(0, len(self.thickness)):
            j=i
            temp_transmission=matchdim(slice_t[0], 1)
            
            while j>0:
                assert len(temp_transmission)==len(slice_t[j])
                # temp_transmission=mult(temp_transmission,slice_t[j]) 
                temp_transmission=mult(temp_transmission, slice_t[j-1])  # ## TESTING FIX
                j-=1
            cumulative_transmission[i]=temp_transmission

        if self.print_matrix_sums:
            print_sum_matrix_by_layer(cumulative_transmission, 'voxel_absorbed_flux cumulative_transmission')
            if len(self.thickness)>1:
                print_sum_matrix(cumulative_transmission, 'voxel_absorbed_flux cumulative_transmission')
        
        # print("\ncumulative_transmission:")
        # print(cumulative_transmission)
        
        for k in range(0, len(slice_t)):
            temp_surface=matchdim(f_flux)
            # for i in range(0,len(s_flux[0])):
            #    for j in range(0, len(s_flux)-1):
            for i in range(0, len(f_flux)):  # ## TESTING FIX
                for j in range(0, len(f_flux[0])):  # ## TESTING FIX
                    # temp_surface[i][j]=mult(f_flux[i][j],cumulative_transmission[k])
                    temp_surface[i][j]=mult(f_flux[i][j], cumulative_transmission[k])  # ## TESTING FIX
            voxel_impinging_flux[k]=temp_surface
        
        if self.print_matrix_sums:
            print_sum_matrix_by_layer(voxel_impinging_flux, 'voxel_absorbed_flux voxel_impinging_flux')
            if len(self.thickness)>1:
                print_sum_matrix(voxel_impinging_flux, 'voxel_absorbed_flux voxel_impinging_flux')

        # print("\nvoxel_impinging_flux")
        # print(voxel_impinging_flux)
        voxel_absorbed_flux=matchdim(voxel_impinging_flux)
        
        assert depth(slice_absorption)==2
        assert depth(voxel_impinging_flux)==4
        
        
        for k in range(0, len(voxel_impinging_flux)):
            # temp_surface 3d, initialize as empty 2d
            # temp_surface=cell2(len(voxel_impinging_flux[0]),len(voxel_impinging_flux[0][0]))
            temp_surface=cell2(len(voxel_impinging_flux[0][0]), len(voxel_impinging_flux[0]))  #### TESTING FIX
            s_ak=slice_absorption[k]
            vk=voxel_impinging_flux[k]
            for i in range(0, len(voxel_impinging_flux[0])):
                vki=vk[i]
                for j in range(0, len(voxel_impinging_flux[0][0])):
                    # print([len(voxel_impinging_flux),len(voxel_impinging_flux[k]),len(voxel_impinging_flux[k][i]),len(voxel_impinging_flux[k][i][j])])
                    # print([len(slice_absorption),len(slice_absorption[0])])
                    # assert len(voxel_impinging_flux[k][i][j])==len(slice_absorption[k])
                    vkij=vki[j]
                    temp_surface[i][j]=[vkij[m]*s_ak[m] for m in range(0, len(slice_absorption[k]))]
            voxel_absorbed_flux[k]=temp_surface
        # print("\nvoxel_absorbed_flux")
        # print(voxel_absorbed_flux) 
        # 4d

        if self.print_matrix_sums:
            print_sum_matrix_by_layer(voxel_absorbed_flux, 'voxel_absorbed_flux voxel_absorbed_flux')
            if len(self.thickness)>1:
                print_sum_matrix(voxel_absorbed_flux, 'voxel_absorbed_flux voxel_absorbed_flux')
            
        return voxel_absorbed_flux

    def voxel_absorbed_power_density(self, v_power, slice_volumes):
        """Divide power by volume to get power density. 3d->3d"""
        assert matchdim(v_power)==matchdim(slice_volumes)
        
        if self.print_matrix_sums:
            print_sum_matrix_by_layer(v_power, 'voxel_absorbed_power_density v_power')
            if len(self.thickness)>1:
                print_sum_matrix(v_power, 'voxel_absorbed_power_density v_power')

            print_sum_matrix_by_layer(slice_volumes, 'voxel_absorbed_power_density slice_volumes')
            if len(self.thickness)>1:
                print_sum_matrix(slice_volumes, 'voxel_absorbed_power_density slice_volumes')
       
        v_power_density=matchdim(v_power)
        
        # The indeces here are brutal and do not conform to the rest of the index convention. This monstrosity will be fixed later.
        for k in range(0, len(v_power)):
            vk=v_power[k]
            sk=slice_volumes[k]
            for j in range(0, len(v_power[0])):
                vkj=vk[j]
                skj=sk[j]
                for i in range(0, len(v_power[0][0])):
                    # v_power_density[k][i][j]=v_power[k][i][j]/slice_volumes[k][i][j]
                    v_power_density[k][j][i]=vkj[i]/skj[i]  # ## TESTING FIX
                    
        if self.print_matrix_sums:
            print_sum_matrix_by_layer(v_power_density, 'voxel_absorbed_power_density v_power_density')
            if len(self.thickness)>1:
                print_sum_matrix(v_power_density, 'voxel_absorbed_power_density v_power_density')
        
        return v_power_density
        
    def voxel_flux_to_power(self, v_flux):
        """Transforms the power flux load into power. 4d->3d"""
        
        if self.print_matrix_sums:
            print_sum_matrix_by_layer(v_flux, 'voxel_flux_to_power v_flux')
            if len(self.thickness)>1:
                print_sum_matrix(v_flux, 'voxel_flux_to_power v_flux')
       
        # v_flux[slice][y][x][energy]
        v_power=matchdim(v_flux)
        ea=self.ea
        # initialize index limits
        klimit=len(self.thickness)  # thickness, z
        # i:y
        # j:x
        if self.LIP==True:
            ilimit=self.vd+2
            jlimit=self.hd+2
        else:
            ilimit=self.vd
            jlimit=self.hd
        mlimit=len(ea)  # energy
        # dE=self.ea[2]-self.ea[1]
        
        # massive time draining calculations! Woohoo!
        for k in range(0, klimit):
            vk=v_flux[k]
            for i in range(0, ilimit):
                vki=vk[i]
                for j in range(0, jlimit):
                    vkij=vki[j]
                    for m in range(0, mlimit):
                        v_power[k][i][j][m]=vkij[m]*ea[m]*1.60217646e-19
                        
        # int_v_power=cell3(ilimit,jlimit,klimit)
        int_v_power=cell3(jlimit, ilimit, klimit)  # ## TESTING CODE
        
        # Quadruple integral!
        for k in range(0, klimit):
            vk=v_power[k]
            for i in range(0, ilimit):
                vki=vk[i]
                for j in range(0, jlimit):
                    vkij=vki[j]
                    temp_power=0
                    for m in range(0, mlimit):
                        temp_power+=vkij[m]
                    # There seems to be a factor of about 4 between the true power/density and the heatbump-produced. FIXED!
                    int_v_power[k][i][j]=temp_power  # /3.985473468
                    
        if self.print_matrix_sums:
            print_sum_matrix_by_layer(int_v_power, 'voxel_flux_to_power int_v_power')
            if len(self.thickness)>1:
                print_sum_matrix(int_v_power, 'voxel_flux_to_power int_v_power')
        
        return int_v_power
        
    def write_uncorrected_flux(self, uncorrected_flux):
        """writes each power slice to the file output.csv. 3d->file"""
        # There might be an error here in the cube writing to file, y instead of z split.
        # screw it, 4d array to 3d file doesn't work well.
        st=""
        u_flux=uncorrected_flux
        
        # voxel dimensions
        zlen=len(u_flux)
        ylen=len(u_flux[0])
        xlen=len(u_flux[0][0])
        
        for k in range(0, zlen):
            s=""
            power_temp=cell2(xlen, ylen)        
            for i in range(0, ylen):
                for j in range(0, xlen):
                    # flipdim unnecesary
                    power_temp[i][j]=u_flux[k][i][j]
            
            
            power_temp_s=[list(map(str, i)) for i in power_temp]
            
            s+="\n".join([",".join(i) for i in power_temp_s])
            
            
            if k==0:
                st+=s
            else:
                st+="\n\n"+s
      
        f=open("raw_flux.csv", "w")
        f.write(st)
        f.close()
        
        f2=open("pickle\\raw_flux.pkl", "wb")
        pickle.dump(u_flux, f2)
        f2.close()

    def write_slice_to_table(self, voxel_absorbed_power_density, title):
        """writes each power slice to the file output.csv. 3d->file"""
        # There might be an error here in the cube writing to file, y instead of z split.
        st=""
        vd=voxel_absorbed_power_density

        # Axis definitions
        hr=[0]+self.rect_center_x()+[self.h]
        vr=[0]+self.rect_center_y()+[self.v]
        
        # voxel dimensions
        zlen=len(vd)
        ylen=len(vd[0])
        xlen=len(vd[0][0])
        for k in range(0, zlen):
            # thickness loop
            s=""
            power_temp=cell2(xlen, ylen)        
            for i in range(0, ylen):
                for j in range(0, xlen):
                    # flipdim unnecesary
                    power_temp[i][j]=vd[k][i][j]
            
        
            # vertical zero padding
            for i in range(0, ylen):
                power_temp[i].insert(0, 0)
                power_temp[i].append(0)
                
        
            # horizantal zero padding
            power_temp.append(cell1(xlen+2))
            power_temp.insert(0, cell1(xlen+2))
            
            if (len(power_temp)<len(vr)):
                print('len(power_temp) >= i', k, len(power_temp), i, len(vr))

            for i in range(0, len(vr)):
                power_temp[i].insert(0, vr[i])  # ## BUG
            
            hr.insert(0, 10*self.thickness[k])
            power_temp.insert(0, hr)
            power_temp_s=[list(map(str, i)) for i in power_temp]
            
            s+="\n".join([",".join(i) for i in power_temp_s])
            
            if k==0:
                st+=s
            else:
                st+="\n\n"+s
            del hr[0]
        outputfile="heatload_output\\"+title+".csv"
        
        outputfile_d=path.dirname(outputfile)
        
        if not path.exists(outputfile_d):
            makedirs(outputfile_d)
        
        f=open(outputfile, "w")
        f.write(st)
        f.close()
        
    def ws(self, x_offset=0, y_offset=0, phase=0, jobdir="", x_dim=0, y_dim=0):
        return self.run_xop('ws', x_offset, y_offset, phase, jobdir, x_dim, y_dim)
        
if __name__=="__main__":
    # display_chart("c:\project\python\heat load\heatbump_output\output_power.csv")    
    # display_chart("c:\project\python\heat load\heatbump_output\output_density.csv")    
    print("Please, don't run me from here! Run heatbump through heatbump.py")
