hd=2
vd=2
h=2
v=2
mat="Al"
thickness=[10,50,100]
source="wig"
xop_path="C:\\Users\\Public\\Documents\\xop2.3\\bin.x86\\"

from basic_functions import mu
import megatest
import math
from time import time

def region_filtered_flux(s_flux):
        """Finds the flux through the filtered region, accounts for materials"""

        thickness_s=sum(thickness)
        reg_flux=s_flux
        
        ea=megatest.generate_energy_axis()        
        assert len(ea)==len(s_flux[0][0])
        for i in range(0, len(s_flux)):
            for j in range(0,len(s_flux[0])):
                for k in range(0, len(ea)):
                    reg_flux[i][j][k]*=math.exp(-1*thickness_s*mu(mat,ea[k]))
        
        return reg_flux


tstart=time()
s=megatest.source_flux()
r=megatest.filter_flux(s)
print(r)
print(time()-tstart)
print([len(r),len(r[0]),len(r[0][0])])