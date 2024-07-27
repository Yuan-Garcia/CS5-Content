# Action cards - pseudo, prompting, output, questions, practice, etc. 

# WEEK 1
    # conditionals 
    # Jenny+Yuan
"""'
we want to use conditionals to output aliens! 
why does the code not run as intended? 

Assume the variable str contains some beginning of the word

if len(str) > 2:
    str = str + "ens!"
if len(str) > 3:
    str = str + "ns!"
if len(str) > 4:
    str = str + "s!"
else: 
    str = str + "!"

print(str)

""" 
   

# WEEK 2
'''
def largestOf(A,B,C):
    if (A > B):
        if (A > C):
            return A
    else:
        if ( B > C):
            return B
        else:
            return C

Which permutation of A>B>C or A>C>B or B>C>A etc... does it correctly return the largest number? 
(hint: There may be more than one answer)

'''

 

# WEEK 3
"""
For this exercise, use a virtual dice roller!
action = ["", "do not"]
object = ["Study", "outside", "play", "do p-set you're ignoring", "eat a poptart", "email Prof. Dodds a picture of spam"]

action = [i + " go " for i in action]

roll a dice to access an index through the object list, then flip a coin for an index in the action list, and find your fate!

bonus points (not really) if you submit your own version of this with your next homework (must use the topic!)
"""

# WEEK 4
'''
slice = "Thereisprobablynosecretmessage!"

In: slice[6:8] + slice[11] + slice[23]
Out: ?

reverseStep = "eagsadsfsgehmjskdlr;azwxkccvabb"
In: reverseStep[::-2]
Out: ?

'''
# WEEK 5
'''

checkpointOne = not (True and (( False or False) or True))
checkpointTwo = (True and (not False and True) and checkpointOne) or True
checkpointThree = not (not checkpointOne and checkpointTwo) or checkpointOne

if (checkpointOne and checkpointTwo) or checkpointThree:
    print("this entire thing is true!")
else:
    print("this entire thing is false!!")

'''
# WEEK 6

# WEEK 7
'''
str = "CS5 is cool. I am also cool because I'm in CS5."

for i in range (0, len(str), 1):
    if str[i] == 'o':
        str[i] = '0'
    if str[i] == 's':
        str[i] = '5'
    if str[i] == 'e':
        str[i] = '3'

print(str)
Why doesn't the loop replace all instances of 'o', 's', and 'e'?
'''

# WEEK 8
'''
str = "sriats"

for i in range(0, len(str)):
    print(" "*i + str[len(str)-i-1])

What does this output?

Come up with a novel way to use nested loops in everyday life, and find a place that nested loops are present.
'''
# WEEK 9
'''
Hoch = {
    40421111 : "Dodds",
    40421010 : "Xanda",
    40420000 : "Medero",
    40421100 : "Wloka"
}

Meals = {
    "Dodds" : 0,
    "Xanda" : 0,
    "Medero" : 0,
    "Wloka" : 0
}

How would you write a program for the scanners at the hoch
to make it so that when they get the ID, the number
of meals for that person goes up by one?



'''
# WEEK 10

'''
class Cookie:
    def __init__(self, flavor, size):
        self.flavor = flavor
        self.size = size
    
    def bite():
        size = size - 1
        
Why will this class give an error when calling bite()?

Create a gingerbread cookie object...

What are 3 advantages of OOP?
1. ______
2. ______
3. ______

Name some other three common mistakes made in OOP

1. Forgetting the self.
2. No setter but getter
3. ______
4. ______
5. ______

'''

# WEEK 11
"""
Using the following lines of code, determine which code(s) will not run and which one(s) will, with reasons and their predicted output
Code 1: t = (9, 4, 6)
             t[1] = 5          
   
Code 2: d = [{“a” : “apple”}, {“b” : “ball”}, {“c” : “cage”}]
              d[“a”] = “antelope” 

Code 3: l = [‘w’, 34’ ‘r’, [20,90,42]]
              l[2] = 24
"""

'''
Using the following lines of code, determine which code(s) will not run and which one(s) will, with reasons and their predicted output
Code 1: t = (9, 4, 6)
             t[1] = 5          
   
Code 2: d = [{"a" : "apple"}, {"b" : "ball"}, {"c" : "cage"}]
              d[“a”] = “antelope” 

Code 3: l = ['w', '34' 'r', [20,90,42]]
              l[2] = 24
'''


# WEEK 12
# Jonathan+Florence

# WEEK 13
# Leena+Rachel
