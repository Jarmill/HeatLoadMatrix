from basic_functions import chunks
import _pickle as pickle

class pctest():
    def __init__(self):
        self.d=.1
        self.h=1
        self.hd=8
        self.v=1
        self.vd=6
        return
    def patch_centers2(self):
        """Creates partitioned (2d) list of coordinates of sampled points, with an interpolation guard (lip)"""
        def cusum(s):
            t=0
            for i in s:
                t+=i
                yield t
        
        lx=self.h/self.hd
        ly=self.v/self.vd
        
        n=self.hd*self.vd+2*(self.vd+self.hd)+4
        
        if self.hd==1:
            dx=[self.d/2,(lx-self.d)/2,(lx-self.d)/2,self.d/2]
        if self.hd==2:
            dx=[self.d/2,lx/2,lx-self.d,lx/2,self.d/2]
        else:
            dx=[self.d/2,lx/2,lx-self.d/2]+[lx]*(self.hd-3)+[lx-self.d/2,lx/2,self.d/2]
            
        if self.vd==1:
            dy=[self.d/2,(ly-self.d)/2,(ly-self.d)/2,self.d/2]
        if self.vd==2:
            dy=[self.d/2,ly/2,lx-self.d,ly/2,self.d/2]
        else:
            dy=[self.d/2,ly/2,ly-self.d/2]+[ly]*(self.vd-3)+[ly-self.d/2,ly/2,self.d/2]
        x=list(cusum(dx))[:-1]
        y=list(cusum(dy))[:-1]
        
        patch=[(i,j) for i in x for j in y]
        assert n==len(patch)
        print(x)
        print(y)
        print(str(n)+" points\n"+str(len(x))+" x points\n"+str(len(y))+" y points")
        print
        f=open("pc_test.pkl","wb")
        pickle.dump(patch,f)
        f.close()
        patch=chunks(patch,self.vd+2)
        return patch

pc=pctest()
pc.patch_centers2()