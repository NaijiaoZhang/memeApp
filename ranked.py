import operator

def RBO(l1, l2, p=0.9):
    """
        Calculates Ranked Biased Overlap (RBO) score. 
        l1 -- Ranked List 1
        l2 -- Ranked List 2
    """
    if l1 == None: l1 = []
    if l2 == None: l2 = []
    
    sl,ll = sorted([(len(l1), l1),(len(l2),l2)])
    s, S = sl
    l, L = ll
    if s == 0: return 0

    # Calculate the overlaps at ranks 1 through l 
    # (the longer of the two lists)
    ss = set([]) # contains elements from the smaller list till depth i
    ls = set([]) # contains elements from the longer list till depth i
    x_d = {0: 0}
    sum1 = 0.0
    for i in range(l):
        x = L[i]
        y = S[i] if i < s else None
        d = i + 1
        
        # if two elements are same then 
        # we don't need to add to either of the set
        if x == y: 
            x_d[d] = x_d[d-1] + 1.0
        # else add items to respective list
        # and calculate overlap
        else: 
            ls.add(x) 
            if y != None: ss.add(y)
            x_d[d] = x_d[d-1] + (1.0 if x in ss else 0.0) + (1.0 if y in ls else 0.0)     
        #calculate average overlap
        sum1 += x_d[d]/d * pow(p, d)
        
    sum2 = 0.0
    for i in range(l-s):
        d = s+i+1
        sum2 += x_d[d]*(d-s)/(d*s)*pow(p,d)

    sum3 = ((x_d[l]-x_d[s])/l+x_d[s]/s)*pow(p,l)

    # Equation 32
    rbo_ext = (1-p)/p*(sum1+sum2)+sum3
    return rbo_ext
    
def convertToDict(currentUser):
    
    tagN = {}
    
    tagN[1] = currentUser.multipanel
    tagN[2] = currentUser.celebrity
    tagN[3] = currentUser.singleimage
    tagN[4] = currentUser.anime
    tagN[5] = currentUser.gaming
    tagN[6] = currentUser.politics
    tagN[7] = currentUser.wholesome
    tagN[8] = currentUser.race
    tagN[9] = currentUser.total
    
    return tagN
    
def getRankedList(tagN):
    
    sortedTag = sorted(tagN.items(), key=operator.itemgetter(1)) 
    rankedTag =[]
    
    for i in sortedTag:
        rankedTag.append(i[0])
        
    return rankedTag
    

def simplified(tagN):
    
    rankedTag = []
    sortedTag = sorted(tagN.items(), key=operator.itemgetter(1)) 
    
    for i in sortedTag:
        rankedTag.append(i[0])
        
    return rankedTag
    
    
if __name__ == "__main__":
    list1 = [0,1,2,3,4,5,6,7,8]
    list2 = [1,0,2,3,4,5,6,7,8]
    list3 = {1:5, 2:10, 3:15, 4:20, 5:2, 6:3}
    print RBO(list1,list2, p = 0.9)
    print simplified(list3)

    list1 = ['0','1','2','3','4','5','6','7','8']
    list2 = ['0','1','2','3','4','5','7','6','8']
    print RBO(list1, list2, p = 0.9)
    
    list1 = ['0','1','2','3','4','5']
    list2 = ['5','4','3','2','1','0']
    print RBO(list1, list2, p = 0.9)
    