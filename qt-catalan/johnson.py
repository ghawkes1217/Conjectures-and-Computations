#We can use this code to check Conjecture 3 as stated on page 31 here: https://arxiv.org/pdf/2403.06318.pdf
#The conjecture is due to Drew Armstrong and based on an earlier conjecture of Paul Johnson
#To check that B_a[m,n] has the desired decompostion run the function find(a,[m,m+1,...,n])
#E.g., if a=5 it suffices to check find(5,v) for each v in {[0,1],[2],[3],[4],[5,6],[7],[8],[9],[10,11], and [12]}
#a=5 is probably the farthest you can check all B_a[m,n] without powerful computing
#However, when m and n are small you can check larger a quickly, e.g., find(8,[2,3])
#If m=n=2 the conjecture is actually very easy to prove for all applicable (odd) a.



import copy
import random
import math 
def cover(y,x):
    #determines if y covers x in inclusion poset on partitions, Dyck paths, etc.
    c=[]
    for i in range(0,len(x)):
        c.append(y[i]-x[i])
    if max(c)==1 and min(c)==0 and sum(c)==1:
        return True
    return False

def john(a,cap):
    #create the sequences defined on bottom of page 30 (reversed order and with n=0 m=cap
    #we have reversed order to match more standard area sequence notation in Dyck paths
    leng=a-1
    SEQ=[[]]
    while len(SEQ[0])<leng:
        newSEQ=[]
        for curseq in SEQ:
            last=0
            top=cap
            if len(curseq)>0:
                last=curseq[-1]
                top=min(last+a-1,cap)
            for j in range(last,top+1):
                newSEQ+=[curseq+[j]]
        SEQ=newSEQ
    return(SEQ)


def find(a,Last):
    #conduct a Monte Carlo search to find the desired  chain decomposition of length a
    # Last is a list of possible last entries, i.e., the numbers between m and n
    JA=(john(a,max(Last)))
    JAE=[]
    for j in JA:
        if j[-1] in Last:
            JAE.append(j)
    JAE.sort(key=lambda x:str(x))
    JAE.sort(key=lambda x:sum(x))
    #JAE is tbe set B[m,n]
    inst=0
    decomp=[]
    while inst<5000000:
        inst+=1
        JL=copy.deepcopy(JAE)
        #JL represents the paths we haven't used yet
        Failure=False
        #Failure becomes True if the current decomp attempt fails
        A_Groups=[]
        #A_Groups is the list of chains
        A_list=[]
        #A_List is the list of all paths in some chain
        while Failure==False and len(JL)>0:
            #if JL is not empty and we haven't run into a dead end initialize a new chain
            base=JL[0]
            JL.remove(base)
            group=[base]
            A_list.append(base)
            while  Failure==False and len(group) <a:
                #build the chain until it has length a
                Potential_covers=[]
                x=0
                while x<len(JL) and sum(JL[x])<=sum(group[-1])+1:
                    Potential_covers.append(JL[x])
                    x+=1
                covers=[]
                for c in Potential_covers:
                    if sum(c)==sum(group[-1])+1:
                        if cover(c,group[-1])==True:
                            covers.append(c)
                if len(covers)==0:
                    #if the last path in the group has no covers we fail
                    Failure=True

                else:
                    #pick a random cover
                    covers.sort(key=lambda x: str(x))
                    covers.reverse()
                    randex=math.floor(math.pow(random.random(),3)*len(covers))
                    A_list.append(covers[randex])
                    group.append(covers[randex])
                    JL.remove(covers[randex])
            A_Groups.append(group)
            #Append the chain to the list of chains
        if len(JL)==0:
            inst=5000000
            decomp=A_Groups
    return(decomp)
F=find(5,[5,6])
for f in F:
    print(f)