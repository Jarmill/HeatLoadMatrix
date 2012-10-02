import _pickle as pickle
f=open("reg.pkl","rb")
flt=pickle.load(f)
print(flt)
print("The material is: " + flt["mat"])

f.close()