from basic_functions import depth,matchdim
v_power=[[[1,1],[2,3]],[[1,1],[3,4]]]
area=[[2,2],[1,1]]
full_area=1
total_integrated_power2=sum(sum(sum(v_power,[]),[]))

total_integrated_power=0

klimit=len(v_power)
ilimit=len(v_power[0])
jlimit=len(v_power[0][0])
v_power2=matchdim(v_power)
for k in range(0,klimit):
    for i in range(0,ilimit):
        for j in range(0,jlimit):
            v_power2[k][i][j]=v_power[k][i][j]*(area[i][j]/full_area)
            total_integrated_power+=v_power[k][i][j]*(area[i][j]/full_area)#dA element
print(v_power)
print(v_power2)
print(total_integrated_power,total_integrated_power2)
print(depth(v_power), len(v_power),len(v_power[0]),len(v_power[0][0]))