from time import time
from basic_functions import chunks,cell3

class pc_test():
    def __init__(self):
        self.hd=3
        self.vd=3
        self.h=1
        self.v=1
        self.thickness=[.01]
        self.d=.1

    def patch_centers2(self,x_offset=0,y_offset=0):
        """Calculates Centers of rectangular cells. The number of cells is h*v+2(h+v)+4"""
    
        n=self.hd*self.vd+2*(self.hd+self.vd)+4
        """
        #interior centers
        x=[(2*j-1)*self.h/(2*self.hd)+x_offset+self.h/self.hd for j in range(0,self.hd)]
        y=[self.v+y_offset+(3-2*i)*self.v/(2*self.vd)-2*self.v/self.vd for i in range(0,self.vd)]
        
        #add points on edges, xedge yedge
        xedge=[0]+x+[self.h]
        yedge=[0]+y+[self.v]
        """
        #combine into coordinates
        x=[self.d/2+self.h*n/self.hd for n in range(0,self.hd+2)]
        y=[self.d/2+self.v*n/self.vd for n in range(0,self.vd+2)]
        patch=[(i,j) for i in x for j in y]

        assert n==len(patch)
        patch=chunks(patch,self.vd+2)
        return patch
    def calc_slice_volumes(self):
        """Calculates the volume of each cell/voxel. Right now, progressive meshing is not supported by this model, these are constant lengths/widths"""
        pc=self.patch_centers2()
        """
        if self.vd==1:
            patch_height=self.v
        else:
            patch_height=abs(pc[1][1][1]-pc[2][1][1])
        
        if self.hd==1:
            patch_width=self.hd
        else:
            patch_width=abs(pc[1][2][1]-pc[1][1][1])
        """
        #define the width and height of each cell. Progressive meshing will involve non-constant measurements.
        patch_height=self.v/self.vd
        patch_width=self.h/self.hd
        
        patch_area=patch_width*patch_height
        
        #define indices
        klimit=len(self.thickness)
        ilimit=self.hd+2
        jlimit=self.vd+2  
        
        slice_volumes=cell3(jlimit,ilimit,klimit)
        print((klimit,ilimit,jlimit))
        print(len(slice_volumes),len(slice_volumes[0]),len(slice_volumes[0][0]))
        for k in range(0,klimit):
            for j in range(0,jlimit):
                for i in range(0,ilimit):
                    #W/mm^2->W/m^2
                    slice_volumes[k][i][j]=patch_area*self.thickness[k]*10*(10**-9)
        print(pc) 
        print(slice_volumes)     
ts=time()
p=pc_test()
print(p.patch_centers2())
#print(p.calc_slice_volumes())
print(time()-ts)