import copy
import math


#Creates a list of all words of a specified length using integers from 0 up to largest.
def words(length,largest):
    HW=[[]]
    while len(HW[0])<length:
        hw=[]
        for i in range(0,len(HW)):
            hi=HW[i]
            for j in range(0,largest+1):
                hij=hi+[j]
                hw.append(hij)
        HW=hw
    return(HW)

#Creates a list of lists of all words using integers from 0 up to largest for each length from 1 up to max_length.
def all_words(max_length,largest):
    W=[]
    for i in range(1,max_length+1):
        W.append(words(i,largest))
    return(W)

#Applies the Hecke operation associated to the index i to the permutation PP.
def Hecke(i,PP):
    P=copy.copy(PP)
    if i==0 and P[0]>0:
        P[i]=-P[i]
    if i>0 and P[i-1]<P[i]:
        j=i-1
        pi=P[i]
        pj=P[j]
        P[i]=pj
        P[j]=pi
    return(P)


#Given a word applies (left to right) the Hecke operators associated to each letter to the indentity permutation
def permute(w):
    ind=[1,2,3,4,5,6,7,8,9]
    for i in range(0,len(w)):
        ind=Hecke(w[i],ind)
    return(ind)


#Creates a list of tuples where the first entry is a word and the second entry is the associated permutation
#Groups together pairs which have the same permutation.  
def createX(max_length, largest):
    W=all_words(max_length, largest)
    X=[]
    for i in range(0,len(W)):
        w=W[i]
        x=[]
        for j in range(0,len(w)):
            x.append([w[j],permute(w[j])])
        X+=x
    X.sort(key=lambda x: str(x[1]))
    return(X)
        


#This is the condition that adjacent rows in the conjectured definition of Hecke tableaux must satisfy.
#(The row A lies on top of the row B)
def colreq(B,A):
    for i in range(0,len(B)):
        if B[i]==min(B):
            bindex=i
    for i in range(0,bindex+1):
        B[i]=-B[i]
    for i in range(0,len(A)):
        if A[i]==min(A):
            aindex=i
    for i in range(0,aindex):
        A[i]=-A[i]
    good=1
    if len(B)>0:
        if len(A)<=len(B):
            good=0
        if len(A)>len(B):

            if abs(B[len(B)-1])>=abs(A[0]):
                good=0
            if abs(B[0])>=abs(A[0]):
                good=0
           
            for i in range(0,len(B)):
                if A[i+1]>B[i]:
                    for j in range(i+1,len(B)):
                        if B[i]  < B[j]  < A[i+1]   or   B[i] <  -B[j] <   A[i+1]:
                            good=0
                        if B[j]==A[i+1] or B[j]==-A[i+1]:
                            good=0  
                        
                        
                    for k in range(0,i+1):
                        if B[i]  < A[k]  < A[i+1]   or   B[i] <  -A[k] <   A[i+1]:
                            good=0
                        if A[k]==-A[i+1] or A[k]==A[i+1]:
                            good=0
    return(good)



#This is the condition that an individual row in the conjectured definition of Hecke tableau must satisfy.
def hook(A):
    good=0
    if len(A)>0:
        good=1
        mindex=0
        for i in range(0,len(A)):
            if A[i]==min(A):
                mindex=i
        for i in range(0,mindex):
            if A[i]<=A[i+1]:
                good=0
        for i in range(mindex,len(A)-1):
            if A[i]>=A[i+1]:
                good=0
    return(good)





#Given a list of words, returns the list of all words which are a valid reading word for a Hecke tableau of specified shape.
def HeckeTabs(H,shape):
    V=[]
    d=[]
    for k in range(0,len(shape)+1):
        d.append(sum(shape[0:k]))
    for i in range(0,len(H)):
        good=1
        h=H[i]
        T=[]
        for j in range(0,len(shape)):
            if j<len(shape)-1:
                B=(h[d[j]:d[j+1]])
                A=(h[d[j+1]:d[j+2]])
                if hook(B)==0 or hook(A)==0 or colreq(B,A)==0:
                    good=0
            if j==len(shape)-1:
                B=(h[d[j]:d[j+1]])
                if hook(B)==0:
                    good=0
        if good==1:
            V.append(h)
    return(V)

# Given a strict partition, returns the partitions attained by adding one entry to a shifted set tableau of shape par.
def children(par):
    C=[]
    for i in range(0,len(par)):
        if i==0 or par[i]<par[i-1]-1:
            c=copy.copy(par)
            c[i]+=1
            C.append(c)
    if par[len(par)-1]>1:
        c=copy.copy(par)
        c.append(1)
        C.append(c)
    for i in range(0,len(par)):
        if i==len(par)-1 or par[i]>par[i+1]+1:
            c=copy.copy(par)
            C.append(c)
    return(C)


#Creates a list of the shapes of all shifted set tableaux with no more than 'length' entries        
def createT(length):
    Sizes=[[],[[1]]]
    for i in range(2,length+1):
        nex=[]
        las=Sizes[i-1]
        for j in range(0,len(las)):
            p=las[j]
            nex+=children(p)
        Sizes.append(nex)
    return(Sizes)
        

#Given, H, the list of all words of at most a specified length for a fixed permutation
#And T, the shapes (with multiplicity), of all partitions coprresponding to a shifted set tableau with 'length' entries
#Returns: First entry is a representative for the permutation
#Second entry is the number of pairs of Hecke tableaux and shifted set tableaux (with 'length' entries) for that permutation
#Third entry is the number of Hecke words of the specified length
def check(H,T):
    nn=0
    for i in range(0,len(T)):
        tab=T[i][1]
        mult=T[i][0]
        rs=sum(tab)
        bat=copy.copy(tab)
        bat.reverse()
        V=HeckeTabs(H[rs],bat)
        nn+=len(V)*mult
    return([H[len(H)-1][0],nn,len(H[len(H)-1])])
    

#Given a list returns a list of distinct elements with multiplicity.    
def distabs(W):
    U=[[1,W[0]]]
    for i in range(1,len(W)):
        toadd=W[i]
        spot=-1
        for j in range(0,len(U)):
            if U[j][1]==toadd:
                spot=j
        if spot>=0:
            U[spot][0]+=1
        if spot==-1:
            U.append([1,toadd])
        U.sort(key=lambda x: x[0])
    return(U)



#For each permutation with inversion number at most 'length' prints the result of check()
#The second two number should always be the same if the conjecture holds
#Returns [number of permutations where conjecture holds, number of permutations where conjecture fails]
def all_check(length,largest):
    T=createT(length)
    T=distabs(copy.deepcopy(T[length]))  
    X=createX(length,largest)
    G=[]

    current=X[0][1]
    i=0
    while i<len(X):
        H=[]
        for f in range(0,length+1):
            H.append([])
        while i<len(X) and current==X[i][1]:
            L=len(X[i][0])
            H[L].append(X[i][0])
            i+=1
        g=check(H,T) 
        G.append(g)
        print(g)
        if i<len(X):
            current=X[i][1]
        
    same=0
    different=0
    for i in range(0,len(G)):
        if G[i][1]==G[i][2]:
            same+=1
        if G[i][1]!=G[i][2]:
            different+=1
        
    return([same,different])

all_check(8,4)