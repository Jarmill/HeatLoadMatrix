import rectangle_grid
from basic_functions import cell1, list_str,depth
from copy import deepcopy
from os import makedirs, path

class bump_output(rectangle_grid.pc):
    def output_initialize(self):
        """pseudo-constructor"""
        self.rect_initialize()
        self.power_grid=[[[10,9,8,7,6],[8,7,6,5,4],[6,5,4,3,2],[4,3,2,1,0]],
                         [[10,9,8,7,6],[8,7,6,5,4],[6,5,4,3,2],[4,3,2,1,0]]]
    def write_slice_to_table(self):
        """writes file. hr goes on top, vr goes on left"""
        pgrid=deepcopy(self.power_grid)
        
        hr=[0]+self.rect_center_x()+[self.h]
        vr=[0]+self.rect_center_y()+[self.v]
        #print(hr,len(hr),depth(hr))
        #print(vr,len(vr),depth(vr))
        print ('hr=', hr)
        print ('vr=', vr)
        s=""
        #loop through slices (thicknesses) 
        for k in range(0,len(pgrid)):
            #top, bottom zeroes
            #pgrid[k]=[cell1(len(pgrid[k]))]+pgrid[k]+[cell1(len(pgrid[k]))]
            pgrid[k]=[cell1(len(pgrid[k])+1)]+pgrid[k]+[cell1(len(pgrid[k])+1)]  ### TESTING FIX
            #left, right zeroes, with y axis labels
            #print(len(pgrid[k]),len(vr))
            for i in range(len(pgrid[k])):
                pgrid[k][i]=[vr[i]]+[0]+pgrid[k][i]+[0]
            #x axis labels
            hr2=[self.thickness[k]]+hr
            pgrid[k]=[hr2]+pgrid[k]
            s+=list_str(pgrid[k])+"\n\n"
            
        print(s)
        
        if self.title=="":
            self.title="output"
            
        outputfile="write_slice_output\\"+self.title+".csv"
        
        outputfile_d=path.dirname(outputfile)
        
        if not path.exists(outputfile_d):
            makedirs(outputfile_d)
        
        f=open(outputfile,"w")
        f.write(s)
        f.close()
    def write_to_mathematica(self):
        """writes to a mathematica ListPlot3D format"""
        hr=self.rect_center_x()
        vr=self.rect_center_y()
        print(hr)
        print(vr)
        print(self.power_grid)
        print(len(hr),len(vr), len(self.power_grid[0]),len(self.power_grid[0][0]))
        s=[("{"+str(hr[j])+","+str(vr[i])+","+str(self.power_grid[0][i][j])+"}") for i in range(0,len(vr)) for j in range(len(hr))]
        sl="{"+",".join(s)+"}"
        f=open("mathematica_output.txt","w")
        f.write(sl)
        f.close()
    
if __name__=="__main__":
    b=bump_output()
    b.output_initialize()
    b.rect_setup()
    b.write_to_mathematica()