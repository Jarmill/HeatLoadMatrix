from basic_functions import depth
"""
hd=10
vd=10
h=1
v=1

def patch_centers(x_offset=0,y_offset=0):
        Calculates Centers of rectangular cells
        #create empty array
        patch=cell2(hd,vd)
                
        for i in range(0,vd):
            for j in range(0,hd):
                x=(2*j-1)*h/(2*hd)+x_offset+h/hd
                y=v+y_offset+(3-2*i)*v/(2*vd)-2*v/vd
                patch[i][j]=[x,y]        
        return patch
    
pc=patch_centers()

hr=[i[0] for i in pc[0]]
vr=[pc[m][1][1] for m in range(0,len(pc))]
hr.sort()
vr.sort()
print(hr)
print(vr)


#print(frange(500,100000,5000)[3000:3010])
f=open("raw_flux.pkl","rb")
g=pickle.load(f)
print(g)
f.close()
"""
a=2
b=[1,2]
c=[[1,2],[3,4]]
#print(depth(a))
print(depth(b))
print(depth(c))