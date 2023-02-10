import math

#This the code needed to complete the proofs of Lemma 2 and Lemma 3 of Section 9 of https://arxiv.org/pdf/2208.00577.pdf
#We use position coordinates (See the beginning of Section 4) to define Dyck paths in this code





#DEFINITIONS----------------------------------------------------------------------

#Define the basic statistics needed to define degree (See Definition 2 of Section 4)
def alpha(a,b,m):
    if a<=b:
        return(min(b-a,m))
    if a>b:
        return(min(a-b-1,m))

def alpha0(a,m):
    return(max(0,a-m))


#Define the point and pair maps (See definitions 5 and 6 of section 4)
def point(x,m):
    for i in range(len(x)-1,-1,-1):
        if x[i]-x[len(x)-1]>-m:
            pt=i
    return(pt)

def pair(x,m):
    pr=len(x)-2
    for i in range(len(x)-3,-1,-1):
        if x[i]-x[i+2]>=-m:
            pr=i
    return(pr)



#Define right and left maps (See definitions 7 and 8 of Section 4)
def right(x,m):
    pt=point(x,m)
    pr=pair(x,m)

    if pt<=pr+1 and pt<len(x)-1:
        y=x[0:pt+1]
        y+=[x[len(x)-1]+1]
        y+=x[pt+1:len(x)-1]
        return(y)

    if pt>pr+1 or pt==len(x)-1:
        return(x)

def left(x,m):
    pr=pair(x,m)
    if x[len(x)-1]-x[pr+1]>=-m-1:
        y=x[0:pr+1]
        y+=x[pr+2:len(x)]
        y+=[x[pr+1]-1]  
        return(y)
    if x[len(x)-1]-x[pr+1]<-m-1:
        return(x)



#Define lowest (See definition 17 of Section 6)   
def lowest(x,m):
    Record=[]
    y=None
    while x!=y:
        y=x
        x=right(x,m)
        Record.append(x)
    return(x)



#Define height of A to be height of (number of rows of) the unique partition P such that f(g(P))=A
# (f is the map of Claim 11 of Secion 5 and g is the map of Claim 9 of Secion 5)
def height(A):
    greatest=0
    j=0
    for i in range(0,len(A)):
        if A[i]>=greatest:
            greatest=A[i]
            j=i
    return((greatest-1)*(len(A)-1)+j-sum(A))





           
#GENERATE DYCK PATHS------------------------------------------------------------------

#Generate all relevant Dyck paths: Format [m,d,[a0,a1,...,a_l]]
def generate():
    Dyck_Paths=[]
    #We need to check m=1,2,3,...,20
    for m in range(20,0,-1):
        print('generating Dyck Paths with m = ' + str(m) )
        #Compute lstar and dstar for given m
        lstar=int(math.ceil(20/m+1.001))
        dstar=20
        #Initialize A as all paths for a given m
        A=[[m,0,[0]]]
        #Initialize X as paths with current number of coordinates
        X=[[m,0,[0]]]
        while len(X[0][2])<lstar+1:
            #Initialize Y as paths of with one more coordinate than X
            Y=[]
            for i in range(0,len(X)):
                x=X[i][2]
                last=x[len(x)-1]
                #Create paths with l+1 coordinates from a path with l
                for j in range(0,last+m+1):
                    d=X[i][1]
                    #Compute increase in degr statistic
                    for k in range(1,len(x)):
                        d+=alpha(x[k],j,m)
                    d-=alpha0(j,m)
                    #If degr<=dstar record the path
                    if d<=dstar:
                        Y.append([m,d,x+[j]])
                        A.append([m,d,x+[j]])
            #Reset X to Y
            X=Y
        #Collect all A together in variable Dyck_Paths
        Dyck_Paths+=A
    return(Dyck_Paths)












#CHECK LEMMA 2----------------------------------------------------------------------------

#Perform the computation for Lemma 2 for a single Dyck path of form A=[m,d,[a0,a1,...,a_l]]
#See Section 9 for  definitions of the terms within this function
def string_okay(A):
    m=A[0]
    d=A[1]
    x=A[2]
    #Compute lstar and dstar for given m
    lstar=int(math.ceil(20/m+1.001))
    dstar=20
    #If l<lstar there is nothing to check
    if len(x)<lstar+1:
        return(True)
    if len(x)==lstar+1:
        #If x is not a maximal Dyck path there is nothing to check
        if x[1]>0:
            return(True)
        if x[1]==0:
            #Compute M, h, and b=lowest(x)
            M=m*len(x)*(len(x)-1)/2
            h=height(x)
            b=lowest(x,m)
            #Compare area(b) to its supposed bound
            if sum(b)<=M-h-d:
                return(True)
            if sum(b)>M-h-d:
                print(A)
                return(False)


#Check computation needed for Lemma 2 for all Dyck Paths in a given set     
def all_strings_okay(dp):
    okay=True
    for v in range(0,len(dp)):
        if string_okay(dp[v])==False:
            okay=False
    return(okay)





#CHECK LEMMA 3-----------------------------------------------------------------------------


#Check the computation needed for Lemma 3 for all Dyck Paths in a given set
def conjecture(dp):
    okay=True
    start=0
    end=0
    while end<len(dp):
        #Group together paths if they have the same value of m and they have the same value of l
        while end<len(dp)-1 and dp[end][0]==dp[end+1][0] and\
            len(dp[end][2])==len(dp[end+1][2]):
            end+=1
        end+=1
        Dlm=dp[start:end]
        l=len(Dlm[0][2])-1
        #The case l=0 is trivial
        if l>0:
            m=Dlm[0][0]
            M=m*(l+1)*(l)/2
            #Plus represents all positive monomials appearing in RHS of the computation of Lemma 3
            Plus=[]
            #Minus represents all negative monomials appearing in RHS of the computation of Lemma 3
            Minus=[]
            #All represents all monomials appearing in LHS of the computation of Lemma 3
            All=[]
            #Monomial format is [q degree, sum of q and t degree]
            for i in range(0,len(Dlm)):
                x=Dlm[i][2]
                d=Dlm[i][1]
                a=sum(x)
                #Add a monomial to All for every element of Dlm
                All.append([a,M-d])
                #Check if x is also an element of Tlm
                if x[1]==0:
                    a=sum(x)
                    if a<=M-a-d:
                        #Add monomial string to Plus if coefficients are positive
                        for j in range(a,int(M-a-d+1)):
                            Plus.append([j,M-d])
                    if M-a-d<a:
                        #Add monomial string to Minus if coefficients are negative
                        for j in range(int(M-a-d+1),a):
                            Minus.append([j,M-d])
            #Check that the union of All and Minus gives Plus
            All_Minus=All+Minus
            Plus.sort(key=sort_rule)
            All_Minus.sort(key=sort_rule)
            if Plus==All_Minus:
                print('The Lemma 3 computation holds for m=' + str(m) + ' and l=' + str(l))
            if Plus!=All_Minus:
                okay=False
        start=end
    return(okay)


def sort_rule(X):
    return(X[1]+X[0]/1000)






#RUN THE FUNCTIONS------------------------------------------------

#Generate all relevant Dyck paths (will take a few minutes)
DP=generate()
print('All '+str(len(DP))+' Dyck Paths generated')

#Perform computation needed for Lemma 2
str_check=all_strings_okay(DP)
if str_check==True:
    print('Lemma 2 is proved')

#Perform computation needed for Lemma 3 (will take a few minutes)
con_check=conjecture(DP)
if con_check==True:
    print('The computation for Lemma 3 holds at all required pairs (m,l): Lemma 3 is proved')
