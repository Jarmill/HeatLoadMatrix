def cusum(s):
    t=0
    for i in s:
        t+=i
        yield t
        
s=[1,2,3,4,5,6]
print(list(cusum(s))[:-1])