import _pickle as pickle
import time
ts=time.time()
file_path="mu_data\\"

def mu_interpolate(element,x=100):
	f=open("mu_data\\"+element+".pkl","rb")
	edata=pickle.load(f)
	f.close()
	ex=[i[0] for i in edata]
	ey=[i[1] for i in edata]
	n=0
	for i in ex:
		if x<=i: break
		else: n+=1
		
	#linear interpolation
	m=(ey[n]-ey[n-1])/(ex[n]-ex[n-1])
	b=ey[n]
	return [[ex[n],ey[n]],[ex[n-1],ey[n-1]],[ex[n]-ex[n-1],ey[n]-ey[n-1]],[m,b],(x-ex[n])*m+b]
	
	#return m*x+b
	#return ((ey[n+1]-ey[n])/(ex[n+1]-ex[n])*x+ey[n]) #linear interpolation

print(mu_interpolate("Au",85974))