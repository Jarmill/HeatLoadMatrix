print("Testing simultaneous files")
for i in range(1,10):
    f1=open("blah.txt","w")
    f1.write(str(i)+" "+str(i-1))
    f2=open("blah.txt","r")
    print(str(i)+":"+str(f2.readline()))
    f2.close()
    f1.close()
input("")

ff=open("blah.txt","r")
print(ff.readlines())
ff.close()