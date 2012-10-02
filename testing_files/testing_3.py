import _pickle as pickle
from basic_functions import depth,cell1,cell2

#pickling statements, load data into voxel_impinging_flux and slice_absorption
f=open("voxel_impinging_flux.pkl","rb")
voxel_impinging_flux=pickle.load(f)
f.close()
f2=open("slice_absorption.pkl","rb")
slice_absorption=pickle.load(f2)
f2.close()

#Additional entries will be overwritten (<- heavily obfuscated language)
voxel_absorbed_flux=cell1(len(voxel_impinging_flux))

print("depth of voxel_impinging_flux:\t"+str(depth(voxel_impinging_flux)))
print("depth of slice_absorption:\t"+str(depth(slice_absorption)))
print([len(voxel_impinging_flux),len(voxel_impinging_flux[0]),len(voxel_impinging_flux[0][0]),len(voxel_impinging_flux[0][0][0])])
print([len(slice_absorption),len(slice_absorption[0])])
for k in range(0, len(voxel_impinging_flux)):
    #temp_surface 3d, initialize as empty 2d
    temp_surface=cell2(len(voxel_impinging_flux[0]),len(voxel_impinging_flux[0][0]))
    
    for i in range(0,len(voxel_impinging_flux[0])):
        for j in range(0,len(voxel_impinging_flux[0][0])):
            #??? voxel_impinging_flux length KABOOM BANG ZOOM IMPLOSION BOOM!
            #print(voxel_impinging_flux)
            #print(type(voxel_impinging_flux[k][i][j]))
            #print(type(slice_absorption[k]))
            #print(voxel_impinging_flux[k][i][j][3000:3020])
            #print(slice_absorption[k][3000:3020])
            temp_surface[i][j]=[voxel_impinging_flux[k][i][j][m]*slice_absorption[k][m] for m in range(0, len(slice_absorption[k]))]
    voxel_absorbed_flux[k]=temp_surface
f3=open("voxel_absorbed_flux.pkl","wb")
pickle.dump(voxel_absorbed_flux,f3)
f3.close
print("voxel_impinging_flux:\t"+str(voxel_impinging_flux[0][0][0][3000:3010]))
print("slice_absorption:\t"+str(slice_absorption[0][3000:3010]))
print("voxel_absorbed_flux:\t"+str(voxel_absorbed_flux[0][0][0][3000:3010]))