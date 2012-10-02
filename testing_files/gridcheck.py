import _pickle as pickle
from rectangle_grid import pRect

fgrid=open("..\\grid_data\\grid.pkl","rb")
grid=pickle.load(fgrid)
fgrid.close()

fcenters=open("..\\grid_data\\centers.pkl","rb")
centers=pickle.load(fcenters)
fcenters.close()

fcorners=open("..\\grid_data\\corners.pkl","rb")
corners=pickle.load(fcorners)
fcorners.close()

fdimensions=open("..\\grid_data\\dimensions.pkl","rb")
dimensions=pickle.load(fdimensions)
fdimensions.close()

fareas=open("..\\grid_data\\areas.pkl","rb")
areas=pickle.load(fareas)
fareas.close()

print(grid)
print(centers)
print(corners)
print(dimensions)
print(areas)