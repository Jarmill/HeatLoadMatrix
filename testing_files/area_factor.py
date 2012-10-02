import _pickle as pickle
h=1
v=1
hd=2
vd=2
fareas=open("..\\grid_data\\areas.pkl","rb")
areas=pickle.load(fareas)
fareas.close()

print(areas)
fullarea=(h/hd)*(v/vd)
for i in range(0,len(areas)):
    for j in range(0,len(areas[0])):
        areas[i][j]/=fullarea
print(areas)