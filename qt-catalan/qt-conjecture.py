#We use step coordinates to define Dyck paths in this code (See the first paragraph of Section 2)

import math


#Define the basic statistics needed to define degree
def beta(n,l,i,j,x):
    return(sum(x[i:j+1]) -n*(j-i+1)/(l+1))

def gamma(n,l,i,j,x):
    b=beta(n,l,i,j,x)
    if b<0:
        g=min(x[i-1],math.floor(-b))
    if b>0:
        g=min(x[i],math.floor(b))
    return(g)



#Generate all relevant Dyck paths: Format [d,(x0,x1,...,x{l-1})] where d is degree

def generate(l,n):
    #Initialize X as paths with current number of coordinates
    X=[[0,[]]]
    while len(X[0][1])<l:
        #Initialize Y as paths of with one more coordinate than X
        Y=[]
        for i in range(0,len(X)):
            x=X[i][1]
            room=math.floor((len(x)+1)*n/(l+1)-sum(x))
            #Create paths with l+1 coordinates from a path with l
            for j in range(0,int(room)+1):
                d=X[i][0]
                xj=x+[j]
                #Compute increase in degr statistic
                for k in range(1,len(xj)):
                    d+=gamma(n,l,k,len(xj)-1,xj)
                #Append path to Y
                Y.append([d,xj])
        #Reset X to Y
        X=Y
    return(X)



#Sorting parameter to use later
def sort_rule(X):
    return(X[1]+X[0]/1000)



#Test the conjecture for a pair of relatively prime integers p and n.  
def conjecture(r,n):
    #Use l=p-1 to agree with notation in paper
    l=r-1
    #Find the point where the path can come within 1/(l+1) of bounding diagonal
    for q in range(0,l):
        if  round((l+1)*( (q+1)*n/(l+1)-math.floor((q+1)*n/(l+1)) ))==1:
            #Record as [horizontal coordinate, vertical coordinate]
            closest=[q,math.floor((q+1)*n/(l+1))]
    dp=generate(l,n)
    #Compute max possible area, 'M'
    M=0
    for i in range(0,l):
        M+=int(math.floor(i+1)*n/(l+1))
    #Plus represents all positive monomials appearing in RHS of conjecture
    Plus=[]
    #Plus represents all negative monomials appearing in RHS of conjecture
    Minus=[]
    #All represents all monomials appearing in LHS of conjecture
    All=[]
    #Monomial format is [q degree, sum of q and t degree]
    for i in range(0,len(dp)):
        x=dp[i][1]
        d=dp[i][0]
        #Compute area, 'a'
        a=M
        for p in range(0,len(x)):
            a-=sum(x[0:p+1])
        #Add a monomial to All for every element
        All.append([a,M-d])
        #Check if x is in T
        if sum(x[0:closest[0]+1])==closest[1]:
            if a<=M-a-d:
            #Add monomial string to Plus if coefficients are positive
                for j in range(a,int(M-a-d+1)):
                    Plus.append([j,M-d])
            if M-a-d<a:
            #Add monomial string to Minus if coefficients are negative
                for j in range(int(M-a-d+1),a):
                    Minus.append([j,M-d])  
    print('The sum of '+str(len(All))+' and '+str(len(Minus))+' should be '+str(len(Plus))+'.')

    All_Minus=All+Minus
    Plus.sort(key=sort_rule)
    All_Minus.sort(key=sort_rule)
    print('The conjecture holds for r='+str(r)+' and n='+str(n)+ ' if and only if the follwoing two sets are the same:' )
    print('First Set:')
    print(Plus)
    print('Second Set:')
    print(All_Minus)
    #Check that the union of All and Minus gives Plus

    if Plus==All_Minus:
        okay=True
    if Plus!=All_Minus:
        okay=False
    if okay==True:
        print('They are the same. The conjecture holds for r='+str(r)+' and n='+str(n)+ '.' )    
    return(okay)  



#Test the conjecture on your favorite pair of relatively prime integers

print(conjecture(7,12))