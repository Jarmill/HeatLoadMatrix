import json
import _pickle as pickle
for i in ["adv","flt","reg","run","und","wig"]:
    with open("..\\pickle\\"+i+".pkl","rb") as f, open("..\\pickle\\"+i+".json","w") as g:
        data=pickle.load(f)
        json.dump(data,g,indent=2)
print("done")