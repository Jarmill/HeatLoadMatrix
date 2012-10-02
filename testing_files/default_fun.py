import _pickle as pickle
f=open("..\\pickle\\wig_default.pkl","wb")
w={"energy":"5.3","current":"250","period":"12","num":"49","kx":"0","ky":"9","title":""}
#u=pickle.load(f)
pickle.dump(w,f)
f.close()
#print(u)