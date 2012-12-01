import _pickle as pickle
a=[i**2 for i in range(0,10)]
pickle.dump(a, open("test1.xspec", "wb"))
b=pickle.load(open("test1.xspec", "rb"))
print(b)