import copy
import numpy
import math
def standard_tabs(alph,skew,shape):
   
    #make skew shape and shape have same length
    while len(skew)<len(shape):
        skew.append(0)


    #initialize list with one element composed of a tableau with len(shape) empty rows
    empty_tab=[]
    for i in range(len(shape)):
        empty_tab+=[[]]
    pos=[]
    tab_list=[    [     empty_tab,    pos   ]     ]
    
    
    #Create all tableaux by successively adding each n from 0 to alph-1 to a new box or a terminal box
    for n in range(alph):
        new_list=[]
        for i in range(len(tab_list)):
            tab=tab_list[i][0]
            positions=tab_list[i][1]
            
            for j in range(len(tab)):
                #try to add n to last box of row j of ith tableau in current list 

                if len(tab[j])>0:
                    if j==len(tab)-1 or len(tab[j+1])==0 or (skew[j]+len(tab[j])>skew[j+1]+len(tab[j+1])+1):
                        t_cop=copy.deepcopy(tab) 
                        t_cop[j][-1]+=[n]
                        new_position=[j,skew[j]+len(t_cop[j])+j]
                        new_list.append([t_cop,positions+[new_position]])

                #also try to add new box to row j
                if len(tab[j])<shape[j]-skew[j]:
                    if j==0 or skew[j]+len(tab[j])+1<skew[j-1]+len(tab[j-1]):
                        t_cop=copy.deepcopy(tab) 
                        t_cop[j]+=[[n]]
                        new_position=[j,skew[j]+len(t_cop[j])+j]
                        new_list.append([t_cop,positions+[new_position]])
                    

        tab_list=new_list

    P=[]
    #Check that the final shape is correct
    for g in range(len(tab_list)):
        tab=tab_list[g]
        diags=0
        same_shape=True
        for h in range(len(shape)):
            if len(tab[0][h])!=shape[h]-skew[h]:
                same_shape=False

        if same_shape==True:
            #compute the peak sets and repeat sets for each tableau
            peak_set=[]
            repeat_set=[]
            positions=tab[1]
            for i in range(0,len(positions)-2):
                j=i+1
                k=i+2
                if positions[j][1]>positions[i][1] and positions[k][0]>positions[j][0]:
                    peak_set.append(j)
                if positions[i]==positions[j] and positions[k][0]>positions[j][0]:
                    peak_set.append(j)
                if positions[j][1]>positions[i][1] and positions[j]==positions[k]:
                    peak_set.append(j)
                if positions[i]==positions[j] and positions[j]==positions[k]:
                    peak_set.append(j)
            for i in range(0,len(positions)-1):
                if positions[i]==positions[i+1]:
                    if positions[i][0]==positions[i][1]-1:
                        repeat_set.append(-i-1)
                    if positions[i][0]!=positions[i][1]-1:
                        repeat_set.append(i+1)
            for i in range(0,len(positions)):
                if positions[i][0]==positions[i][1]-1:
                    diags+=1
            P.append([tab[0],peak_set,repeat_set,diags])
                    
    return(P)




def partitions(n,k):
    #Returns list of all partitions of n into at most k parts
    par_list=[[1]]
    while sum(par_list[0])<n:
        new_list=[]
        for i in range(0,len(par_list)):
            par=par_list[i]
            if len(par)==1 or (len(par)>1 and par[-1]<par[-2]):
                p_cop=copy.copy(par)
                p_cop[-1]+=1
                new_list.append(p_cop)
            if len(par)<k:
                p_cop=copy.copy(par)
                p_cop.append(1)
                new_list.append(p_cop)
        par_list=new_list
    return(par_list)
                

def polynomial(TAB,num_vars):
    #Returns the list of partitions that appear in the quasisymmetric polynomial associated to a given tableau
    V=[]
    maxi=0
    tab=TAB[0]
    peak_set=TAB[1]
    repeat_set=TAB[2]
    diags=TAB[3]
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            maxi+=len(tab[i][j])

    pars=partitions(maxi,num_vars)

    for i in range(0,len(pars)):
        par=pars[i]
        weak_seq=[]
        for j in range(0,len(par)):
            weak_seq+=[j+1]*par[j]
        power_of_two=len(par)-diags
        good=True

        for j in range(0,len(weak_seq)-2):
            if weak_seq[j]==weak_seq[j+1] and weak_seq[j+1]==weak_seq[j+2] and j+1 in peak_set:
                good=False                         
        for k in range(0,len(weak_seq)-1):
            if weak_seq[k]==weak_seq[k+1] and -k-1 in repeat_set:
                good=False
            if weak_seq[k]==weak_seq[k+1] and k+1 in repeat_set:
                power_of_two-=1

                
              
                
                
        if good==True:

            V+=[par]*int(math.pow(2,power_of_two))
    return(V)



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
    

def monomial_exp(degree,skew,shape,num_vars):
    #Compute a homogeneous degree part of GR_{shape/skew} as a linear combination of monomial symmetric functions
    tabs=standard_tabs(degree,skew,shape)

    P=[]
    for i in range(0,len(tabs)):
        P+=polynomial(tabs[i],num_vars)
    GR=distinct_elements(P)
    return(GR)
    



import math 


   


def sequences(length,maxi):
    #create list of all sequences of fixed length using numbers {0,...,maxi}
    seq_list=[[]]
    while len(seq_list[0])<length:
        new_list=[]
        for i in range(0,len(seq_list)):
            seq=seq_list[i]
            for j in range(0,maxi+1):
                seq_j=seq+[j]
                new_list.append(seq_j)
        seq_list=new_list
    return(seq_list)



def row(m,n):
    #create list of all one-row shifted set-valued tableau of length m and max entry n
    #We use the representation 1'-->1, 1-->2, 2'-->3, 2-->4, etc
    row_tabs=[[]]
    while len(row_tabs[0])<m:
        new_tabs=[]
        for i in range(0,len(row_tabs)):
            row=row_tabs[i]
            previous=1
            if len(row)>0:
                previous=row[-1][-1]
            #create a list of 0-1 sequences representing all possible subsets of {previous,previous+1,...,2n}
            bit_strings=sequences(2*n+1-previous,1)
            for j in range(0,len(bit_strings)):
                b=bit_strings[j]
                subset=[]
                for k in range(0,len(b)):
                    if b[k]==0:
                        subset.append(k+previous)
                if len(subset)>0 and (previous%2==0 or previous<subset[0] or len(row)==0):
                    #add subset in next box of row
                    new_tabs.append(row+[subset])
        row_tabs=new_tabs
    return(row_tabs)


               
def over (top_row,bottom_row,offset):
    #determine if the two row tableau [top_row,bottom_row] (shifted by offset) is valid
    ok=True
    for i in range(0,len(top_row)):
        top=top_row[i]
        bot=[float('inf')]
        if 0<=i+offset<len(bottom_row):
            bot=bottom_row[i+offset]
        if max(top)>min(bot):
            ok=False
        if max(top)==min(bot) and max(top)%2==0:
            ok=False
    return(ok)    
                
def flag(mu,lam):
    #return all shifted set-valued tableau of shape lam/mu such that entries in row i are <=i
    
    #make partitions have same length
    while len(mu)<len(lam):
        mu.append(0)
        
    flag_tabs=[]
    #initialize flag_tabs to the set of one-row tableau in the alphabet {1',1}
    R1=row(lam[0]-mu[0],1)
    for i in range(0,len(R1)):
        flag_tabs.append([R1[i]])
        
    #add additional rows    
    for j in range(2,len(lam)+1):
        new_tabs=[]
        R=row(lam[j-1]-mu[j-1],j)
        for p in range(0,len(flag_tabs)):
            for q in range(0,len(R)):
                f=flag_tabs[p]
                last_row=f[-1]
                new_row=R[q]
                #check if adding this new row is valid
                if over(last_row,new_row,mu[j-2]-1-mu[j-1])==True:
                    new_tabs.append(f+[new_row])
        flag_tabs=new_tabs
    return(flag_tabs)





            
            
def read_w(P):
    #return reading word: increasing within boxes; left to right within rows; bottom to top row
    r=[]
    for i in range(len(P)-1,-1,-1):
        for j in range(0,len(P[i])):
            for k in range(0,len(P[i][j])):
                r.append(P[i][j][k])
    return(r)
                




def no_prime_diag(P,diags):
    good=True
    for i in range(0,len(P)):
        if i in diags:
            row=P[i]
            box=row[0]
            for k in range(0,len(box)):
                if box[k]%2==1:
                    good=False                        
    return(good)


def back(P):
    #define the reverse reading word of a shifted SVT
    backword=[]
    #read top row to bottom row
    for i in range(0,len(P)):
        row=P[i]
        #read right to left within rows
        for j in range(len(row)-1,-1,-1):
            box=copy.copy(row[j])
            #within a box, read primed entries first, in decreasing order, and then unprimed entries, in decreasing order
            box.sort(key=lambda x: -(x%2)+1/x)
            backword+=box
    return(backword)


def forw(P):
    #define the forwards reading word of a shifted SVT (different from read_w())
    forword=[]
    #read bottom row to top row
    for i in range(len(P)-1,-1,-1):
        row=P[i]
        #read left to right within rows
        for j in range(0,len(row)):
            box=copy.copy(row[j])
            #within a box, read unprimed entries first, in decreasing order, and then primed entries, in decreasing order
            box.sort(key=lambda x: (x%2)+1/x)
            forword+=box
    return(forword)


def latt(P):

    #Does the tableau P have the lattice property?
    counts=[0]*9
    #counts[i] is the is a statistic about the appearances of i and i' as we read the backword and then the forword
    backword=back(P)
    forword=forw(P)

    #read through the backword
    for j in range(0,len(backword)):
        elem=backword[j]
        base=math.ceil(elem/2)
        #while reading the backword add 1 to counts[i] each time you read an i
        if elem%2==0:
            counts[base]+=1
            #if counts[i] becomes greater than counts[i-1] return false
            if base>1 and counts[base]>counts[base-1]:
                return False
        if elem%2==1:
            #if you read an i' while counts[i] equals counts[i-1] return false
            if base>1 and counts[base]==counts[base-1]:
                return False  
    #read through the forword
    for j in range(0,len(forword)):
        elem=forword[j]
        base=math.ceil(elem/2)
        #while reading the forword add 1 to counts[i] each time you read an i'
        if elem%2==1:
            counts[base]+=1
            #if counts[i] becomes greater than counts[i-1] return false
            if base>1 and counts[base]>counts[base-1]:
                return False
        if elem%2==0:
            #if you read an i while counts[i+1] equals counts[i] return false
            if base>0 and counts[base+1]==counts[base]:
                return False          
    return(True)



 
def weights(w):
    counts=[]
    for q in range(0,9):
        counts.append(0)
    for i in range(0,len(w)):
        con=math.ceil(w[i]/2)-1
        counts[con]+=1
    return(counts)
                        



def GR_expand(skew,shape):
    diags=[]
    while len(skew)<len(shape):
        skew.append(0)
    for i in range(len(shape)):
        if skew[i]==0:
            diags.append(i)
    #Write a skew GR as a sum of non-skew GRs
    #Find all the shape/skew shifted SVT with the lattice property
    F=flag(skew,shape)
    W=[]

    for i in range(0,len(F)):
        tab=F[i]
        #Is the first i or i' an i in read_w(tab)? Does tab with first i replaced by i' have the lattice property?
        if no_prime_diag(tab,diags)==True and latt((tab))==True:

            W.append(weights(read_w(tab)))
            #Record the weights of these tableaux
            if weights(read_w(tab))[0:3]==[3,1,0]:
                print(tab)

    W=distinct_elements(W)
    W.sort(key=lambda x: str(x[1]))
    W.reverse()
    return(W)


def list_expand(List,degree,num_vars):
    #Given a list of GRs with multiplicity find the monomial expansion of the corresponding linear combination
    exp=[]
    for i in range(len(List)):
        multiplicity=List[i][0]
        shape=List[i][1]
        #The |shape| must be at most the degree to contribute
        if sum(shape)<=degree:
            #Write the GR_{shape} itself as a linear combination of monomial symmetric functions
            M=monomial_exp(degree,[],shape,num_vars)
            for j in range(len(M)):
                #Add each partition in this linear combination its coefficient times multiplicity many times
                mult_prod=M[j][0]*multiplicity
                partition=M[j][1]
                exp+=[partition]*mult_prod
    EXP=distinct_elements(exp)
    return(EXP)




def compare(degree,skew,shape,num_vars):
    M=monomial_exp(degree,skew,shape,num_vars)
    print(M)
    #M is the homogeneous part of given degree of GR_{shape/skew} in num_vars variables computed directly 
    G=GR_expand(skew,shape)
    print(G)
    L=list_expand(G,degree,num_vars)
    #L is (supposedly) the same thing computed using the expansion, G, of GR_{shape/skew} into shifted shape GRs

    print(L)
    return(M==L)



