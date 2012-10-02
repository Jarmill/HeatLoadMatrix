"""Gigantic Function Testing File! Megatest.py, for source_flux
Megatest is success! source_flux works!
"""
#imports 
from basic_functions import cell1, cell2, cell3, mult, mu2, depth
from os import system
import math
from time import time
import _pickle as pickle
#pseudoglobal values
hd=2
vd=2
h=1
v=.5
mat="Si"
thickness=[1000]
source="und"
xop_path="C:\\Users\\Public\\Documents\\xop2.3\\bin.x86\\"

def patch_centers(x_offset=0,y_offset=0):
    """Calculates Centers of rectangular cells"""
    #create empty array
    patch=cell2(hd,vd)
            
    for i in range(0,vd):
        for j in range(0,hd):
            x=-h/2+h/(2*hd)+(j-1)*h/hd+x_offset+h/2+h/hd
            y=v/2-v/(2*vd)-(i-1)*v/vd+y_offset+v/2-v/vd
            patch[i][j]=[x,y]        
    return patch

def calc_slice_volumes():
    """Calculates the volume of each cell/voxel"""
    pc=patch_centers()
    
    if vd==1:
        patch_height=v
    else:
        patch_height=pc[0][0][1]-pc[1][0][1]
    
    if hd==1:
        patch_width=hd
    else:
        patch_width=pc[0][1][0]-pc[0][0][0]
        
    patch_area=patch_width*patch_height
    
    #define indices
    klimit=len(thickness)
    ilimit=vd
    jlimit=hd  
    
    slice_volumes=cell3(ilimit,jlimit,klimit)
    
    for k in range(0,klimit):
        for j in range(0,jlimit):
            for i in range(0,ilimit):
                slice_volumes[k][i][j]=patch_area*thickness[k]*10*10**-9 
                
    return slice_volumes

def buildusmatrix(x_offset=0,y_offset=0):
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
            [str(adv["estart"]),str(adv["eend"]),str(4999),"0","0","0","0"],\
            [str(reg["dist"]),xpos,ypos,str(reg["xlen"]),str(reg["ylen"]),str(reg["xdiv"]),str(reg["ydiv"])],\
            [adv["mode"],adv["method"],adv["harmonic"],"0","0","0","0"],\
            [adv["nphi"],adv["nalpha"],adv["calpha2"],adv["nomega"],adv["comega"],adv["nsigma"],"0"]]
    
    return matrix

def buildwsmatrix(x_offset=0,y_offset=0):
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

def generate_energy_axis():
    """returns x axis energy values"""
    if source=="wig":
        sdata=pickle.load(open("ws_data.pkl","rb"))
    elif source=="und":
        sdata=pickle.load(open("us_data.pkl","rb"))
    else:
        raise NameError("unknown source")
        
    g=[sdata[i][0] for i in range(0,len(sdata))]
    return g

def integrated_source_power(s_flux):
    """Finds total power in region, triple integral of power flux"""
    intpow=0
    ea=generate_energy_axis()
    for i in range(0,hd):
        for j in range(0,vd):
            for k in range(0, len(s_flux[0][0])):
                intpow+=s_flux[i][j][k]*ea[k]*1.60217646E-19
    
    return intpow

def total_integrated_power(v_power):
    """Find total power in object"""
     
    return sum(sum(sum(v_power,[]),[]))

def us(x_offset=0,y_offset=0):
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
    system(xop_path+"us.exe")
    
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
    
def patch_flux(x_offset=0,y_offset=0):
    """Runs ws() and us() depending upon the source"""
    #should i keep the ws and build matrix functions in wig and und, or move them here? decisions, decisions. resolved, moved to backend.
    if source=="wig":
        ws(x_offset,y_offset)
        f=open("ws_data.pkl","rb")
        ws_data=pickle.load(f)
        f.close()
        return [i[1] for i in ws_data]
    elif source=="und":
        us(x_offset,y_offset)
        f=open("us_data.pkl","rb")
        us_data=pickle.load(f)
        f.close()
        return [i[1] for i in us_data]
    else:
        raise NameError("unknown source")

def ws(x_offset=0,y_offset=0):
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
        system(xop_path+"ws.exe")
        
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

def slice_transmission():
    """Finds the amount of flux that passes though each slice. slice_t[i][j] j direction: energies, i direction: thickness ->2d"""       
    slice_t=[]
    #returns mu values for particular element (y values)
    f=open("mu_data\\"+mat+".pkl","rb")
    mu_data=pickle.load(f)
    f.close()
    mu_raw=[i[1] for i in mu_data]
    for i in range(0,len(thickness)):
        #locked into scan parameter of 500 min 100000 max 5000 div
        slice_t.append([math.exp(-1*thickness[i]*k) for k in mu_raw])
        
    return slice_t

def source_flux():
    """finds the energy flux in a region, through multiple calls to xop"""
    s_flux=uncorrected_flux=cell2(hd,vd)
    
    pc=patch_centers()
    ea=generate_energy_axis()
    dE=ea[1]-ea[0]
    
    for i in range(0,vd):
        for j in range(0,hd):
            x_offset=pc[i][j][0]
            y_offset=pc[i][j][1]
            s_flux[i][j]=patch_flux(x_offset,y_offset)
            
            uncorrected_flux[i][j]=s_flux[i][j]

            for k in range(0,len(ea)):
                s_flux[i][j][k]*=1000*dE/ea[k]
    write_uncorrected_flux(uncorrected_flux)        
    return s_flux

def write_uncorrected_flux(u_flux):
    """writes each power slice to the file output.csv. 3d->file"""
    #There might be an error here in the cube writing to file, y instead of z split.
    st=""
    vd=u_flux
    
    #voxel dimensions
    zlen=len(u_flux)
    ylen=len(u_flux)
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
    
def filter_flux(s_flux):
    """Finds the transmission through a filter,#I=I0*e^(-mu*t). 2d->2d"""       
    ff=open("flt.pkl","rb")
    flt_old=pickle.load(ff)
    ff.close()
    
    ea=generate_energy_axis()
    
    
    #Need to find out how to handle multiple filters. Right now, only the first filter is supported
    flt=[i for i in flt_old if i[0]!=None and i[1]!=None]
    
    #calculate filtered flux through layer
    f_flux=s_flux
    
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

def region_filtered_flux(s_flux):
        """Finds the flux through the filtered region, accounts for materials"""

        thickness_s=sum(thickness)
        reg_flux=s_flux
        
        ea=generate_energy_axis()        
        
        assert len(ea)==len(s_flux[0][0])
        
        f=open("mu_data\\"+mat+".pkl","rb")
        edata=pickle.load(f)
        f.close()
        
        for i in range(0, len(s_flux)):
            for j in range(0,len(s_flux[0])):
                for k in range(0, len(ea)):
                    reg_flux[i][j][k]*=math.exp(-1*thickness_s*mu2(edata,ea[k]))
        
        return reg_flux

def write_slice_to_table(voxel_absorbed_power_density):
    """writes each power slice to the file output.csv. 3d->file"""
    #There might be an error here in the cube writing to file, y instead of z split.
    st=""
    vd=voxel_absorbed_power_density
    
    #voxel dimensions
    zlen=len(vd)
    ylen=len(vd[0])
    xlen=len(vd[0][0])
    
    for k in range(0,zlen):
        s=""
        power_temp=cell2(xlen,ylen)        
        for i in range(0,ylen):
            for j in range(0,xlen):
                #flipdim unnecesary
                power_temp[i][j]=vd[k][i][j]
        
    
        #horizontal padding
        for i in range(0,ylen):
            power_temp[i].insert(0,0)
            power_temp[i].append(0)
            
    
        #vertical padding
        power_temp.append(cell1(xlen+2))
        power_temp.insert(0,cell1(xlen+2))
        
        
        power_temp_s=[list(map(str,i)) for i in power_temp]
        
        s+="\n".join([",".join(i) for i in power_temp_s])
        
        
        if k==0:
            st+=s
        else:
            st+="\n\n"+s
  
    f=open("output.csv","w")
    f.write(st)
    f.close()

def voxel_absorbed_flux(s_flux, slice_t):
    """Finds the power flux from source and transmission through each layer. s_flux=3d, slice_t=2d"""
    voxel_impinging_flux=cell1(len(slice_t))            #4d
    
    #calculate cumulative transmission through each layer
    
    cumulative_transmission=cell1(len(slice_t))         #2d
    cumulative_transmission[0]=cell1(len(slice_t[0]),1)
    
    for i in range(0,len(thickness)):
        j=i
        temp_transmission=cell1(len(slice_t[0]),1)
        
        while j>0:
            assert len(temp_transmission)==len(slice_t[j])
            temp_transmission=mult(temp_transmission,slice_t[j]) 
            j-=1
        cumulative_transmission[i]=temp_transmission
        
    for k in range(0, len(slice_t)):
        temp_surface=s_flux
        for i in range(0,len(s_flux[0])):
            for j in range(0, len(s_flux)):
                temp_surface[i][j]=mult(s_flux[i][j],cumulative_transmission[k])
        voxel_impinging_flux[k]=temp_surface
        
    slice_absorption=slice_t
    
    #absorption+transmission=1, 2d
    for i in range(0, len(slice_t)):
        for j in range(0, len(slice_t[0])):
            slice_absorption[i][j]=1-slice_t[i][j]
    
    voxel_absorbed_flux=cell1(len(voxel_impinging_flux))

    #print("depth of voxel_impinging_flux:\t"+str(depth(voxel_impinging_flux)))
    #print("depth of slice_absorption:\t"+str(depth(slice_absorption)))
    #print([len(voxel_impinging_flux),len(voxel_impinging_flux[0]),len(voxel_impinging_flux[0][0]),len(voxel_impinging_flux[0][0][0])])
    #print([len(slice_absorption),len(slice_absorption[0])])
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
        
    return voxel_absorbed_flux

def voxel_absorbed_power_density(v_power,slice_volumes):
    """Divide power by volume to get power density. 3d->3d"""
    
    assert len(v_power)==len(slice_volumes)
    assert len(v_power[0])==len(slice_volumes[0])
    assert len(v_power[0][0])==len(slice_volumes[0][0])
    
    #index limits
    klimit=len(thickness)
    ilimit=vd
    jlimit=hd
    
    assert len(v_power)==klimit
    assert len(v_power[0])==ilimit
    assert len(v_power[0][0])==jlimit
    
    v_power_density=cell3(ilimit,jlimit,klimit)
    
    for k in range(0,klimit):
        for j in range(0,jlimit):
            for i in range(0,ilimit):
                v_power_density[k][i][j]=v_power[k][i][j]/slice_volumes[k][i][j]
    
    return v_power_density
    
def voxel_flux_to_power(v_flux):
    """Transforms the power flux load into power. 4d->3d"""
    
    #v_flux[slice][thick][y][x] (?)
    v_power=v_flux
    ea=generate_energy_axis()
    #initialize index limits
    klimit=len(thickness) #thickness, z
    ilimit=vd             #y
    jlimit=hd             #x
    mlimit=len(ea)        #energy
    #dE=self.ea[2]-self.ea[1]
    
    #massive time draining calculations! Woohoo!
    for k in range(0,klimit):
        for j in range(0,jlimit):
            for i in range(0, ilimit):
                for m in range(0,mlimit):
                    v_power[k][i][j][m]*=ea[m]*1.60217646e-19
                    
    int_v_power=cell3(ilimit,jlimit,klimit)
    
    for k in range(0,klimit):
        for j in range(0,jlimit):
            for i in range(0,ilimit):
                #sum of spectral energies.
                int_v_power[k][i][j]=sum(v_power[k][i][j])
    
    return int_v_power

def heat_load_matrix():
        """function wrapper"""
        #Filters working improperly, huge time drains and weird results printed
        #disabled functions:
        #    filter_flux
        
        tstart=time()
        print("\n")
        s_flux=source_flux() #calculate flux in each pixel before filtering
        print("source_flux:\t\t\t\t"+str(time()-tstart)+"\n")
        
        integrated_s_power=integrated_source_power(s_flux)
        print("integrated_source_power:\t\t"+str(time()-tstart)+"\n")
        
        s="\n\n"
        s+="Integrated Source Power without filtering: "+str(integrated_s_power)+"\n"
        
        f_flux=filter_flux(s_flux)
        
        integrated_power_after_filtering=integrated_source_power(f_flux)
        s+="Integrated source power after filtering: "+str(integrated_power_after_filtering)+"\n"
        print("integrated_power_after_filtering:\t"+str(time()-tstart)+"\n")
        
        region_filtered_fluxv=region_filtered_flux(f_flux)
        print("region_filtered_flux:\t\t\t"+str(time()-tstart)+"\n")
        
        slice_transmissionv=slice_transmission()
        print("slice_transmission:\t\t\t"+str(time()-tstart)+"\n")
        
        voxel_absorbed_fluxv=voxel_absorbed_flux(f_flux,slice_transmissionv)
        print("voxel_absorbed_flux:\t\t\t"+str(time()-tstart)+"\n")
        
        voxel_absorbed_powerv=voxel_flux_to_power(voxel_absorbed_fluxv)
        print("voxel_absorbed_power:\t\t\t"+str(time()-tstart)+"\n")
        
        slice_volumesv=calc_slice_volumes()
        print("slice_volumes:\t\t\t\t"+str(time()-tstart)+"\n")
        
        voxel_absorbed_power_densityv=voxel_absorbed_power_density(voxel_absorbed_powerv, slice_volumesv)
        print("voxel_absorbed_power_density:\t\t"+str(time()-tstart)+"\n")
        
        write_slice_to_table(voxel_absorbed_power_densityv)
        print("write_slice_to_table:\t\t\t"+str(time()-tstart)+"\n")
        
        total_integrated_absorbed_power=total_integrated_power(voxel_absorbed_powerv)
        print("total_integrated_absorbed_power:\t"+str(time()-tstart)+"\n")
        
        integrated_power_after_region=integrated_source_power(region_filtered_fluxv)
        print("integrated_power_after_region:\t\t"+str(time()-tstart)+"\n")
        
        tend=time()
        dt=tend-tstart
        
        print("Total Time:\t\t\t\t"+str(dt))
        
        s+="Integrated power absorbed in the object: "+str(total_integrated_absorbed_power)+"\n"
        s+="Integrated power transmitted through the object: "+str(integrated_power_after_region)+"\n"
        s+="Elapsed time: "+str(dt)+"\n\n\n"
        s+="Here are some samples of data:\n"
        s+="\tsource flux data"+str(s_flux[0][0][3000:3010])+"\n"
        s+="\tfilter flux data"+str(f_flux[0][0][3000:3010])+"\n"
        s+="\tslice transmission"+str(slice_transmissionv[0][3000:3010])+"\n"
        s+="\tpower data:"+str(voxel_absorbed_powerv[0])+"\n"
        s+="\tpower density:"+str(voxel_absorbed_power_densityv[0])+"\n"
        
        
        f=open("heatbump_result.txt","w")
        f.write(s)
        f.close()
        print(s)
               
def main():
    """Main body of program, run source_flux on wiggler 4cells 2x2, return result and times"""
    tstart=time()
    s=""        
    s_flux=source_flux()
    tsource=time()
    s+="\nsource_flux:\t\t\t"+str(tsource-tstart)+"\n"
    print(s_flux[0][0][3000:3010])
    slice_t=slice_transmission()
    tslice=time()
    s+="slice_transmission:\t\t"+str(tslice-tstart)+"\n"
    
    """f_flux=source_flux()
    tsource=time()
    s+="\nsource_flux:\t\t\t"+str(tsource-tstart)+"\n"
    print(s_flux[0][0][3000:3010])
    slice_t=slice_transmission()
    tslice=time()
    s+="slice_transmission:\t\t"+str(tslice-tstart)+"\n"
    """
    
    v_flux=voxel_absorbed_flux(s_flux,slice_t)
    print(v_flux[0][0][0][3000:3010])
    tflux=time()
    s+="voxel_absorbed_flux:\t\t"+str(tflux-tstart)+"\n"
    
    v_power=voxel_flux_to_power(v_flux)
    print(v_power[0][0][:])
    tpower=time()
    s+="voxel_flux_to_power:\t\t"+str(tpower-tstart)+"\n"
    
    s_volumes=calc_slice_volumes()
    v_density=voxel_absorbed_power_density(v_power,s_volumes)
    print(v_density[0][0][:])
    tdensity=time()
    s+="voxel_absorbed_power_density:\t"+str(tdensity-tstart)+"\n"
    
    print(s)    

heat_load_matrix()
