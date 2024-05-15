# Backpocket 13
# WEEK 1
# conditionals 
temp = 42
if temp < 0:
    print("icy!")
elif temp < 100:
    print("watery!")
else:
    print("steamy!")

# prints "watery!"


# WEEK 2

def vwl(s):
    """ return # of vowels in s """
    if len(s) == 0:
        return 0
    elif s[0] in 'aeiou':
        return 1 + vwl(s[1:])
    else:
        return 0 + vwl(s[1:])
    #  In: vwl('aliiien')
    # Out: 4



# WEEK 3

L = ['xlii','aliiien','pi']
LC = [ vwl(s) for s in L]
 #LC == [2, 4, 1]
LoL = [[vwl(s),s for s in L]]
#LoL == [ [2,'xlii'], [4, 'aliiien'], [1, 'pi'] ]

#  In: bestpr = min(LoL)
#  In: bestpr
# Out: [1, 'pi']    


# WEEK 4

def remAll(e, L):
    """ return copy of L w/o the elem. e"""

    if len(L) == 0:
        return L
    elif L[0] != e: #use it
        return L[0:1]+remAll(e, L[1:])
    else: #or lose it
        return remAll(e, L[1:])
#  In: remAll(5, [4,5,2,5])
# Out: [4,2]

# WEEK 5

def numToBinary(N):
    """ return N in binary (string)"""
    if N == 0:
        return ''
    elif N%2 == 0:
        return numToBinary(N//2) + '0'
    else: #when N%2 == 1
        return numToBinary(N//2) + '1'
    #  In: numToBinary(42)
    # Out: '101010'

# WEEK 6

def evensum(L):
    """ return sum of L's even #'s """
    result = 0
    for x in L:
        if x%2 == 0:
            result += x
    
    return result
#  In: evensum([3,20,21,22,23])
# Out: 42


# WEEK 7

def indexofmax(L):
    """ return _index_ of max in L """
    max_so_far = L[0]
    max_index = 0
    for i in range(len(L)):
        if L[i] > max_so_far:
            max_so_far = L[i]
            max_index = i
    
    return max_index
#  In: indexofmax([8,1,0,42,7])
# Out: 3

# WEEK 8

def livecount(A):
    """ return # of 1's in 2d LoL A """
    result = 0
    for r in range(len(A)):
        for c in range(len(A[r])):
            if A[r][c] == 1:
                result += 1
    
    return result
# In: A = [ [1,0,1],
#           [0,1,1] ]
# In: livecount(A)
# Out: 4


# WEEK 9

def allcounts(s):
    """ return counts of all chars in s """
    d = {}
    for c in s: # for every character c in s
        if c not in d: # not yet a key in d?
            d[c] = 1   # make it a key w/ value 1
        else:
            d[c] += 1  # else, add 1 to its value
    
    return d
# In: allcounts('xlii')
# Out: { 'x':1, 'l':1, 'i':2 }


# WEEK 10

class Alien:
    """multi-eyed Aliens """
    def __init__(self, eyes):
        self.ni = eyes

    def __repr__(self):
        result = "al" + "i"*self.ni + "en"
        return result 
    
    def addEyes(self, eyes):
        self.ni += eyes

a1 = Alien(1)
print(a1)  # alien

a1.addEyes(2)
print(a1)  # aliiien


# WEEK 11

# halt
def hc(f):
    """ returns True if f() halts
        returns False if f() runs forever
    """
    # imagine _any_ implementation here...
    # hc will have a bug, no matter what

# bug finding
def bff():
    """ bug-finding funcion """
    if hc(bff) == True:
        while True:
            print("Ha!")

    if hc(bff) == False:
        return 42

# WEEK 12

#circuit stuff

# WEEK 13

# FSM stuff