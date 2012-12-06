from basic_functions import chunks, matchdim
import _pickle as pickle
from os import path, makedirs
#this wil become much simpler after numpy
#need to implement progressive meshing.
def cusum(s):
    t=0
    for i in s:
        t+=i
        yield t

class pRect():
    def __init__(self,h,v,x,y):
        self.h=h
        self.v=v
        self.x=x
        self.y=y
        self.cx=x+h/2
        self.cy=y+v/2
    __public__=["h","v","x","y","cx","cy"]
    def __str__(self):
        return "dim=({self.h},{self.v}) center=({self.cx},{self.cy}) corner=({self.x},{self.y})".format(self=self)

class pc():
    def rect_initialize(self):
        """only used for testing, if run through rectangle_grid.py"""
        self.h=1
        self.v=1
        self.d=.1
        self.hd=5
        #self.hd=5
        self.vd=5
        #self.vd=4
        self.LIP=True
        self.thickness=[1,2]
        self.title="rect_grid_test"
    def rect_setup(self):
        """dodge the diamond of death, one level up. set up rectangle handling"""
        #length and width of each division, assuming constant
        l=self.h/self.hd
        w=self.v/self.vd
        if self.LIP==True:
            #set horizantal lip
            if self.hd>=2:
                hl=[0,self.d,l-self.d]+[l]*(self.hd-2)+[l-self.d,self.d,0]
            elif self.hd==1:
                hl=[0,self.d,l-2*self.d,self.d,0]
            #set vertical lip
            if self.vd>=2:
                vl=[0,self.d,w-self.d]+[w]*(self.vd-2)+[w-self.d,self.d,0]
            elif self.vd==1:
                vl=[0,self.d,w-2*self.d,self.d,0]

            #print('hl=', hl)
            #print('vl=', vl)

            #sum lists up, find corners
            xl=list(cusum(hl))[:-2]
            yl=list(cusum(vl))[:-2]

            #print('cusum(hl)=', list(cusum(hl)))
            #print('xl=', xl)

            #print('cusum(vl)', list(cusum(vl)))
            #print('yl=', yl)

            #generate and partition rectangles
            grid=[pRect(hl[i+1],vl[j+1],xl[i],yl[j]) for i in range(0,len(xl)) for j in range(0,len(yl))]
            grid2=chunks(grid,self.hd+2)
        else:
            hl=list(cusum([0]+[l]*(self.hd)))[:-1]
            vl=list(cusum([0]+[w]*(self.vd)))[:-1]
            grid=[pRect(l,w,i,j) for i in hl for j in vl]
            grid2=chunks(grid,self.vd)  ### TESTING FIX????? Make this HD?
        self.grid=grid2

        #generate further arrays for storage, (corners, centers,areas,dimensions)
        centers=matchdim(grid2)
        corners=matchdim(grid2)
        areas=matchdim(grid2)
        dimensions=matchdim(grid2)

        for i in range(0,len(grid2)):
            for j in range(0,len(grid2[0])):
                r=grid2[i][j]
                centers[i][j]=(r.cx,r.cy)
                corners[i][j]=(r.x,r.y)
                dimensions[i][j]=(r.h,r.v)
                areas[i][j]=r.h*r.v
        if __name__=="__main__":
            print(centers)
            print(corners)
            print(dimensions)
            print(areas)
            print(grid2[0][0])
        self.centers=centers
        self.corners=corners
        self.dimensions=dimensions
        self.areas=areas

    def rect_centers(self): return self.centers

    def rect_corners(self): return self.corners

    def rect_dimensions(self): return self.dimensions

    def rect_areas(self): return self.areas

    def rect_grid(self): return self.grid

    def rect_center_x(self):
        #print(self.grid)
        #return [str(i[0]) for i in self.grid]
        return [i[0].cx for i in self.grid]

    def rect_center_y(self):
        return [i.cy for i in self.grid[0]]



if __name__=="__main__":
    p=pc()
    p.rect_initialize()
    p.rect_setup()
    print(p.rect_center_x())
    print(p.rect_center_y())
    print("rect run.")