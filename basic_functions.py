                                                                     
                                                                     
                                                                     
                                             
"""This program contains a series of misc functions, mostly related to data structures that are annoying in python"""
import _pickle as pickle
import bisect
# array initialization, handling
def chunks(l, n):
    """Partitions a list into n parts"""
    assert len(l)%n==0
    rowsize=len(l)//n
    return [l[i:i+rowsize] for i in range(0, len(l), rowsize)]

def depth(x):
    """Finds the dimension of an array (d=1 list, d=2 matrix, d=0 returns TypeError)"""
    j=0
    while type(x)==(list or tuple):
        j+=1
        x=x[0]
    return j   

def sum_matrix(mat):
    if depth(mat)==1:
        return sum(mat)
    else:
        accum=0
        for i in range(0, len(mat)):
            accum+=sum_matrix(mat[i])

        return accum

def print_number(num, txt):
    print(txt+' = '+str(num))
   
def print_sum_matrix(mat, txt):
    print(txt+' = '+str(sum_matrix(mat)))

def sum_matrix_by_first_dim(mat):
    retList=[]
    for i in range(0, len(mat)):
        retList.append(sum_matrix(mat[i]))

    return retList

def print_sum_matrix_by_first_dim(mat, txt, dimname):
    first_value_list=sum_matrix_by_first_dim(mat)
    for i in range(0, len(first_value_list)):
        print(txt+' '+dimname+'('+str(i+1)+') = '+str(first_value_list[i]))

def print_sum_matrix_by_layer(mat, txt):
    print_sum_matrix_by_first_dim(mat, txt, 'layer')

def test_sum_matrix_routines():
    a=[[1, [2, 3, 4], [5, 6, 7]], [2, [12, 13, 14], [15, 16, 17]]]
    print(sum_matrix([1, 2, 3]))
    print_sum_matrix(a, 'test1')
    print_sum_matrix_by_layer(a, 'test1')

# test_sum_matrix_routines()    
  

def cell1(x, n=0):
    """create empty list (array"""
    s=[n for i in range(0, x)]
    return s

def cell2(x, y, n=0):
    """create empty 2d array (matrix)"""
    s=[]
    for i in range(0, y):
        s.append([])
        for j in range(0, x):
            s[i].append(n)
    return s

def cell3(x, y, z, n=0):
    """create empty 3d array (3-rank tensor)"""
    s=[]
    for i in range(0, z):
        s.append([])
        for j in range(0, y):
            s[i].append([])
            for k in range(0, x):
                s[i][j].append(n)
    return s

def matchdim(a, n=0):
    """Creates list matching the dimension of another, filled with elements of value n"""
    try: depth(a)
    except TypeError: raise TypeError("List not passed to matchdim")
    else:
        if depth(a)==1:
            # list
            return [n for i in range(0, len(a))]
        elif depth(a)==2:
            # matrix
            return [[n for j in range(0, len(a[0]))] for i in range(0, len(a))]
        elif depth(a)==3:
            # box (3-rank)
            return [[[n for k in range(0, len(a[0][0]))] for j in range(0, len(a[0]))] for i in range(0, len(a))]
        elif depth(a)==4:
            # energy box (4-rank tensor)
            return [[[[n for m in range(0, len(a[0][0][0]))] for k in range(0, len(a[0][0]))] for j in range(0, len(a[0]))] for i in range(0, len(a))]
        else: return None  # nope! d from 1-4 only.

def ones(x): 
    """Creates square matrix full of ones""" 
    cell2(x, x, 1)

def matmult(A, B):
    """Element-wise matrix multiplication .* also works for lists"""
    # C=A
    C=matchdim(A)  # ## TESTING FIX
    for i in range(0, len(A)):
        for j in range(0, len(A[0])):
            C[i][j]=A[i][j]*B[i][j]
    return C

def listmult(A, B):
    return [A[i]*B[i] for i in range(0, len(A))]


def mu(element, x=100):
    """Linear interpolation to find the mu-transmission coefficient for a material at an energy. 100 Gev-100,000 GeV with 5000 divisions"""
    assert element in ["Ag", "Al", "Au", "Be", "Br", "C", "Co", "Cu", "Fe", "Hg", "Mn", "Ni", "Pb", "Pt", "Rb", "Se", "Si", "Ta", "Zn"]
    
    f=open("mu_data\\"+element+".pkl", "rb")
    edata=pickle.load(f)
    f.close()
    ex=[i[0] for i in edata]
    ey=[i[1] for i in edata]
    n=0
    for i in ex:
        if x<=i: break
        else: n+=1
        
    # linear interpolation (shifted line)
    m=(ey[n]-ey[n-1])/(ex[n]-ex[n-1])
    b=ey[n]
    return (x-ex[n])*m+b

def mu2(edata, x=1000):
    """Same thing as mu, except the array is passed instead of created by the function"""
    ex=[i[0] for i in edata]
    ey=[i[1] for i in edata]
    n=0
    for i in ex:
        if x<=i: break
        else: n+=1
        
    # linear interpolation (shifted line)
    m=(ey[n]-ey[n-1])/(ex[n]-ex[n-1])
    b=ey[n]
    return (x-ex[n])*m+b

def mu3(edata_energy_levels, edata_mu, energy_level):
    """Same thing as mu, except the array is passed instead of created by the function. The third version of the mu function, uses binary search to drastically cut time"""

    n=bisect.bisect_right(edata_energy_levels, energy_level);
    if n==0: n=1
    if n==len(edata_energy_levels): n=len(edata_energy_levels)-1
       
    # linear interpolation (shifted line) mx+b where m is slope and b is intercept
    m=(edata_mu[n]-edata_mu[n-1])/(edata_energy_levels[n]-edata_energy_levels[n-1])
    b=edata_mu[n]
    
    return (energy_level-edata_energy_levels[n])*m+b

def mult(A, B):
    if depth(A)==depth(B)==1:
        return listmult(A, B)
    elif depth(A)==depth(B)==2:
        return matmult(A, B)
    elif depth(A)!=depth(B):
        raise ValueError("Depth mismatch")
    else:
        raise ValueError("cannot handle list depth")

def list_str(l):
    """turn matrix into string"""
    outList=matchdim(l)
    for i in range(len(l)):
        outList[i]=str(l[i])
    return "\n".join(["".join(i)[1:-1] for i in outList])
