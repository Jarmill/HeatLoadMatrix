import _pickle as pickle
file_path="E:\\"

elem=["Ag","Al","Au","Be","Br","C","Co","Cu","Fe","Hg","Mn","Ni","Pb","Pt","Rb","Se","Si","Ta","Zn"]


for i in elem:
	lt=[]
	ct=""
	f=open(file_path+i+".txt","r")
	fr=f.readlines()
	f.close()
	fsp=[j.split() for j in fr]
	for j in fsp:
		lt.append([float(k) for k in j])
	fp=open(file_path+i+".pkl","wb")
	pickle.dump(lt,fp)
	fp.close()

	s="\n".join([",".join(j.split()) for j in fr])
	fc=open(file_path+i+".csv","w")
	fc.write(s)
	fc.close()