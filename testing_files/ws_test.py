"""
f=open("us.out")
s=[]
for i, line in enumerate(f):
    if i>=23:
        g=line[3:26].split()
        s.append([float(x) for x in g])        
f.close()
print(s[0:2])
"""
from basic_functions import mu
import _pickle as pickle
import math


def generate_energy_axis():
    """returns x axis energy values"""
    sdata=pickle.load(open("ws_data.pkl","rb"))
    g=[sdata[i][0] for i in range(0,len(sdata))]
    return g

ea=generate_energy_axis()
ff=open("flt.pkl","rb")
flt_old=pickle.load(ff)
ff.close()

f_flux=[[[1,9,5],[4,6,5]],[[3,3,8],[2,1,0]]]
#Need to find out how to handle multiple filters. Right now, only the first filter is supported
flt=[i for i in flt_old if i[0]!=None and i[1]!=None]
del flt_old

ilimit=len(f_flux)
jlimit=len(f_flux[0])
klimit=len(f_flux[0][0])

for i in range(0,ilimit):
    for j in range(0,jlimit):
        #I=I0*e^(-mu*t)
        for k in range(0,klimit):
            f_flux[i][j][k]=f_flux[i][j][k]*math.exp(-1*mu(flt[0][0],ea[k])*flt[0][1])            

print(f_flux)