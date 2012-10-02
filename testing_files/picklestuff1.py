import _pickle as pickle
usdata={"title":"","energy":"5.3","current":"250","sigx":"1.070","sigy":".081","sigx1":".1433","sigy1":".0135","ky":"2.350","kx":"0","period":"2.44","num":"40"}

f=open("und_default.pkl","wb")
pickle.dump(usdata,f)
f.close()


