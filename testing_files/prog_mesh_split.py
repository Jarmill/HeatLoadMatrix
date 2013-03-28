x_split=[1, 2, 0, 0, 1, 1]  # the number of splits per interval, n-1 numbers
xpar=[0, 0.01, 4.25, 8.5, 12.75, 16.99, 17]  # the partition, n numbers
y_split=[1, 0, 0, 0, 1, 1]
ypar=[0, 0.01, 4.25, 8.5, 12.75, 16.99, 17]
dxchain=[[xpar[i+1]-(xpar[i+1]-xpar[i])/(x_split[i]+1)*(j+1) for j in range(x_split[i])] for i in range(len(xpar)-1)]
dychain=[[ypar[i+1]-(ypar[i+1]-ypar[i])/(y_split[i]+1)*(j+1) for j in range(y_split[i])] for i in range(len(ypar)-1)]

# Objective: add x_split[i] values between between xpar[i+1] and xpar[i].
s_flux=([[100]*6])*6
# current non-working code:

x_index=1
for i in reversed(range(len(x_split))):
    for k in dxchain[i]:
        s_flux[i].insert(i, 0)
        xpar.insert(i+1, k)

newlen=len(s_flux[0])
for i in reversed(range(len(y_split))):
    s_flux.insert(i, [0]*newlen)
    for k in dychain[i]:
        ypar.insert(i+1, k)
        
print(xpar)
print(ypar)
print(s_flux)
