from basic_functions import cell1, cell2, cell3, mult, mu2, depth, matchdim
import math
from time import time
import _pickle as pickle
from os import system, path, makedirs
import rectangle_grid

"""
The centipede has been caught! This error turned values of source_flux from 10^12 --> 10^-21, due to a "=" instead of a "==" in region_filtered flux
Interpolation guard is currently being implemented. The previous implementation did not work well, working on now. Created a new class and rectangle handling function to deal with this error.
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
        #intepolation guard length
        self.d=10**-5
        #set up rectangle handling
        self.rect_setup()
        
        
        
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
        
        area=self.rect_areas()
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
        slice_volumes=cell3(ilimit,jlimit,klimit)
        #print((klimit,ilimit,jlimit))
        #print(len(slice_volumes),len(slice_volumes[0]),len(slice_volumes[0][0]))
        for k in range(0,klimit):
            for i in range(0,ilimit):
                for j in range(0,jlimit):
                    #W/mm^2->W/m^2
                    #slice_volumes[k][i][j]=patch_area*self.thickness[k]*10*(10**-9)
                    slice_volumes[k][i][j]=area[i][j]*self.thickness[k]*10*(10**-9)        

        return slice_volumes
        
    
    def filter_flux(self,s_flux):
        """Finds the transmission through a filter,#I=I0*e^(-mu*t). 3d->3d"""
        #find the user submitted filters       
        ff=open("pickle\\flt.pkl","rb")
        flt_old=pickle.load(ff)
        ff.close()
        
        ea=self.generate_energy_axis()
        

        flt=[i for i in flt_old if i[0]!=None and i[1]!=None]
        
        #calculate filtered flux through layer
        f_flux=s_flux
        assert len(ea)==len(s_flux[0][0])
        
        #This handles multiple filters. Filters multiply together, and order does not matter
        #This calculation is as slow as hell, but there is no way around it
        for p in range(0,len(flt)):
            mat=flt[p][0]
            f=open("mu_data\\"+mat+".pkl","rb")
            edata=pickle.load(f)
            f.close()
            for i in range(0,len(s_flux)):
                for j in range(0,len(s_flux[0])):
                    #I=I0*e^(-mu*t)
                    for k in range(0,len(ea)):
                        f_flux[i][j][k]*=math.exp(-1*mu2(edata,ea[k])*(flt[p][1]/10000))             
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
        #export corner results for testing so far, this result agrees with the previous result
        """
        s_flux_sample=s_flux[self.vd-1][self.hd-1]
        s1="\n".join([str(i) for i in s_flux_sample])
        f=open("s_flux_data_in_function.csv","w")
        f.write(s1)
        f.close()
        #print("line 230\ts_flux assignment")
        #print(s_flux[self.vd-1][self.hd-1][3000:3005])
        """
        integrated_s_power=self.integrated_source_power(s_flux)
        print("s_flux assignment " ,time()-tstart)
        s="Integrated Source Power without filtering: "+str(integrated_s_power)+" W\n"
        
        #export f_flux resutlts for testing
        f_flux=self.filter_flux(s_flux)
        """
        f_flux_sample=f_flux[self.vd-1][self.hd-1]
        s2="\n".join([str(i) for i in f_flux_sample])
        f=open("f_flux_data_in_function.csv","w")
        f.write(s2)
        f.close()
        #print("line 245\tf_flux assignment")
        #print(s_flux[self.vd-1][self.hd-1][3000:3005])
        """
        integrated_power_after_filtering=self.integrated_source_power(f_flux)
        s+="Integrated source power after filtering: "+str(integrated_power_after_filtering)+" W\n"
        print("f_flux assignment ",time()-tstart)
        #DINGDINGDING! The bug is in one of these two functions. Phil thinks there is a faulty comparision somewhere, a = instead of an ==
        region_filtered_fluxv=self.region_filtered_flux(f_flux)        
        slice_transmissionv=self.slice_transmission()
        print("slice_transmission ",time()-tstart)
        #print("line 254\tregion_filtered_flux and slice_transmission")
        #print(s_flux[self.vd-1][self.hd-1][3000:3005])
        voxel_absorbed_fluxv=self.voxel_absorbed_flux(f_flux,slice_transmissionv)
        print("voxel_absorbed_fluxv ",time()-tstart)
        voxel_absorbed_powerv=self.voxel_flux_to_power(voxel_absorbed_fluxv)
        print("voxel_absorbed_power ",time()-tstart)        
        slice_volumesv=self.calc_slice_volumes()        
        print("calc_slice_volume ",time()-tstart)
        voxel_absorbed_power_densityv=self.voxel_absorbed_power_density(voxel_absorbed_powerv, slice_volumesv)
        print("voxel_absorbed_power_density ",time()-tstart)
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
        print("write_slice_to_table ",time()-tstart)        
        total_integrated_absorbed_power=self.total_integrated_power(voxel_absorbed_powerv)        
        integrated_power_after_region=self.integrated_source_power(region_filtered_fluxv)
        print("final power integrals ",time()-tstart)
        
        #print("line 275\twriting files")
        #print(s_flux[self.vd-1][self.hd-1][3000:3005])
        tend=time()
        dt=tend-tstart
        
        s+="Integrated power absorbed in the object: "+str(total_integrated_absorbed_power)+" W\n"
        s+="Integrated power transmitted through the object: "+str(integrated_power_after_region)+" W\n"
        s+="Elapsed time: "+str(dt)+" s\n"
        
        #temporary samples
        
        """
        s+="Here are some samples of data:\n"
        s+="\tsource flux data"+str(s_flux[self.vd-1][self.hd-1][3000:3005])+"\n"
        s+="\tfilter flux data"+str(f_flux[self.vd-1][self.hd-1][3000:3005])+"\n"
        s+="\tslice transmission"+str(slice_transmissionv[0][3000:3005])+"\n"
        s+="\tpower data:"+str(voxel_absorbed_powerv[0])+"\n"
        s+="\tpower density:"+str(voxel_absorbed_power_densityv[0])+"\n"
        """
        f=open("heatbump_result.txt","w")
        f.write(s)
        f.close()
        print(s)
        
    def integrated_source_power(self,s_flux):
        """Finds total power in region, triple integral of power flux. 3d->scalar. Only uses interior points for power calculation. Exterior points used for interpolation correction"""
        intpow=0
        ea=self.generate_energy_axis()
        areas=self.rect_areas()
        full_area=(self.h/self.hd)*(self.v/self.vd) #area of a complete center cell
        for i in range(0,len(s_flux)):
            for j in range(0,len(s_flux[0])):
                for k in range(0, len(ea)):
                    intpow+=(s_flux[i][j][k]*ea[k]*1.60217646E-19)*(areas[i][j]/full_area)#the dA element of the integral
        return intpow
    
    
    def patch_flux(self,x_offset=0,y_offset=0):
        """Runs ws() and us() depending upon the source, outputs intensity data vector"""
        #should i keep the ws and build matrix functions in wig and und, or move them here? decisions, decisions. resolved, moved to backend.
        if self.source=="wig":
            self.ws(x_offset,y_offset)
            f=open("pickle\\ws_data.pkl","rb")
            ws_data=pickle.load(f)
            f.close()
            return [i[1] for i in ws_data]
        elif self.source=="und":
            self.us(x_offset,y_offset)
            f=open("pickle\\us_data.pkl","rb")
            us_data=pickle.load(f)
            f.close()
            return [i[1] for i in us_data]
        else: 
            raise NameError("unknown source")
    
    def region_filtered_flux(self,s_flux):
        """Finds the flux through the filtered region, accounts for materials"""
        #Strong Feeling there is a big fat bug somewhere around here
        thickness=sum(self.thickness) #in cm

        mat=self.mat        
        ea=self.generate_energy_axis()        
        
        reg_flux=matchdim(s_flux)
        
        f=open("mu_data\\"+mat+".pkl","rb")
        edata=pickle.load(f)
        f.close()
        #you knew it, absurdly slow code below. Really no way to get around it though. Filtering sucks, O(n^3)
        for i in range(0, len(s_flux)):
            for j in range(0,len(s_flux[0])):
                for k in range(0, len(ea)):
                    reg_flux[i][j][k]=s_flux[i][j][k]*math.exp(-1*thickness*mu2(edata,ea[k]))
        
        return reg_flux
    
    def total_integrated_power(self,v_power):
        """Find total power in object"""
        
        #index limits
        assert depth(v_power)==3
        
        areas=self.rect_areas()
        full_area=(self.h/self.hd)*(self.v/self.vd)
        total_integrated_power=0
        
        klimit=len(v_power)
        ilimit=len(v_power[0])
        jlimit=len(v_power[0][0])

        for k in range(0,klimit):
            for i in range(0,ilimit):
                for j in range(0,jlimit):
                    total_integrated_power+=v_power[k][i][j]*(areas[i][j]/full_area)#dA element
        #This takes the sum of all elements in total_integrated_power, equivalent to the above triple integral.
        #Inaccurate, does not account for area.
        #total_integrated_power=sum(sum(sum(v_power,[]),[]))
        
        return total_integrated_power
    
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
        for i in range(0,ilimit):
            for j in range(0,jlimit):
                x_offset=pc[i][j][0]
                y_offset=pc[i][j][1]
                s_flux[i][j]=self.patch_flux(x_offset,y_offset)

                
                uncorrected_flux[i][j]=s_flux[i][j]
    
                for k in range(0,len(ea)):
                    #convert from bandpass to raw flux(ph/s/.1%BW -> ph/s)
                    #GOTCHA! Bug, i found you!
                    s_flux[i][j][k]*=1000*dE/ea[k]
                    #s_flux[i][j][k]=s_flux[i][j][k]*1000*dE/ea[k]
        #self.write_uncorrected_flux(uncorrected_flux)
        
        return s_flux       

    def us(self,x_offset=0,y_offset=0):
        """writes the matrix to us.inp, runs ws.exe, and processes the result"""
        matrix=self.buildusmatrix(x_offset,y_offset)
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
        
        #pickle floating-point results to file
        f3=open("pickle\\us_data.pkl","wb")
        pickle.dump(us_data, f3)
        f3.close()
        
        #typecast results into strings, write to .csv file
        """
        s=""
        us_data_s=[[str(i[0]),str(i[1])] for i in us_data]
        s+="\n".join([",".join(i) for i in us_data_s])
        
        f4=open("us_data.csv","w")
        f4.write(s)
        f4.close()
        """
    def voxel_absorbed_flux(self,s_flux, slice_t):
        """Finds the power flux from source and transmission through each layer. s_flux=3d, slice_t=2d"""
        #This is a troublesome, fickle beast (when processing undulators)
        voxel_impinging_flux=matchdim(slice_t)            #4d, eventually
        assert len(slice_t)==len(voxel_impinging_flux)
        #calculate cumulative transmission through each layer
        
        cumulative_transmission=matchdim(slice_t)             #2d
        cumulative_transmission[0]=matchdim(slice_t[0],1)
        
        slice_absorption=slice_t
        assert len(slice_absorption)==len(slice_t)==len(voxel_impinging_flux)
        #absorption+transmission=1, 2d
        for i in range(0, len(slice_t)):
            for j in range(0, len(slice_t[0])):
                slice_absorption[i][j]=1-slice_t[i][j]
        #print("slice_absorption:")
        #print(slice_absorption)
        
        for i in range(0,len(self.thickness)):
            j=i
            temp_transmission=matchdim(slice_t[0],1)
            
            while j>0:
                assert len(temp_transmission)==len(slice_t[j])
                temp_transmission=mult(temp_transmission,slice_t[j]) 
                j-=1
            cumulative_transmission[i]=temp_transmission
        
        #print("\ncumulative_transmission:")
        #print(cumulative_transmission)
        
        for k in range(0, len(slice_t)):
            temp_surface=s_flux
            for i in range(0,len(s_flux[0])):
                for j in range(0, len(s_flux)-1):
                    temp_surface[i][j]=mult(s_flux[i][j],cumulative_transmission[k])
            voxel_impinging_flux[k]=temp_surface
        
        #print("\nvoxel_impinging_flux")
        #print(voxel_impinging_flux)
        voxel_absorbed_flux=matchdim(voxel_impinging_flux)
        
        assert depth(slice_absorption)==2
        assert depth(voxel_impinging_flux)==4
        
        
        for k in range(0, len(voxel_impinging_flux)):
            #temp_surface 3d, initialize as empty 2d
            temp_surface=cell2(len(voxel_impinging_flux[0]),len(voxel_impinging_flux[0][0]))
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
        return voxel_absorbed_flux

    def voxel_absorbed_power_density(self,v_power,slice_volumes):
        """Divide power by volume to get power density. 3d->3d"""
        assert matchdim(v_power)==matchdim(slice_volumes)
        
        v_power_density=matchdim(v_power)
        
        for k in range(0,len(v_power)):
            for j in range(0,len(v_power[0])):
                for i in range(0,len(v_power[0][0])):
                    v_power_density[k][i][j]=v_power[k][i][j]/slice_volumes[k][i][j]
        
        return v_power_density
        
    def voxel_flux_to_power(self,v_flux):
        """Transforms the power flux load into power. 4d->3d"""
        
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
                        
        int_v_power=cell3(ilimit,jlimit,klimit)
        
        #Quadruple integral!
        for k in range(0,klimit):
            for j in range(0,jlimit):
                for i in range(0,ilimit):
                    temp_power=0
                    for m in range(0,mlimit):
                        temp_power+=v_power[k][i][j][m]
                    #There seems to be a factor of about 4 between the true power/density and the heatbump-produced.
                    int_v_power[k][i][j]=temp_power #/3.985473468
        
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
        hr=[0]+[i[0][0] for i in pc]+[self.h]
        vr=[0]+[i[1] for i in pc[0]]+[self.v]

        #prevent energy bleeding due to ansys approximations, lock points close to boundaries near zero
        #THIS IS THE FATAL FLAW! locking down next to centers is wrong, must lock down close to edge.
        #This brings up a major problem, as the edge points must be sampled in order to properly lock the energy values
        #New points must be introduced, but there is an issue as to what their volumes are for density purposes,
        #as well the fact that they must not be included in any and all integrals to find power in the region,
        #besides that multiprocessing will not support this. As of now, the lock will occur on the boundary, 
        #this may produce incorrect results, though
        """
        minh=min(hr)-.0000000001
        maxh=max(hr)+.0000000001
        minv=min(vr)-.0000000001
        maxv=max(vr)+.0000000001
        """
        #This forces locking on the edge, vs. above, which locks by the irrelevant point center
        """
        minh=0
        maxh=self.h
        minv=0
        maxv=self.v
        hr.extend([minh,maxh])
        vr.extend([minv,maxv])
        
        hr.sort()
        vr.sort()
        
        """        
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
            
            for i in range(0,len(vr)):
                power_temp[i].insert(0,vr[i])
            
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

    def ws(self,x_offset=0,y_offset=0):
        """writes the matrix to ws.inp, runs ws.exe, and processes the result"""
        matrix=self.buildwsmatrix(x_offset,y_offset)
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

        for i, line in enumerate(f2):
            if i>=18:
                g=line[0:26].split()
                ws_data.append([float(x) for x in g])        
        f2.close()
        
        #write floating-point results to file
        f3=open("pickle\\ws_data.pkl","wb")
        pickle.dump(ws_data, f3)
        f3.close()
        
        #typecast results into strings, write to .csv file
        """
        s=""
        ws_data_s=[[str(i[0]),str(i[1])] for i in ws_data]
        s+="\n".join([",".join(i) for i in ws_data_s])
        
        f4=open("us_data.csv","w")
        f4.write(s)
        f4.close()
        """
        
if __name__=="__main__":
    print("Please, don't run me from here! Run heatbump through heatbump.py")