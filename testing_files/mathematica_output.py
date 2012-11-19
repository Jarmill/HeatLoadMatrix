hr=[0.05, 0.175, 0.375, 0.625, 0.825, 0.95]
vr=[0.05, 0.175, 0.375, 0.625, 0.825, 0.95]
data=[[i,i+1,i+2,i+3,i+4,i+5] for i in range(0,6)]
#s=(",".join(["{"+str(hr[i])+","+str(vr[j])+","+str(data[j][i])+"}" for i in range(0,len(hr)) for j in range(0,len(vr))]))
s=("\n".join([str(hr[i])+"\t"+str(vr[j])+"\t"+str(data[j][i]) for i in range(0,len(hr)) for j in range(0,len(vr))]))
print(s)
with open("mathematica_output.dat","w") as f:
	f.write(s)