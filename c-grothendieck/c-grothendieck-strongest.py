import copy
import math
import time




#creates W such that (for i<=length) W[i][j][1] is the jth (lexographically) word of length i that in the alphabet
#{0,1,...,largest} that has no consecutive entries equal.  W[i][j][0] is the associated permutation.
def word_list(length,largest):
    ind=[]
    for i in range(1,largest+2):
        ind.append(i)
    W=[[[ind,[]]]]
    while len(W[-1][0][1])<length:
        new_W=[]
        for i in range(0,len(W[-1])):
            word=W[-1][i][1]
            perm=copy.copy(W[-1][i][0])
            for j in range(0,largest+1):
                if len(word)==0 or word[-1]!=j:
                    word_j=word+[j]
                    perm_j=Hecke(j,perm)
                    new_W.append([perm_j,word_j])
        W.append(new_W)

    return(W)





#Creates a dictionary where the keys are permutations.  Gives each permutation an attribute  called 'words' 
#where the value of 'words' is the set of all words for that permutation in the alphabet {0,1,...,largest}, 
#with length at most max_length, and no consecutive entries equal 
def create_perm_dict(max_length, largest):
    W=word_list(max_length, largest)
    X=[]
    for i in range(1,len(W)):
        X+=W[i]
    X.sort(key=lambda x: str(x[0]))   
    Y={}
    for i in range(0,len(X)):
        if i==0 or X[i][0]!=X[i-1][0]:
            Y.update({str(X[i][0]):{'words':[]}})
            Y[str(X[i][0])]['words'].append(X[i][1])            
        if i>0 and X[i][0]==X[i-1][0]:
            Y[str(X[i][0])]['words'].append(X[i][1])       
    return(Y)



#Takes the perm_dict and gives each permutation an attribute called 'peaksets.'  The value of 'peaksets' is a list
#with one entry, K, for each word in 'words.' K[0] is the length of the word and K[1:len(K)] the peak set. 
def add_peaks(Y):
    for perm in Y:
        W=Y[perm]['words']
        P=[]
        for i in range(len(W)):
            w=W[i]
            peaks=[len(w)]
            for j in range(1,len(w)-1):
                if w[j-1]<w[j] and w[j]>w[j+1]:
                    peaks.append(j)
            P.append(peaks)
        P.sort(key=lambda x: str(x))
        Y[perm].update({"peaksets":P})
    return(Y)

#Takes the perm_dict and gives each permutation an attribute called 'tabs.'  The value of 'tabs' is a list
#with one entry, T, for each word in 'words' that is a the reading word for a valid unimodal tableau. The value of 
#T is the associated tableau.   
def add_Htabs(Y):
    for perm in Y:
        W=Y[perm]['words']
        T=[]
        for i in range(len(W)):
            w=W[i]
            t=Hecke_tab(w)
            if t!=[]:
                T.append(t)
        Y[perm].update({"tabs":T})
    return(Y)        
        
    
    
def add_tabpeaks(max_length,Y):
    Q=create_Qdict(standard_tabs(max_length))
    for perm in Y:
        T=Y[perm]['tabs']
        P=[]
        tabpeaks=[]
        for i in range(len(T)):
            t=T[i]
            shape=[]
            for j in range(len(t)):
                shape.append(len(t[j]))
            tabpeaks+=Q[str(shape)]['peaksets']
        tabpeaks.sort(key=lambda x: str(x))
        Y[perm].update({'tabpeaks':tabpeaks})
            
    return(Y) 



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


#This is the condition that adjacent rows in the conjectured definition of Hecke tableaux must satisfy.
#The row a lies on top of the row b. The function returns true this is a valid two-row unimodal tableau.
def colreq(b,a):
    if len(a)<=len(b):
        return(False)
    B=copy.copy(b)
    A=copy.copy(a)
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

    if abs(B[len(B)-1])>=abs(A[0]):
        return(False)
    if abs(B[0])>=abs(A[0]):
        return(False)
           
    for i in range(0,len(B)):
        if A[i+1]>B[i]:
            for j in range(i+1,len(B)):
                if B[i]  < B[j]  < A[i+1]   or   B[i] <  -B[j] <   A[i+1]:
                    return(False)
                if B[j]==A[i+1] or B[j]==-A[i+1]:
                    return(False)                          
                        
            for k in range(0,i+1):
                if B[i]  < A[k]  < A[i+1]   or   B[i] <  -A[k] <   A[i+1]:
                    return(False)
                if A[k]==-A[i+1] or A[k]==A[i+1]:
                    return(False)
    return(True)



#This is the condition that an individual row in the conjectured definition of Hecke tableau must satisfy.
#It returns true if the row is a valid hook.
def hook(A):
    good=False
    if len(A)>0:
        good=True
        mindex=0
        for i in range(0,len(A)):
            if A[i]==min(A):
                mindex=i
        for i in range(0,mindex):
            if A[i]<=A[i+1]:
                return(False)
        for i in range(mindex,len(A)-1):
            if A[i]>=A[i+1]:
                return(False)
    return(good)

def Hecke_tab(w):
    #Given a word, w, returns the shape of the unique Hecke tab (if it exists) with that reading word. Otherwise returns []
    T=[]
    remainder=copy.copy(w)
    while hook(remainder)==False:
        i=1
        while hook(remainder[i:len(remainder)+1])==False:
            i+=1
        if max(remainder[0:i])>=max(remainder[i:len(remainder)+1]):
            return([])
        T.append(remainder[i:len(remainder)+1])

        remainder=remainder[0:i]
        if len(T)>1 and colreq(T[-1],T[-2])==False:
            return([])      
    T.append(remainder)
    if len(T)>1 and colreq(T[-1],T[-2])==False:
        return([])
    return(T)


#Returns list of all strict partitions of n
def strict_parts(n):
    par_list=[[1]]
    while sum(par_list[0])<n:
        new_list=[]
        for i in range(0,len(par_list)):
            par=par_list[i]
            if len(par)==1 or (len(par)>1 and 1+par[-1]<par[-2]):
                p_cop=copy.copy(par)
                p_cop[-1]+=1
                new_list.append(p_cop)
            if par[-1]>1:
                p_cop=copy.copy(par)
                p_cop.append(1)
                new_list.append(p_cop)
        par_list=new_list
    return(par_list)



#Creates a list where TABS where TABS[i][j] represents data for the jth (under some order) standard shifted set valued
#tableau with entries {0,1...,i} for each i<max_length.  TABS[i][j][0] is the tableau itself. TABS[i][j][1] records 
#the positions of its entries.  TABS[i][j][2] the number of entries and the peak set.  TABS[i][j][3] records the shape.
def standard_tabs(max_length):
   
    TABS=[ [  [[],[],[],[]] ]  ]
        

    for n in range(max_length):
        small_tabs=TABS[-1]
        big_tabs=[]
        for i in range(len(small_tabs)):
            tab=small_tabs[i][0]
            positions=small_tabs[i][1]
            peakset=small_tabs[i][2]
            shape=small_tabs[i][3]
            for j in range(len(tab)):
                #try to add n to last box of row j of ith tableau in current list 
                if n-1 not in tab[j][-1] and (j==len(tab)-1 or len(tab[j])>1+len(tab[j+1])):
                    t_cop=copy.deepcopy(tab)
                    p_cop=copy.copy(positions)
                    k_cop=copy.copy(peakset)
                    t_cop[j][-1]+=[n]
                    new_position=[j,len(t_cop[j])-1+j]
                    p_cop+=[new_position]
                    if len(positions)>1 and positions[-2][1]<positions[-1][1] and positions[-1][0]<new_position[0]:
                        k_cop+=[n-1]
                    big_tabs.append([t_cop,p_cop,k_cop,shape])

                #also try to add new box to row j
                if j==0 or 1+len(tab[j])<len(tab[j-1]):
                    t_cop=copy.deepcopy(tab) 
                    p_cop=copy.copy(positions)
                    k_cop=copy.copy(peakset)
                    s_cop=copy.deepcopy(shape)
                    t_cop[j]+=[[n]]
                    new_position=[j,len(t_cop[j])-1+j]
                    p_cop+=[new_position]
                    if len(positions)>1 and positions[-2][1]<positions[-1][1] and positions[-1][0]<new_position[0]:
                        k_cop+=[n-1]
                    s_cop[j]+=1
                    big_tabs.append([t_cop,p_cop,k_cop,s_cop])

                    
            #also try to create new row
            if len(tab)==0 or len(tab[-1])>1:
                t_cop=copy.deepcopy(tab) 
                t_cop+=[[[n]]]
                p_cop=copy.copy(positions)
                k_cop=copy.copy(peakset)
                s_cop=copy.deepcopy(shape)
                new_position=[len(t_cop)-1,len(t_cop)-1]
                p_cop+=[new_position]
                if len(positions)>1 and positions[-2][1]<positions[-1][1] and positions[-1][0]<new_position[0]:
                    k_cop+=[n-1] 
                s_cop+=[1]
                big_tabs.append([t_cop,p_cop,k_cop,s_cop])


        TABS.append(big_tabs)
                    
    return(TABS)


#Given a set of standard shifted SVTs, creates a dictionary where the keys are the partitions associated to each shape
#appearing in the list.  Give each partition an attribute 'peaksets' whose value is a list where there is an element K
#for each tableau of the given shape appearing in the original list.  K[0] is the number of entries in that tableau, 
#and K[1:len(K)] its peakset
def create_Qdict(T):
    X=[]
    for i in range(0,len(T)):
        for j in range(0,len(T[i])):
            X.append([T[i][j][3],[i]+T[i][j][2]])
    X.sort(key=lambda x: str(x[0]))
    Y={}        
    for i in range(0,len(X)):
        if i==0 or X[i][0]!=X[i-1][0]:
            Y.update({str(X[i][0]):{'peaksets':[]}})
            Y[str(X[i][0])]['peaksets'].append(X[i][1])            
        if i>0 and X[i][0]==X[i-1][0]:
            Y[str(X[i][0])]['peaksets'].append(X[i][1])       
    return(Y)


#Given a list of words, returns the list of all words which are a valid reading word for a Hecke tableau of specified shape.
def HeckeTabs(H):
    U=[]
    
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


#Checks if the conjecture is true for all signed permutations p of [1,2,...,largest+1] for all lengths l from 
#{inv(p),...,max_length}  (l is the length of the (non)reduced words we consider, equivalently the number of entries
#in the standard shifted SVTs we consider and inv(p) is the inversion number, i.e., length of a reduced word for p.)
#returns: [number of permutations where conjecture is (nontrivially) true, number where false] 
def uni_con(max_length,largest):
    t0=time.time()
    P=create_perm_dict(max_length,largest)
    t1=time.time()
    print(t1-t0)
    K=add_peaks(P)
    t2=time.time()
    print(t2-t1)
    H=add_Htabs(K)
    t3=time.time()
    print(t3-t2)
    T=add_tabpeaks(max_length,H)
    t4=time.time()
    print(t4-t3)
    good=0
    bad=0
    for perm in T:
        if T[perm]['peaksets']==T[perm]['tabpeaks']:
            good+=1
        else:
            bad+=1
    t5=time.time()
    print(t5-t4)
    return([good, bad])

uni_con(11,4)