from basic_functions import cell2, cell1

voxel_absorbed_power_density=[[[3,4,9],[2,1,0],[6,4,5],[7,7,3]],[[8,1,1],[0,2,7],[1,8,6],[0,6,4]],[[5,4,4],[7,3,2],[9,5,1],[3,1,5]]]
st=""
a=[]
vd=voxel_absorbed_power_density
print(vd)
print([len(vd),len(vd[0]),len(vd[0][0])])
print("\n")
zlen=len(vd)
ylen=len(vd[0])
xlen=len(vd[0][0])
for k in range(0,zlen):
    s=""
    #power_temp=cell2(len(vd[0]),len(vd[0][0]))
    #for i in range(0,len(vd[0])):
    #    for j in range(0,len(vd[0][0])):
    power_temp=cell2(xlen,ylen)        
    for i in range(0,ylen):
        for j in range(0,xlen):
            #flipdim unnecesary
            power_temp[i][j]=vd[k][i][j]
            #power_temp[i][j]=vd[len(vd)-i-1][j][k]
            
    
    #horizontal padding
    for i in range(0,ylen):
        power_temp[i].insert(0,0)
        power_temp[i].append(0)
    #vertical padding
    power_temp.insert(0,cell1(xlen+2))
    power_temp.append(cell1(xlen+2))

    
    power_temp_s=[list(map(str,i)) for i in power_temp]

    s+="\n".join([",".join(i) for i in power_temp_s])


    if k==0:
        st+=s
    else:
        st+="\n\n"+s
"""
f=open("output.csv","w")
f.write(st)
f.close()
"""
print (st)