#We use position coordinates to define Dyck paths in this code
import copy
import math

#Define basic statistics
def alpha(a,b,m):
    if a<=b:
        return(min(b-a,m))
    if a>b:
        return(min(a-b-1,m))
    
def alpha0(a,m):
    return(max(0,a-m))

def degr(A,m):
    d=0
    for i in range(1,len(A)):
        for j in range(i,len(A)): 
            d+=alpha(A[i],A[j],m)
    for k in range(2,len(A)):
        d-=alpha0(A[k],m)
    return(d)
        
def area(A):
    return(sum(A))

def point(A,m):
    for i in range(len(A)-1,-1,-1):
        if A[i]-A[len(A)-1]>-m:
            pt=i
    return(pt)

def rightable(A,m):
    r=False
    pt=point(A,m)
    pr=pair(A,m)
    if pt<=pr+1 and pt<len(A)-1:
        r=True
    return(r)

def leftable(A,m):
    l=False
    pr=pair(A,m)
    if A[len(A)-1]-A[pr+1]>=-m-1 and A[pr+1]>0:
        l=True
    return(l)
        
def pair(A,m):
    pr=len(A)-2
    for i in range(len(A)-3,-1,-1):
        if A[i]-A[i+2]>=-m and A[i+1]!=0:
            pr=i
    return(pr)

#Define right and left
def right(A,m):
    pt=point(A,m)
    pr=pair(A,m)
    if pt<=pr+1 and pt<len(A)-1:
        B=A[0:pt+1]
        B+=[A[len(A)-1]+1]
        B+=A[pt+1:len(A)-1]
        return(B)
    if pt>pr+1 or pt==len(A)-1:
        return(A)
    
def left(A,m):
    pr=pair(A,m)
    if A[len(A)-1]-A[pr+1]>=-m-1 and A[pr+1]>0:
        B=A[0:pr+1]
        B+=A[pr+2:len(A)]
        B+=[A[pr+1]-1]   
        return(B)
    if A[len(A)-1]-A[pr+1]<-m-1:
        return(A)






#Define lowest    
def lowest(A,m):
    Record=[]
    B=None
    while A!=B:
        B=A
        A=right(A,m)
        Record.append(A)
    return(A)

#Define height of A to be height of P such that f(g(P))=A
def height(A):
    mx=0
    j=0
    for i in range(0,len(A)):
        if A[i]>=mx:
            mx=A[i]
            j=i
    return((mx-1)*(len(A)-1)+j-sum(A))
            
#Generate all elements of D_lm with degree <= dstar
def generate_D(l,m,dstar):
    X=[[0]]
    while len(X[0])<l+1:
        Y=[]
        for i in range(0,len(X)):
            x=X[i]
            last=x[len(x)-1]
            for j in range(0,last+m+1):
                if degr(x+[j],m)<=dstar:
                    Y.append(x+[j])
        X=Y
    Z=[]
    for u in range(0,len(X)):
        if degr(X[u],m)==dstar:
            Z.append(X[u])
    Z.sort(key=sum)
    return(Z)

#Generate all elements of T_lm with degree <= dstar 
def generate_T(l,m,dstar):
    X=[[0,0]]
    while len(X[0])<l+1:
        Y=[]
        for i in range(0,len(X)):
            x=X[i]
            last=x[len(x)-1]
            for j in range(0,last+m+1):
                if degr(x+[j],m)<=dstar:
                    Y.append(x+[j])
        X=Y
    Z=[]
    S=[]
    for u in range(0,len(X)):
        if degr(X[u],m)==dstar:

            Z.append((X[u]))
            S.append(sum(X[u]))
    Z.sort(key=sum)

    S.sort()

    return(Z)

#Generate all elements of T_lm with degree <= dstar 
def generate_S(l,m,dstar):
    X=[[0,0]]
    while len(X[0])<l:
        Y=[]
        for i in range(0,len(X)):
            x=X[i]
            last=x[len(x)-1]
            for j in range(0,last+m+1):
                if degr(x+[j],m)<=dstar:
                    Y.append(x+[j])
        X=Y
    Z=[]
    S=[]
    for u in range(0,len(X)):
        if degr(X[u]+[0],m)==dstar:

            Z.append((X[u]+[0]))
            S.append(sum(X[u]))
    Z.sort(key=sum)

    S.sort()

    return(Z)

        
# Check if string of A is not too long
def string_okay(A,m):
    M=m*len(A)*(len(A)-1)/2
    h=height(A)
    d=degr(A,m)
    B=lowest(A,m)
    if sum(B)<=M-h-d:
        return(True)
    if sum(B)>M-h-d:
        return(False)
    
# For given m, check if strings are okay  
def strings_okay(m):
    m_is_ok=True
    if m>1:
        lstar=12-m
        dstar=10*m-m*m
    if m==1:
        lstar=22
        dstar=20
    T=generate_T(lstar,m,dstar)
    for j in range(0,len(T)):
        if string_okay(T[j],m)==False:
            m_is_ok=False
    print('m=' +str(m)+ ' is ok')
    return(m_is_ok)


# For all m, check if strings are okay 
def all_strings_okay():
    all_ok=True
    for m in range(1,11):
        if strings_okay(m)==False:
            all_ok=False
    if all_ok==True:
        print('All are ok!')
    return(all_ok)
    
def sort_rule(X):
    return(X[1]+X[0]/1000)


# For a given l and m and dstar test the conjecture 

def conjecture(l,m,dstar):
    L=[]
    M=m*(l+1)*(l)/2
    T=generate_T(l,m,dstar)
    Plus=[]
    Minus=[]
    for i in range(0,len(T)):
        a=sum(T[i])
        d=degr(T[i],m)
        if a<=M-a-d:
            for j in range(a,int(M-a-d+1)):
                Plus.append([j,d])
        if M-a-d<a:
            for j in range(int(M-a-d+1),a):
                Minus.append([j,d])
                
    D=generate_D(l,m,dstar)
    All=[]
    for i in range(0,len(D)):
        a=sum(D[i])
        d=degr(D[i],m)
        All.append([a,d])
    print(len(Plus))
    print(len(Minus))
    print(len(All))
    All_Minus=All+Minus
    Plus.sort(key=sort_rule)
    All_Minus.sort(key=sort_rule)
    if Plus==All_Minus:
        print('m=' + str(m) + ', l=' + str(l) + ' is ok')
    return(Plus==All_Minus)

    
    
# For a given m test the conjecture for all l<=lstar

def conjectures(m):
    lstar=0
    m_is_ok=True
    if m>1:
        lstar=12-m
        dstar=10*m-m*m
    if m==1:
        lstar=22
        dstar=20
    for l in range(1,lstar+1):
        if conjecture(l,m,dstar)==False:
            m_is_ok=False
    if m_is_ok==True:
        print('m=' +str(m)+ ' is okay!')
    return(m_is_ok)
    
    
# Test the conjecture for all l<=lstar
   
def all_conjectures():
    all_ok=True
    for m in range(10,0,-1):
        if conjectures(m)==False:
            all_ok=False
    if all_ok==True:
        print('Everything is okay!!!')
    return(all_ok)

def set_minus(A,B):
    C=[]
    for i in range(0,len(A)):
        if A[i] not in B:
            C.append(A[i])
    return(C)


def distinct_elements(W):
    W.sort(key=lambda x: str(x))
    U=[[1,W[0]]]
    for i in range(1,len(W)):
        if W[i]==W[i-1]:
            U[-1][0]+=1
        else:
            U.append([1,W[i]])
    U.reverse()
    return(U)















def poss_right(x,m):
    Y=[]
    for i in range(1,len(x)-1):
        for j in range(i+1,len(x)):
            if x[i-1]-x[j]-1>=-m: 
                if x[j]+1-x[i]>=-m:
                    if j==len(x)-1 or x[j-1]-x[j+1]>=-m:
                        y=x[0:i]+[x[j]+1]+x[i:j]+x[j+1:len(x)]
                        if degr(x,m)==degr(y,m) and y not in Y:
                            Y.append(y)
    for i in range(1,len(x)):
        if x[i-1]-x[i]-1>=-m:
            y=x[0:i]+[x[i]+1]+x[i+1:len(x)]
            if degr(x,m)==degr(y,m) and y not in Y:
                Y.append(y)                                  
    return(Y)




def cover(A,B):
    maxi=max(max(A),max(B))
    weight_A=[0]*(maxi+1)
    weight_B=[0]*(maxi+1)
    for a in A:
        weight_A[a]+=1
    for b in B:
        weight_B[b]+=1
    diff=0
    for i in range(0,len(weight_A)):
        if weight_A[i]!=weight_B[i]:
            diff+=1
    return(diff)

def adjacency(X,Y):
    AD=[]
    for x in X:
        ad_x=[]
        for y in Y:
            if cover(x,y)==2:
                ad_x.append(1)
            else:
                ad_x.append(0)
        AD.append([x,ad_x])
    AD.sort(key = lambda x: str(x[1]))
    AD.sort(key = lambda x: sum(x[1]))
    return(AD)
                
    
    
def all_right(X,Y):
    rX=[]
    uX=[]
    uY=[]
    for x in X:
        if right(x,m)!=x:
            rX.append(right(x,m))
        else:
            uX.append(x)
    for y in Y:
        if y not in rX:
            uY.append(y)
    if len(uX)>0:
        print(uX)
        print(uY)
        print("---------")
    return 0 
    
def bysum(linear):
    Grouped=[[linear[0]]]
    for i in range(1,len(linear)):
        if sum(linear[i])==sum(linear[i-1]):
            Grouped[-1].append(linear[i])
        else:
            Grouped.append([linear[i]])
    return(Grouped)
    
    
def matchings(AD):
    dim=len(AD)
    M=[[]]
    for row in AD:
        new_M=[]
        for m in M:
            for i in range(0,len(row[1])):
                if row[1][i]==1 and i not in m:
                    new_M+=[m+[i]]
        M=new_M
    return(M)

def clean(AD):
    n=len(AD)
    for j in range(0,n):
        some=0
        last=0
        for i in range(0,n):
            some+=AD[i][1][j]
            if AD[i][1][j]==1:
                last=i
        if some==1:
            zeros=[0]*n
            zeros[j]=1
            AD[i][1]=copy.copy(zeros)
    return(AD)

def match_exist(AD,stop):
    attempts=0
    n=len(AD)
    index=0
    perm=[]
    while index<len(AD) and attempts<stop:
        #create ones
        ones=[]
        for i in range(0,n):
            if i not in perm and AD[index][1][i]==1:
                ones.append(i)
        ##################
        if len(ones)>0:
            r=math.floor(random.random()*len(ones))
            perm.append(ones[r])
            index+=1
        else:
            index=0
            perm=[]
            attempts+=1
    if attempts>=stop:
        print("uh-oh")
    print(attempts)
    return(perm)
        
        
    