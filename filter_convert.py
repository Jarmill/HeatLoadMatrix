import os
import _pickle as pickle
import csv
class cubic_spline():
    def __init__(self, x, y):
        self.x=x
        self.y=y
        # write rest of interpolation here
        # self.M=[[1,1],[2,4]]
        n=len(self.x)
        b=d=[0]*n
        a=c=[0]*(n-1)
        """
        for i in range(n-1):
            if y[i] == y[i+1]:
                y[i+1] *= 1e-10 * y[i]
        """

        # set up intermediate diagonal values
        b[0]=2/(x[1]-x[0])
        b[n-1]=2/(x[n-1]-x[n-2])
        d[0]=3*(y[1]-y[0])/(x[1]-x[0])**2
        d[n-1]=3*(y[n-1]-y[n-2])/(x[n-1]-x[n-2])**2
        for i in range(1, n-1):
            b[i]=2*(1/(x[i]-x[i-1])+1/(x[i+1]-x[i]))
            d[i]=3*((y[i]-y[i-1])/(x[i]-x[i-1])**2+(y[i+1]-y[i])/(x[i+1]-x[i])**2)

        # set up off diagonal points
        for i in range(n-1):
            a[i]=c[i]=1/(x[i+1]-x[i])

        k=self.band_solve(a, b, c, d)

        self.k=k

    def binary_search(self, l, first, last, key):
        # Return index to the left of insertion
        mid=(first+last)/2
        while first<=last and l[mid]!=key:
            if l[mid]>key:
                last=mid-1
            else:
                first=mid+1
            mid=(first+last)/2
        return mid

    def band_solve(self, a, b, c, d):
        """solve the tridiagonal matrix to generate k values"""
        n=len(d)
        # len(b) = n, len(a) = len(c) = n-1
        c[0]/=b[0]
        d[0]/=b[0]
        c+=[0]
        """
        print a[0], "\t", b[0], "\t\t", d[0]
        for j in range(1,n-1):
            print a[j], "\t", b[j], "\t", c[j], "\t", d[j]
        print "\t", b[n-1], "\t", c[n-1], "\t", d[n-1]
        """
        # forward cancellation
        for i in range(n):
            denom=b[i]-(a[i]*c[i-1])
            if denom==0:
                print(b[i], "- (", a[i], "*", c[i-1], ") = 0, line ", i)
            c[i]/=denom
            d[i]=(d[i]-a[i]*d[i-1])/denom

        # back substitution
        k=[0]*n
        k[n-1]=d[n-1]
        for i in reversed(range(n-1)):
            k[i]=d[i]-c[i]*k[i+1]

        return k

    @property
    def n(self):
        return len(self.x)

    def interp(self, xt):
        """execute cubic spline at x value xt"""
        index=self.binary_search(self.x, 0, len(self.x), xt)
        y1=self.y[index]
        y2=self.y[index+1]
        x1=self.x[index]
        x2=self.x[index+1]

        a=self.k[index]*(x2-x1)-(y2-y1)
        b=-self.k[index+1]*(x2-x1)+(y2-y1)
        t=(xt-x1)/(x2-x1)

        ans=(-2*a+b)*t**2+(a-b)*t**3+(a-y1+y2)*t+y1
        return ans

    def add(self, num):
        n=len(self.x)
        x0, xn=self.x[0], self.x[n-1]
        xa=[x0+i*float((xn-x0))/(num+1) for i in range(1, num+1)]
        ya=[]

        xo=[]
        yo=[]
        i=0
        j=0

        for k in range(len(xa)):
            ya.append(self.interp(xa[k]))
            while i<n and j<len(ya):
                # print self.x[i], "\tvs\t", xa[j]
                if self.x[i]<xa[j]:
                    xo.append(self.x[i])
                    yo.append(self.y[i])
                    i+=1
                elif self.x[i]==xa[j]:
                    xo.append(xa[j])
                    yo.append(ya[j])
                    j+=1
                    i+=1
                else:
                    xo.append(xa[j])
                    yo.append(ya[j])
                    j+=1

        while i<n:
            xo.append(self.x[i])
            yo.append(self.y[i])
            i+=1

        
        return [xo, yo]

    def __call__(self, other):
        return self.interp(other)

files=["mu_data_2\\"+i for i in os.listdir("mu_data_2") if i[-3:]=="pkl"]
for i in files:
    print(i)
    with open(i, "rb") as f1:
        elem=pickle.load(f1)
    s=cubic_spline(elem[0], elem[1])
    k=s.k
    n_elem=[elem[0], elem[1], k]
    st=""
    for j in range(len(n_elem[0])):
        st+=str(n_elem[0][j])+"\t"+str(n_elem[1][j])+"\t"+str(n_elem[2][j])+"\n"
    with open(i, "wb") as f2, open(i[:-4]+".csv", "w") as fc:
        fc.write(st)
        pickle.dump(n_elem, f2)
    del s
    
print(files)
