"""
This is testing code to create the partition, compatible with progressive meshing.
"""

from basic_functions import chunks, matchdim

def cusum(l):
    o=[]
    s=0
    o.append(0)
    for i in range(1, len(l)):
        s+=l[i]
        o.append(s)
    return o

class pc2():
    def rect_initialize(self):
        """only used for testing, if run through rectangle_grid.py"""
        self.h=1
        self.v=1
        self.d=.01
        self.hd=5
        # self.hd=5
        self.vd=5
        # self.vd=4
        self.LIP=True
        self.thickness=[1, 2]
        self.title="rect_grid_test"
        
    def rect_setup(self):
        """dodge the diamond of death, one level up. set up rectangle handling"""
        # length and width of each division, assuming constant
        l=self.h/self.hd
        w=self.v/self.vd
        self.xpar=[]
        self.ypar=[]
        
        if self.LIP==True:
            # set horizantal lip
            if self.hd>=2:
                hl=[0, self.d, l-self.d]+[l]*(self.hd-2)+[l-self.d, self.d]
            elif self.hd==1:
                hl=[0, self.d, l-2*self.d, self.d]
            # set vertical lip
            if self.vd>=2:
                vl=[0, self.d, w-self.d]+[w]*(self.vd-2)+[w-self.d, self.d]
            elif self.vd==1:
                vl=[0, self.d, w-2*self.d, self.d]
            hl=cusum(hl)
            vl=cusum(vl)
        else:
            hl=cusum([0]+[l]*(self.hd))
            vl=cusum([0]+[w]*(self.vd))
        self.xpar=hl
        self.ypar=vl
        self.rect_param()
    
    def rect_areas(self):
         return [[(self.xpar[i+1]-self.xpar[i])*(self.ypar[j+1]-self.ypar[j]) for i in range(len(self.xpar)-1)] for j in range(len(self.ypar)-1)]
    
    def rect_dim_x(self):
        return [self.xpar[i+1]-self.xpar[i] for i in range(len(self.xpar)-1)]    
    
    def rect_dim_y(self):
        return [self.ypar[i+1]-self.ypar[i] for i in range(len(self.ypar)-1)]
    
    def rect_dimensions(self):
        return [[(self.xpar[i+1]-self.xpar[i], self.ypar[j+1]-self.ypar[j]) for i in range(len(self.xpar)-1)] for j in range(len(self.ypar)-1)]
    
    def rect_center_x(self):
        return [(self.xpar[i+1]+self.xpar[i])/2 for i in range(len(self.xpar)-1)]
    
    def rect_center_y(self):
        return [(self.ypar[i+1]+self.ypar[i])/2 for i in range(len(self.ypar)-1)]

    def rect_centers(self):
        return [[((self.xpar[i+1]+self.xpar[i])/2, (self.ypar[j+1]-self.ypar[j])/2) for i in range(len(self.xpar)-1)] for j in range(len(self.ypar)-1)]
    
    def rect_param(self):
        self.centers=self.rect_centers()
        self.areas=self.rect_areas()
        self.dimensions=self.rect_dimensions()
    
    def __repr__(self):
        return "X coord:\t"+str(self.xpar)+"\nY coord:\t"+str(self.ypar)
    
if __name__=="__main__":
    p=pc2()
    p.rect_initialize()
    p.rect_setup()
    print(p)
    print(p.rect_areas())
    print(p.rect_centers())
    print(p.rect_dimensions())
