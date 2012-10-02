from time import time
from basic_functions import chunks, matchdim
ts=time()

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
    def __str__(self):
        return "dim=({self.h},{self.v}) center=({self.cx},{self.cy}) corner=({self.x},{self.y})".format(self=self)

class pc():
    def __init__(self,LIP):
        self.hd=4
        self.vd=4
        self.h=1
        self.v=1
        self.d=.1
        self.LIP=True
        self.setup()
    def setup(self,):
        """dodge the diamond of death, one level up"""
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
                
            #sum lists up, find corners
            xl=list(cusum(hl))[:-2]
            yl=list(cusum(vl))[:-2]
            
            #generate and partition rectangles
            grid=[pRect(hl[i+1],vl[j+1],xl[i],yl[j]) for i in range(0,len(xl)) for j in range(0,len(yl))]
            grid2=chunks(grid,self.vd+2)
        else:
            hl=list(cusum([0]+[l]*(self.hd)))[:-1]
            vl=list(cusum([0]+[w]*(self.vd)))[:-1]
            grid=[pRect(l,w,i,j) for i in hl for j in vl]
            grid2=chunks(grid,self.vd)
        self.grid=grid2
        
    def centers(self):
        centers=matchdim(self.grid)
        for i in range(0,len(self.grid)):
            for j in range(0,len(self.grid[0])):
                r=self.grid[i][j]
                centers[i][j]=(r.cx,r.cy)
        return centers
    def corners(self):
        corners=matchdim(self.grid)
        for i in range(0,len(self.grid)):
            for j in range(0,len(self.grid[0])):
                r=self.grid[i][j]
                corners[i][j]=(r.x,r.y)
        return corners   
    def dim(self):     
        dim=matchdim(self.grid)
        for i in range(0,len(self.grid)):
            for j in range(0,len(self.grid[0])):
                r=self.grid[i][j]
                dim[i][j]=(r.h,r.v)
        return dim
    def areas(self):
        areas=matchdim(self.grid)
        for i in range(0,len(self.grid)):
            for j in range(0,len(self.grid[0])):
                r=self.grid[i][j]
                areas[i][j]=(r.h*r.v)
        return areas   
    def rgrid(self): 
        return self.grid
    
        
        
        
"""
a=pRect(.5,3,4,1)
print(a.cx)
print(str(a))
"""
p=pc(True)
g=p.rgrid()

#s="\n".join([",".join([str(i) for i in g[j]]) for j in range(0,len(g))])
#print(s)


print(len(g),len(g[0]))
print("centers\t",p.centers())
print("corners\t",p.corners())
print("dimensions",p.dim())
print("areas\t",p.areas())


print(time()-ts)
