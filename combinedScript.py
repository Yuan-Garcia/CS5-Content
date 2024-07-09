# File: CodeMeasure/TestScripts/Brennock.py
#Ellie Brennock
#12/13/19

"""
current issue is with the getCurrentSurroundings(self) function
is saying the index is out of range, but the program should never be on
the edge of the world so there should always be room to check to all sides
"""

import random

HEIGHT = 25
WIDTH = 25
NUMSTATES = 5
POSSIBLE_MOVES = ['N', 'E', 'W', 'S']

class Program(object):
    def __init__(self):
        """
        sets up dictionary of picobot rules
        """
        self.rules = {}


    def __repr__(self):
        """
        sets up for printing
        """
        unsortedKeys = list(self.rules.keys())
        sortedKeys = sorted(unsortedKeys)
        p = ''
        for i in range(len(sortedKeys)):
            p += str(sortedKeys[i][0]) + " " 
            p += sortedKeys[i][1] + " -> " 
            p += self.rules[sortedKeys[i]][0] + " "
            p += str(self.rules[sortedKeys[i]][1]) + '\n'
        return p

    def randomize(self):
        """
        completes a set of 45 randomized rules
        """
        surroundings = ['xxxx', 'Nxxx', 'NExx', 'NxWx', 'xxxS', 'xExS', 'xxWS', 'xExx', 'xxWx']
        state = 0
        movedir = ''
        for i in range(0, 5):
            for j in surroundings:
                state = random.choice(range(0, 5))
                movedir = random.choice(POSSIBLE_MOVES)
                while movedir in j:
                    movedir = random.choice(POSSIBLE_MOVES)
                self.rules[(i, j)] = (movedir, state)
    
    def getMove(self, state, surroundings):
        """
        returns the move for the current situation based 
        on state and surroundings
        """
        return self.rules[(state, surroundings)]


    def mutate(self):
        """
        chooses a rule from self.rules and changes the 
        value for that rule to a new random choice
        """
        key = random.choice(list(self.rules.keys()))
        state = random.choice(range(0, 5))
        while state != self.rules[key][1]:
            state = random.choice(range(0, 5))
        movedir = random.choice(POSSIBLE_MOVES)
        while movedir != self.rules[key][0]:
            movedir = random.choice(POSSIBLE_MOVES)
        self.rules[key] = (movedir, state)


    def crossover(self, other):
        """
        returns an offspring program with some rules
        from each parent (self and other)
        """
        program = Program()
        crossState = random.choice(range(0, 4))
        for i in self.rules:
            if i[0] <= crossState:
                program.rules[i] = self.rules[i]
        for j in other.rules:
            if j[0] > crossState:
                program.rules[j] =  other.rules[j]
        return program

    def __gt__(self, other):
        """Greater-than operator -- works randomly, but works!"""
        return random.choice([True, False])

    def __lt__(self, other):
        """Less-than operator -- works randomly, but works!"""
        return random.choice([True, False])

class World(object):

    def __init__(self, initial_row, initial_col, program):
        self.row = initial_row
        self.col = initial_col
        self.state = 0
        self.prog = program
        self.room = [[' ']*WIDTH for row in range(HEIGHT)]
        #places in walls on all 4 sides
        for c in range(WIDTH):
            self.room[0][c] = '+'
            self.room[HEIGHT - 1][c] = '+'
        for r in range(0, HEIGHT):
            self.room[r][0] = '+'
            self.room[r][WIDTH - 1] = '+'
        #places picobot in inital location
        self.room[self.row][self.col] = 'P'
        

    def __repr__(self):
        r = ''
        for row in range(HEIGHT):
            for col in range(WIDTH):
                r += self.room[row][col]
                r += ' '
            r += '\n'
        return r


    def getCurrentSurroundings(self):
        """
        returns the current surroundings of the program
        """
        surroundings = ''
        #checks north
        if self.room[self.row - 1][self.col] == '+':
            surroundings += 'N'
        else:
            surroundings += 'x'
        #checks east
        if self.room[self.row][self.col + 1] == '+':
            surroundings += 'E'
        else:
            surroundings += 'x'
        #checks west
        if self.room[self.row][self.col - 1] == '+':
            surroundings += 'W'
        else:
            surroundings += 'x'
        #checks south
        if self.room[self.row + 1][self.col] == '+':
            surroundings += 'S'
        else:
            surroundings += 'x'
        return surroundings
        
    def step(self):
        """
        moves a step according to getMove and updates world
        """
        (move, st) = self.prog.getMove(self.state, self.getCurrentSurroundings())
        self.room[self.row][self.col] = 'o'
        if move == 'N':
            self.row -= 1
        elif move == 'E':
            self.col += 1
        elif move == 'W':
            self.col -= 1
        else:
            self.row += 1
        self.state = st
        self.room[self.row][self.col] = 'P'

    def run(self, steps):
        """
        runs step steps number of times
        """
        for i in range(steps):
            self.step()

    def fractionVisitedCells(self):
        """
        calculates fraction of cells visited by the program
        """
        count = 1
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if self.room[row][col] == 'o':
                    count += 1
        return count / 529

def popList(size):
    """
    creates a list of size size of randomized programs
    """
    L = []
    for i in range(size):
        prog = Program()
        prog.randomize()
        L.append(prog)
    return L

def evaluateFitness(program, trials, steps):
    """
    runs the program a number of steps over a number of trials
    and averages the percentage of squares visited
    """
    fit = 0
    for i in range(trials):
        world = World(random.choice(range(1, 24)), random.choice(range(1, 24)), program)
        world.run(steps)
        fit += world.fractionVisitedCells()
    return fit / trials

def GA(popsize, numgens):
    """
    currently just creates a list of programs and how well they work
    """
    popLists = popList(popsize)
    L = [[0]*2]*popsize
    for i in range(popsize):
        L[i][0] = evaluateFitness(popLists[i], 42, 1000)
        L[i][1] = popLists[i]
    for j in range(numgens):
        Sl = sorted(L)
        length = int(len(Sl) * 0.1)
        Sl = Sl[len(Sl) - length:  -1]
        for i in range(popsize - len(Sl)):
            parent1 = random.choice(Sl)[1]
            parent2 = random.choice(Sl)[1]
            newProg = parent1.crossover(parent2)
            if random.choice([1,2, 3]) == 1:
                newProg.mutate()
            Sl.append([evaluateFitness(newProg, 42, 1000), newProg])
        L = Sl
        print("Generation " + str(j))
        ave = 0
        for k in L:
            ave += k[0]
        ave = ave / len(L)
        print('Average fitness: ' + str(ave))
        max = L[0][0]
        print('Best fitness: ' + str(max))
    print('Best Picobot program:')
    print(L[0][1])
    return L[0][1]

"""
Best fitness: 0.06593752813034474
Best Picobot program:
0 NExx -> W 4
0 NxWx -> E 3
0 Nxxx -> S 2
0 xExS -> W 3
0 xExx -> N 0
0 xxWS -> E 0
0 xxWx -> E 2
0 xxxS -> E 1
0 xxxx -> S 1
1 NExx -> S 4
1 NxWx -> E 3
1 Nxxx -> S 2
1 xExS -> W 3
1 xExx -> S 0
1 xxWS -> N 0
1 xxWx -> N 4
1 xxxS -> N 3
1 xxxx -> N 4
2 NExx -> S 4
2 NxWx -> E 0
2 Nxxx -> S 0
2 xExS -> W 0
2 xExx -> S 4
2 xxWS -> E 3
2 xxWx -> N 4
2 xxxS -> E 1
2 xxxx -> W 3
3 NExx -> S 2
3 NxWx -> E 3
3 Nxxx -> S 0
3 xExS -> N 1
3 xExx -> N 1
3 xxWS -> E 4
3 xxWx -> E 0
3 xxxS -> N 1
3 xxxx -> N 2
4 NExx -> W 4
4 NxWx -> E 3
4 Nxxx -> S 0
4 xExS -> N 1
4 xExx -> W 4
4 xxWS -> E 1
4 xxWx -> N 4
4 xxxS -> N 3
4 xxxx -> W 3
"""

# File: CodeMeasure/TestScripts/textModel.py
#
# textmodel.py
#
# TextModel project!
#
# Name(s): Florence Lin and Annette Chang
#

import string 
from porter import create_stem
import math

class TextModel:
    """A class supporting complex models of text."""

    def __init__(self):
        """Create an empty TextModel."""
        # 
        # The text in the model, all in a single string--the original
        # and "cleaned" versions.
        #
        self.text = ''            # No text present yet
        self.cleanedtext = ''     # Nor any cleaned text yet
                                  # ..(cleaned == only letters, all lowercase)

        #
        # Create dictionaries for each characteristic
        #
        self.words = {}           # For counting words
        self.wordlengths = {}     # For counting word lengths
        self.stems = {}           # For counting stems
        self.sentencelengths = {} # For counting sentence length
        self.repeatedPhrase2 = {}     # For counting phrases length 2
        self.repeatedPhrase3 = {}     # For counting phrases length 3
        self.repeatedPhrase4 = {}     # For counting phrases length 4
        self.repeatedPhrase5 = {}     # For counting phrases length 5

    def __repr__(self):
        """Display the contents of a TextModel."""
        s = f'Words:\n{str(self.words)}\n\n'
        s += f'Word lengths:\n{str(self.wordlengths)}\n\n'
        s += f'Stems:\n{str(self.stems)}\n\n'
        s += f'Sentence lengths:\n{str(self.sentencelengths)}\n\n'
        s += f'Phrases of length 2:\n{str(self.repeatedPhrase2)}\n\n'
        s += f'Phrases of length 3:\n{str(self.repeatedPhrase3)}\n\n'
        s += f'Phrases of length 4:\n{str(self.repeatedPhrase4)}\n\n'
        s += '+'*55 + '\n'
        s += f'Text[:42]    {self.text[:len(self.text)]}\n'
        s += f'Cleaned[:42] {self.cleanedtext[:len(self.cleanedtext)]}\n'
        s += '+'*55 + '\n\n'
        return s

    # We provide two text-adding methods (functions) here:
    def addRawText(self, text):
        """addRawText accepts self (the object itself)
                      and text, a string of raw text to add.
           Nothing is returned from this method, but
           the text _is_ added.
        """
        self.text += text 
        self.cleanedtext += self.cleanString(self.text) 

    # The second one adds text from a file:
    def addFileText(self, filename):
        """addFileText accepts a filename.

           Nothing is returned from this method, but
           the file is opened and its text _is_ added.

           If the file is not present, it will crash!
        """
        f = open(filename, 'r', encoding='latin1')
                               # The above may need utf-8 or utf-16, depending
        text = f.read()        # Read all of the contents into text 
        f.close()              # Close the file
        self.addRawText(text)  # Uses the previous method!

    # Include other functions here.
    # In particular, you'll need functions that add to the model.

    def makeSentenceLengths(self):
        """Creates the dictionary of sentence lengths
               should use self.text, because it needs the punctuation!
        """

        LoW = self.text.split()
        count = 0
        for i in LoW:
            count += 1
            if i[-1] in '.?!':
              if count in self.sentencelengths:
                self.sentencelengths[count] += 1
              else: 
                self.sentencelengths[count] = 1 
              count = 0



    def cleanString(self, s):
        """Returns the string s, but
           with only ASCII characters, only lowercase, and no punctuation.
           See the description and hints in the problem!
        """
        s = s.encode("ascii", "ignore")   # Ignores non-ASCII characters
        s = s.decode()       

        result = s.lower()  # converts to lowercase 

        for p in string.punctuation: # gets rid of punctuation
          result = result.replace(p, "")

        return result


    def makeWordLengths(self):
      """creates the dictionary of word-length features using
          self.cleanedtext
      """
      
      LoW = self.cleanedtext.split()
      count = 0
      for i in LoW:
        for x in range(len(i)):
          count += 1
        if count in self.wordlengths:
          self.wordlengths[count] += 1
        else:
          self.wordlengths[count] = 1
        count = 0
    
    def makeWords(self):
      """ creates the dictionary of words using self.cleanedtext
      """
      LoW = self.cleanedtext.split()
      for i in LoW:
        if i in self.words:
          self.words[i] += 1
        else:
          self.words[i] = 1
      

    def makeStems(self):
       """ creates the dictionary of the stems of the words themselves
       """
       LoW = self.cleanedtext.split()
       for i in LoW:
            if create_stem(i) in self.stems:
               self.stems[create_stem(i)] += 1
            else:
               self.stems[create_stem(i)] = 1

    #looking for common phrases in song lyrics (groups of 2, 3, 4)
    def repeatedPhrasesLen2(self):
       """ creates the dictionary for every two word lengthed phrase
       """
       LoW = self.cleanedtext.split()
       i = 0
       while i < len(LoW):
        phrase = str(LoW[i: i+2])
        if phrase in self.repeatedPhrase2:
            self.repeatedPhrase2[phrase] += 1
        else:
            self.repeatedPhrase2[phrase] = 1
        i += 1
    
    def repeatedPhrasesLen3(self):
       """ creates the dictionary for every three word lengthed phrase
       """
       LoW = self.cleanedtext.split()
       i = 0
       while i < len(LoW):
        phrase = str(LoW[i: i+3])
        if phrase in self.repeatedPhrase3:
            self.repeatedPhrase3[phrase] += 1
        else:
            self.repeatedPhrase3[phrase] = 1
        i += 1
    
    def repeatedPhrasesLen4(self):
       """ creates the dictionary for every three word lengthed phrase
       """
       LoW = self.cleanedtext.split()
       i = 0
       while i < len(LoW):
        phrase = str(LoW[i: i+4])
        if phrase in self.repeatedPhrase4:
            self.repeatedPhrase4[phrase] += 1
        else:
            self.repeatedPhrase4[phrase] = 1
        i += 1

    def repeatedPhrasesLen5(self):
       """ creates the dictionary for every three word lengthed phrase
       """
       LoW = self.cleanedtext.split()
       i = 0
       while i < len(LoW):
        phrase = str(LoW[i: i+5])
        if phrase in self.repeatedPhrase5:
            self.repeatedPhrase5[phrase] += 1
        else:
            self.repeatedPhrase5[phrase] = 1
        i += 1
       
 
    def normalizeDictionary(self, d):
      """accepts any model dictionary D and returns a normalized version
      """
      nd = {}
      for k in d:
        nd[k] = d[k] / float(sum(d.values()))
      return nd

    def smallestValue(self, nd1, nd2):
      """accepts two model dictionaries and returns the smallest positive 
        value across them both
      """
      minNd1 = 1
      minNd2 = 1
      for k in nd1:
         if nd1[k] <= minNd1:
            minNd1 = nd1[k]
      for k in nd2:
         if nd2[k] <= minNd2:
            minNd2 = nd2[k]

      if minNd1 <= minNd2:
        return minNd1
      else:
        return minNd2
      
    def compareDictionaries(self, d, nd1, nd2):
      """computes the log probabilities that the dictionary d came from
         the distribution of data in the normalized dictionaries nd1 
         and nd2 and returns the value of the log probabilities.
      """
      total_log_prob = 0.0
      epsilon = 0.5*(self.smallestValue(nd1, nd2))
      for k in d:
        if k in nd1:
           total_log_prob += d[k]*math.log(nd1[k])
        else:
           total_log_prob += d[k]*math.log(epsilon)
        lp1 = total_log_prob
      total_log_prob = 0.0
      for k in d:
        if k in nd2:
           total_log_prob += d[k]*math.log(nd2[k])
        else:
           total_log_prob += d[k]*math.log(epsilon)
        lp2 = total_log_prob
      return [lp1, lp2]


    def createAllDictionaries(self):
      """Create out all of self's
         dictionaries in full.
      """
      self.makeSentenceLengths()
      self.makeWords()
      self.makeStems()
      self.makeWordLengths()
      self.repeatedPhrasesLen2()     
      self.repeatedPhrasesLen3()    
      self.repeatedPhrasesLen4()     
      self.repeatedPhrasesLen5()


    def compareTextWithTwoModels(self, model1, model2):
      """runs compareDictionaries for each feature dictionaries in self   
          against corresponding dictionaries
      """

      #create normalized dictionaries for each dictionary
      ndWords1 = self.normalizeDictionary(model1.words)
      ndWords2 = self.normalizeDictionary(model2.words)
      ndWordLengths1 = self.normalizeDictionary(model1.wordlengths)
      ndWordLengths2 = self.normalizeDictionary(model2.wordlengths)
      ndStems1 = self.normalizeDictionary(model1.stems)
      ndStems2 = self.normalizeDictionary(model2.stems)
      ndSentenceLengths1 = self.normalizeDictionary(model1.sentencelengths)
      ndSentenceLengths2 = self.normalizeDictionary(model2.sentencelengths)
      ndRepeatedPhrase2_1 = self.normalizeDictionary(model1.repeatedPhrase2)
      ndRepeatedPhrase2_2 = self.normalizeDictionary(model2.repeatedPhrase2)
      ndRepeatedPhrase3_1 = self.normalizeDictionary(model1.repeatedPhrase3)
      ndRepeatedPhrase3_2 = self.normalizeDictionary(model2.repeatedPhrase3)
      ndRepeatedPhrase4_1 = self.normalizeDictionary(model1.repeatedPhrase4)
      ndRepeatedPhrase4_2 = self.normalizeDictionary(model2.repeatedPhrase4)
      ndRepeatedPhrase5_1 = self.normalizeDictionary(model1.repeatedPhrase5)
      ndRepeatedPhrase5_2 = self.normalizeDictionary(model2.repeatedPhrase5)

      #compute the two log-probability values of each dictionary
      LogProbs1 = self.compareDictionaries(self.words, ndWords1, ndWords2)
      LogProbs2 = self.compareDictionaries(self.wordlengths, ndWordLengths1, ndWordLengths2)
      LogProbs3 = self.compareDictionaries(self.stems, ndStems1, ndStems2)
      LogProbs4 = self.compareDictionaries(self.sentencelengths, ndSentenceLengths1, ndSentenceLengths2)
      LogProbs5 = self.compareDictionaries(self.repeatedPhrase2, ndRepeatedPhrase2_1, ndRepeatedPhrase2_2)
      LogProbs6 = self.compareDictionaries(self.repeatedPhrase3, ndRepeatedPhrase3_1, ndRepeatedPhrase3_2)
      LogProbs7 = self.compareDictionaries(self.repeatedPhrase4, ndRepeatedPhrase4_1, ndRepeatedPhrase4_2)
      LogProbs8 = self.compareDictionaries(self.repeatedPhrase5, ndRepeatedPhrase5_1, ndRepeatedPhrase5_2)
      print("LogProbs1 is", LogProbs1)
      print("LogProbs2 is", LogProbs2)
      print("LogProbs3 is", LogProbs3)
      print("LogProbs4 is", LogProbs4)
      print("LogProbs5 is", LogProbs5)
      print("LogProbs6 is", LogProbs6)
      print("LogProbs7 is", LogProbs7)
      print("LogProbs8 is", LogProbs8)
      print("Overall comparison: \n" )

      #generate comparison chart
      print(f"     {'name':>20s}   {'vsTM1':>10s}   {'vsTM2':>10s} ")
      print(f"     {'----':>20s}   {'-----':>10s}   {'-----':>10s} ")
      d_name = 'words'
      print(f"     {d_name:>20s}   {LogProbs1[0]:>10.2f}   {LogProbs1[1]:>10.2f} ") 
      d_name = 'word lengths'
      print(f"     {d_name:>20s}   {LogProbs2[0]:>10.2f}   {LogProbs2[1]:>10.2f} ") 
      d_name = 'word stems'
      print(f"     {d_name:>20s}   {LogProbs3[0]:>10.2f}   {LogProbs3[1]:>10.2f} ")
      d_name = 'sentence lengths'
      print(f"     {d_name:>20s}   {LogProbs4[0]:>10.2f}   {LogProbs4[1]:>10.2f} ")  
      d_name = 'repeated Phrases length 2'
      print(f"     {d_name:>20s}   {LogProbs5[0]:>10.2f}   {LogProbs5[1]:>10.2f} ") 
      d_name = 'repeated Phrases length 3'
      print(f"     {d_name:>20s}   {LogProbs6[0]:>10.2f}   {LogProbs6[1]:>10.2f} ") 
      d_name = 'repeated Phrases length 4'
      print(f"     {d_name:>20s}   {LogProbs7[0]:>10.2f}   {LogProbs7[1]:>10.2f} ") 
      d_name = 'repeated Phrases length 5'
      print(f"     {d_name:>20s}   {LogProbs8[0]:>10.2f}   {LogProbs8[1]:>10.2f} ") 
      
      #compare the two text models
      textMod1 = [LogProbs1[0], LogProbs2[0], LogProbs3[0], LogProbs4[0], LogProbs5[0], LogProbs6[0], LogProbs7[0], LogProbs8[0]]
      textMod2 = [LogProbs1[1], LogProbs2[1], LogProbs3[1], LogProbs4[1], LogProbs5[1], LogProbs6[1], LogProbs7[1], LogProbs8[1]]
      model1Wins = 0
      model2Wins = 0
      print(textMod1)

      for i in range(len(textMod1)):
         if textMod1[i] > textMod2[i]:
            model1Wins += 1
         if textMod1[i] < textMod2[i]:
            model2Wins += 1

      print("--> Text model 1 wins on ", model1Wins, "features")
      print("-->  Text model 2 wins on ", model2Wins, "features")
      if model1Wins > model2Wins:
         print("Text model 1 is the better match!")
      else:
         print("Text model 2 is the better match!")
      

      


# And let's test things out here...
TMintro = TextModel()

# Add a call that puts information into the model
TMintro.addRawText("""This is a small sentence. This isn't a small
sentence, because this sentence contains more than 10 words and a
number! This isn't a question, is it?""")

# Put the above triple-quoted string into a file named test.txt, then run this:
#  TMintro.addFileText("test.txt")   # "comment in" this line, once the file is created

# Print it out
print("TMintro is", TMintro)

print(" +++++++++++ TextModel 1 +++++++++++ ")
TM1 = TextModel()
TM1.addFileText("hungerGames.txt")
TM1.createAllDictionaries()  # provided in hw description
print(TM1)

print(" +++++++++++ TextModel 2 +++++++++++ ")
TM2 = TextModel()
TM2.addFileText("divergent.txt")
TM2.createAllDictionaries()  # provided in hw description
print(TM2)


print(" +++++++++++ test +++++++++++ ")
TM_Unk = TextModel()
TM_Unk.addFileText("percyJackson.txt")
TM_Unk.createAllDictionaries()  # provided in hw description
print(TM_Unk)





# File: CodeMeasure/TestScripts/FloHw2Pr3.py
# CS 5 Gold, hw2pr3
# filename: hw2pr3.py
# Name: Florence Lin
# problem description: List comprehensions



# this gives us functions like sin and cos...
from math import *



# two more functions (not in the math library above)

def dbl(x):
    """Doubler!  argument: x, a number"""
    return 2*x

def sq(x):
    """Squarer!  argument: x, a number"""
    return x**2



# examples for getting used to list comprehensions...

def lc_mult(N):
    """This example accepts an integer N
       and returns a list of integers
       from 0 to N-1, **each multiplied by 2**
    """
    return [2*x for x in range(N)]

def lc_idiv(N):
    """This example accepts an integer N
       and returns a list of integers
       from 0 to N-1, **each divided by 2**
       WARNING: this is INTEGER division...!
    """
    return [x//2 for x in range(N)]

def lc_fdiv(N):
    """This example accepts an integer N
       and returns a list of integers
       from 0 to N-1, **each divided by 2**
       NOTE: this is floating-point division...!
    """
    return [x/2 for x in range(N)]

# printing tests
print( "lc_mult(4)   should be [0, 2, 4, 6] :", lc_mult(4) )   
print( "lc_idiv(4)   should be [0, 0, 1, 1] :", lc_idiv(4) ) 
print( "lc_fdiv(4)   should be [0.0, 0.5, 1.0, 1.5] :", lc_fdiv(4) ) 

# assertion tests
assert lc_mult(4) == [0, 2, 4, 6]
assert lc_idiv(4) == [0, 0, 1, 1]
assert lc_fdiv(4) == [0.0, 0.5, 1.0, 1.5]

# Here is where your functions start for the lab:

# Step 1, part 1
def unitfracs(N):
    """returns a list of evenly-spaced left-hand endpoints (fractions) in the unit interval [0, 1)
    """
    return [x/N for x in range(N)]

# Step 1, part 2
def scaledfracs(low, high, N):
    """returns N left endpoints uniformly through the interval [low, high).
       basically the scaled fraction of low high N 
    """
    return [x*(high-low)+low for x in unitfracs(N)]

# Step 2, part 1
def sqfracs(low, high, N):
    """returns scaledfracs(low, high, N) but each value returned in scaledfracs is squared
       basically takes three numbers and returns the square of its scaled fraction created in scaled fracs
    """
    return [x**2 for x in scaledfracs(low,high,N)]

# Step2, pt 2
def f_of_fracs(f, low, high, N):
    """returns f of N numbers in scaled fraction by using four values (f, low, high, N) where f is the function, low is the bottom limit
       high is the top limit, and N is the number of scaled fraction
    """
    return [f(x) for x in scaledfracs(low,high,N)]


#Step 3
def integrate(f, low, high, N):
    """Integrate returns an estimate of the definite integral
       of the function f (the first argument)
       with lower limit low (the second argument)
       and upper limit high (the third argument)
       where N steps are taken (the fourth argument)

       integrate simply returns the sum of the areas of rectangles
       under f, drawn at the left endpoints of N uniform steps
       from low to high
    """
    return sum(f_of_fracs(f, low, high, N)) * (high-low)/N

#Q 2
def c(x):
    """c is a semicircular function of radius two"""
    return (4 - x**2)**0.5


print( "integrate(dbl, 0, 10, 4) should be 75 :", integrate(dbl, 0, 10, 4) )
print( "integrate(sq, 0, 10, 4) should be 218.75 :", integrate(sq, 0, 10, 4) )




# File: CodeMeasure/TestScripts/connect4.py
# Connect Four 2.0!
# A.I. Connect Four 
# Will be able to:
#Look ahead one move for either checker 'X' or 'O'
#Choose a move that can win the game (if a win is available!)
#Choose a move that can block an opponent's win (in the upcoming turn—if it's possible to do so)
#Defeat its creator at Connect Four (well, possibly...)

#given functions (also functions written in hw9pr2)

import random

def inarow_Neast(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading east and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start < 0 or r_start > H - 1:
        return False # out of bounds row
    if c_start < 0 or c_start + (N-1) > W - 1:
        return False # o.o.b. col
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start][c_start+i] != ch: # a mismatch!
            return False
    return True  # all offsets succeeded, so we return True


def sneakyRecur(self, x):
    if x==0:
        return x
    else:
        return self.sneakyRecur(x-1)

def inarow_Nsouth(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading south and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start < 0 or r_start + (N-1) > H - 1:
        return False # out of bounds row
    if c_start < 0 or c_start > W - 1:
        return False # o.o.b. col
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start+i][c_start] != ch: # a mismatch!
            return False
    return True  # all offsets succeeded, so we return True

def inarow_Nnortheast(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading northeast and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start - (N-1) < 0 or r_start > H - 1:
        return False # out of bounds row
    if c_start < 0 or c_start + (N-1) > W - 1:
        return False # o.o.b. col
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start-i][c_start+i] != ch: # a mismatch!
            return False
    return True  # all offsets succeeded, so we return True

def inarow_Nsoutheast(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading southeast and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start < 0 or r_start + (N-1) > H - 1:
        return False # out of bounds row
    if c_start < 0 or c_start + (N-1) > W - 1:
        return False # o.o.b. col
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start+i][c_start+i] != ch: # a mismatch!
            return False
    return True  # all offsets succeeded, so we return True






class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.data = [[' ']*width for row in range(height)] #data is not a variable as we do not need to input it. 

        # We do not need to return anything from a constructor!

    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = ''                          # the string to return
        for row in range(0, self.height):
            s += '|'
            for col in range(0, self.width):
                s += self.data[row][col] + '|'
            s += '\n'

        s += (2*self.width + 1) * '-'   # bottom of the board

        s += '\n'
        
        for col in range(0, self.width):
            s += " " + str(col)

        return s      # the board is complete, return it


    def addMove(self, col, ox):
        """ addMove takes two arguments
            col = index of the column to which the checker
            will be added
            ox = 1-character string representing the checker 
            to add to the board 'X' or 'O'
            addMove checks the row below to see if it is filled.
            If it is, then addMove adds something above it. We keep 
            the return inside the for loop to stop the loop once 
            it fills the row above so it doesn't keep replacing the 
            entire column with the once checker.
        """
        H = self.height
        for row in range(0,H):
            if  self.data[row][col] != ' ':
                self.data[row-1][col] = ox
                return #inside the for loop

        self.data[H-1][col] = ox #sets the bottom most row as a checker in case the entire column is empty. 



    def clear(self):
        """ clears the board of X's and O's"""
        W = self.width
        H = self.height

        for row in range(0, H):
            for col in range(0, W):
                self.data[row][col] = ' '
        


    def setBoard(self, moveString):
        """Accepts a string of columns and places
           alternating checkers in those columns,
           starting with 'X'.

           For example, call b.setBoard('012345')
           to see 'X's and 'O's alternate on the
           bottom row, or b.setBoard('000000') to
           see them alternate in the left column.

           moveString must be a string of one-digit integers.
        """
        nextChecker = 'X'   # start by playing 'X'
        for colChar in moveString:
            col = int(colChar)
            if 0 <= col <= self.width:
                self.addMove(col, nextChecker)
            if nextChecker == 'X':
                nextChecker = 'O'
            else:
                nextChecker = 'X' 



    def allowsMove(self, c):
        """ check if a column is a legal move
            returns True if the calling object (of type Board) 
            does allow a move into column c. It returns False if 
            column c is not a legal column number for the calling 
            object. It also returns False if column c is full.
        """
        
        H = self.height
        W = self.width
        D = self.data

        if c >= W or c < 0:
            return False
        elif D[0][c] != ' ' : #top row's index is 0
            return False
        else:
            return True

    def isFull(self):
        """ returns True is the calling object of type Board is 
            full of checkers. It should return False otherwise. 
        """
        H = self.height
        W = self.width

        for row in range(0, H):
            for col in range(0, W): 
                if self.data[row][col] == ' ':
                    return False

                
        return True

    def delMove(self, c):
        """ removes the top checker from column c.
            If the column is empty, then delMove does nothing
        """

        H = self.height

        for row in range (0,H):
            if  self.data[row][c] != ' ':
                self.data[row][c] = ' '
                return #inside the for loop


    def winsFor(self, ox):
        """ winsFor code argument OX is a 1-character checker:
            either 'X' or 'O'. It should return True 
            if there are four checkers of type ox in a 
            row on the board. It should return False 
            othwerwise.
        """
            
        # this is pseudocode
        H = self.height
        W = self.width

        for row in range (0,H):
            for col in range (0, W):
                if inarow_Neast (ox, row, col, self.data, 4) == True \
                    or inarow_Nsouth(ox, row, col, self.data, 4) == True \
                        or inarow_Nnortheast(ox, row, col, self.data, 4) == True \
                            or inarow_Nsoutheast(ox, row, col, self.data, 4) == True:
                            return True
        return False


    def colsToWin(self, ox):
        """returns a list of columns at which ox would win on the next move
            takes one argument "X" or "O"
            place a checker in each column and each time see if the game is a win.
        """
        L = []
        
        for c in range (self.width):
            if self.allowsMove(c) == True: 
                self.addMove(c, ox)
                if self.winsFor(ox) == True:
                    L = L + [c]
                self.delMove(c)

        return L


    def aiMove(self, ox):
        """ accepts a single argument which will be either X or O
            returns a single integer which is a legal column.
            if there is a way for X or O to win then aiMove returns
            that move.
        """
        if ox == 'O':
            xo = 'X'
        else:
            if ox == 'X':
                xo = 'O'

        B = []
        L = self.colsToWin(ox)
        L2 = self.colsToWin(xo)

        #if you can win, you need to win in the next move
        if L != []:
            return random.choice(L)

        #if you cannot win...
        elif L2 !=[]:
            return random.choice(L2)

        else:
            
            for c in range (self.width):
                if self.allowsMove(c) == True:
                    B = B + [c]
            return random.choice(B)


    
    def hostGame(self):
        """ host a game of connect four! 
            alternates between X and O where X moves first
            asks user for column number for each move
        """

        print()
        print ("Let's play Connect Four!")
        print()
        print (self) #prints the board

        users_checker = str(input('Player 1, choose a checker (X or O) or choose "both" for the AI to play against itself: '))
        if users_checker == 'X':
            while True:  #one X turn and one O turn in the while loop
                users_col = -1 #prompts the user to input a valid column number
                while self.allowsMove(users_col) == False: #same as saying while not self.allowsMove(users_col):
                    users_col = int(input("Player 1, choose a column: "))

                self.addMove(users_col, users_checker) 
                print (self)
                if self.winsFor("X"):
                    return "First Player wins! X wins! Congratulations!"

                # AIs turn
                AI_col = self.aiMove('O')
                self.addMove(AI_col, 'O') 

                print (self)
                if self.winsFor("O"):
                    return "Second Player wins! O wins! Sorry Player 1 lost!"

                if self.isFull() == True:
                    return "GameOver!"
        
    
        elif users_checker == 'O':
            print('Since X always goes first, AI will go first!')
            AI_col = self.aiMove('X')
            self.addMove(AI_col, 'X') 

            print (self)
            if self.winsFor("X"):
                return "Second Player wins! X wins! Congratulations!"

            if self.isFull() == True:
                return "GameOver!"
        
            while True:  #one X turn and one O turn in the while loop
                users_col = -1 #prompts the user to input a valid column number
                while self.allowsMove(users_col) == False: #same as saying while not self.allowsMove(users_col):
                    users_col = int(input("Player 1, choose a column: "))

                self.addMove(users_col, users_checker) 
                print (self)
                if self.winsFor("X"):
                    return "First Player wins! X wins! Congratulations!"

        else: #user picks computer to play both X and O; users_checker == 'both'
            
            while True:
                AI_col = self.aiMove('X')
                self.addMove(AI_col, 'X') 
                print (self)
                if self.winsFor("X"):
                    return "Second Player wins! X wins! Congratulations!"

                if self.isFull() == True:
                    return "GameOver!"

                AI_col = self.aiMove('O')
                self.addMove(AI_col, 'O') 

                print (self)
                if self.winsFor("O"):
                    return "Second Player wins! O wins! Congratulations!"

                if self.isFull() == True:
                    return "GameOver!"


    def playGame(self, px, po, ss = False):
        """Plays a game of Connect Four.
            p1 and p2 are objects of type Player OR
            the string 'human'.
            If ss is True, it will "show scores" each time.

            define both players and board each time
            E.g.
            px = 'human'  #Player('X', 'LEFT', 1)     
            po = 'human' #Player('O', 'LEFT', 1)   
            b = Board(7,6)  
        """

        nextCheckerToMove = 'X'
        nextPlayerToMove = px

        while True:

            # print the current board
            print(self)

            # choose the next move
            if nextPlayerToMove == 'human':
                col = -1
                while not self.allowsMove(col):
                    col = int(input('Next col for ' + nextCheckerToMove + ': '))

                    if not self.allowsMove(col):
                        print('column full, please choose another column!')

            else: # it's a computer player
                if ss:
                    scores = nextPlayerToMove.scoresFor(self)
                    print((nextCheckerToMove + "'s"), 'Scores: ', [int(sc) for sc in scores])
                    print()
                    col = nextPlayerToMove.tiebreakMove(scores)
                else:
                    col = nextPlayerToMove.nextMove(self)

            # add the checker to the board
            self.addMove(col, nextCheckerToMove)

            # check if game is over
            if self.winsFor(nextCheckerToMove):
                print(self)
                print('\n' + nextCheckerToMove + ' wins! Congratulations!\n\n')
                break
            if self.isFull():
                print(self)
                print('\nThe game is a draw.\n\n')
                break

            # swap players
            if nextCheckerToMove == 'X':
                nextCheckerToMove = 'O'
                nextPlayerToMove = po
            else:
                nextCheckerToMove = 'X'
                nextPlayerToMove = px

        print('Come back 4 more!')
            

    #new variation of connectfour (swaps third row with fifth row when third row has been filled!)

    def playCrazyGame(self, px, po, ss = False):
        """Plays a game of Connect Four.
            p1 and p2 are objects of type Player OR
            the string 'human'.
            If ss is True, it will "show scores" each time.

            define both players and board each time
            E.g.
            px = 'human'  #Player('X', 'LEFT', 1)     
            po = 'human' #Player('O', 'LEFT', 1)   
            b = Board(7,6)  
        """

        nextCheckerToMove = 'X'
        nextPlayerToMove = px

        while True:

            # print the current board
            print(self)

            # choose the next move
            if nextPlayerToMove == 'human':
                col = -1
                while not self.allowsMove(col):
                    col = int(input('Next col for ' + nextCheckerToMove + ': '))

                    if not self.allowsMove(col): #if column is full it will prompt you to choose another column
                        print('column full, please choose another column!')

                
            else: # it's a computer player
                if ss:
                    scores = nextPlayerToMove.scoresFor(self)
                    print((nextCheckerToMove + "'s"), 'Scores: ', [int(sc) for sc in scores])
                    print()
                    col = nextPlayerToMove.tiebreakMove(scores)
                else:
                    col = nextPlayerToMove.nextMove(self)

            # add the checker to the board
            self.addMove(col, nextCheckerToMove)

            #variation = ROW SWAP! swaps row 3 for row 5
            if self.checkifrowFull(3) == True:
                print("WARNING!!!!!! Board row swapped")
                for c in range(7):
                    bot = self.data[5][c]
                    up = self.data[3][c]
                    self.data[5][c] = up
                    self.data[3][c] = bot
                    

            # check if game is over
            if self.winsFor(nextCheckerToMove):
                print(self)
                print('\n' + nextCheckerToMove + ' wins! Congratulations!\n\n')
                break
            if self.isFull():
                print(self)
                print('\nThe game is a draw.\n\n')
                break

            # swap players
            if nextCheckerToMove == 'X':
                nextCheckerToMove = 'O'
                nextPlayerToMove = po
            else:
                nextCheckerToMove = 'X'
                nextPlayerToMove = px
                
        #if row three is all full, ret
        #if checkifrowFull == True:

        print('Come back for more! <3 Let us play again!')


    def checkifrowFull(self, r):
        """ Checks if a row is full of checkers or not
            returns true or false """

        H = self.height
        W = self.width

        for col in range (0,W):
                if self.data[r][col] == ' ':
                    return False
                
        return True #needs to be after the for loop ends and it goes throguh each col.




                

# Player Class Final Proejct

class Player:
    """An AI player for Connect Four."""

    def __init__(self, ox, tbt, ply):
        """Construct a player for a given checker, tie-breaking type,
           and ply.
           ply is the amount of moves the player can look ahead"""
        self.ox = ox
        self.tbt = tbt
        self.ply = ply

    def __repr__(self):
        """Create a string represenation of the player."""
        s = "Player for " + self.ox + "\n"
        s += "  with tiebreak type: " + self.tbt + "\n"
        s += "  and ply == " + str(self.ply) + "\n\n"
        return s

    def oppCh(self):
        """ returns the opposite checker of self.ox (a player)"""
        
        if self.ox == 'O':
            return 'X'
            
        else: #if self.ox == 'X':
            return 'O'

    
    def scoreBoard(self, b):
        """ returns a single float value representing the 
            input b (an object of type board). If the board b
            is a win for self, return 100
            if board b is neither win or loss, return 50
            if boars b is a loss, return 0
        """
        if b.winsFor(self.ox) == True:
            return 100.0
        elif b.winsFor(self.oppCh()) == True:
            return 0.0
        else:
            return 50.0

    def tiebreakMove(self, scores):
        """ takes scores which will be a nonempty
        list of floating-point numbers 
        returns a column number based on method chosen by player"""
        
        MS = max(scores) #100, 100, ..
        maxIndices = []
        

        for i in range(len(scores)):
            if MS == scores[i]: #square bracket to collect the index number of each list of index 0 - i
                maxIndices = maxIndices + [i] #maxIndices is the list of indexs/position of the max numbers

        #if len(maxIndices) == 1:
            #return maxIndices[0] #return the index number maxIndices is holding if maxIndices has only one number

        if self.tbt == 'LEFT':
             return maxIndices[0]
        elif self.tbt == 'RIGHT':
            return maxIndices[-1]
        else:
            return random.choice(maxIndices)

    def scoresFor(self, b):
        """ returns a list of scores with the xth score
            representing the "goodness" of the input board after 
            the player moved to column c. Goodness is measured 
            by what happens in the game after self.ply moves.
            
            scoresFor looks at all columns and returns the score that we
            will get by moving our checker into each of the columns

            returns a list of 7 numbers which will be either 100, 50, 0 or -1. 

            The way the function works.. is that for a board b

            | | | | | | | |
            | | | | | | | |
            | | | | |X| | |
            | |O| | |O| | |
            | |X|X| |X| | |
            | |X|O| |O|O| |
            ---------------
             0 1 2 3 4 5 6

            ScoresFor - if our opponent is O - will return [50,50,50,100,50,50,50]
            this is because, with the loop and recurssion, what happens is tha that
            col 3 for the opponent will score 100 until b.addmove(3) occurs. That is
            when the opponent's score will be 50 and so it will be the largest amount 
            when 100-opponent's score is taken. Thus it will be targetted as the best
            place for me to add my checker.
            
            """

        
        scores = [50]*b.width #list "scores" = length of 50 * the width of the board

        for col in range (b.width):
            if b.allowsMove(col) == False:
                scores[col] = -1
            elif b.winsFor(self.ox) == True:
                scores[col] = 100
            elif b.winsFor(self.oppCh()) == True:
                scores[col] = 0
            elif self.ply == 0:
                scores[col] = 50
            else:
                b.addMove(col, self.ox)
                op = Player(self.oppCh(), self.tbt, self.ply -1)
                opscores = op.scoresFor(b) # the seven scores th eopponent thinks it gets
                M = max(opscores)
                My = 100 - M #myscore
                scores[col] = My 
                b.delMove(col)

        return scores #list of scores


    def nextMove(self,b):
        """ This method accepts b, an object of type Board, 
        and returns an integer—namely, the column number that 
        the calling object (of class Player) chooses to move to.
        """
        return self.tiebreakMove(self.scoresFor(b))



b = Board(7,6)

"""
for r in range(1,4):
    for c in range(7):
        b.data[r][c] = 'X'
for r in range(4,6):
    for c in range(7):
        b.data[r][c] = 'O'

print(b)
"""

"""
px = Player('X', 'LEFT', 3)
po = Player('O', 'LEFT', 2)
"""

"""
for c in range(7):
    bot = b.data[5][c]
    up = b.data[3][c]
    b.data[5][c] = up
    b.data[3][c] = bot
print(b)

#variation = top row dissapears when full
            if self.checkifrowFull(0) == True:
                print("WARNING!!!!!! Board row dissapeared!")
                
                for c in range(self.width):
                    if self.data[0][c] != ' ':
                        self.data[0][c] = ' '
                    return
                    
                print(self)

"""

# File: CodeMeasure/TestScripts/MohanYoung.py
#file: final.py
#name: Tulika Mohan and Katharine Young

import random

# copied from hw10pr2
def inarow_Neast( ch, r_start, c_start, A, N ):
    """start from r_start and c_start and check for 
       N-in-a-row eastward of element ch, returning 
       True or False, as appropriate
    """
    NR = len(A)   
    NC = len(A[0])
    if r_start >= NR or c_start+ N-1 >= NC:   
        return False   
    for i in range(N):                  
        if A[r_start][c_start+i] != ch:   
            return False                
    return True   

def inarow_Nsouth( ch, r_start, c_start, A ,N):
    """start from r_start and c_start and check for 
       N-in-a-row southward of element ch, returning 
       True or False, as appropriate
    """
    NR = len(A)   
    NC = len(A[0])
    if r_start+N-1 >= NR or c_start >= NC:   
        return False   
    for i in range(N):                  
        if A[r_start+i][c_start] != ch:   
            return False                
    return True        

def inarow_Nsoutheast( ch, r_start, c_start, A, N ):
    """start from r_start and c_start and check for 
       N-in-a-row southeastward of element ch, returning 
       True or False, as appropriate
    """
    NR = len(A)   
    NC = len(A[0])
    if r_start+N-1 >= NR or c_start+N-1 >= NC:   
        return False   
    for i in range(N):                  
        if A[r_start+i][c_start+i] != ch:   
            return False                
    return True   

def inarow_Nnortheast( ch, r_start, c_start, A ,N):
    """start from r_start and c_start and check for 
       N-in-a-row northeastward of element ch, returning 
       True or False, as appropriate
    """
    NR = len(A)   
    NC = len(A[0])
    if r_start >= NR or c_start+N -1 >= NC:   
        return False   
    for i in range(N):                  
        if A[r_start-i][c_start+i] != ch:   
            return False                
    return True  






class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width 
        and height.
        """
        self.width = width
        self.height = height
        self.data = [[' ']*width for row in range(height)]

        # We do not need to return anything from a constructor!

    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = ''                          # the string to return
        for row in range(0, self.height):
            s += '|'
            for col in range(0, self.width):
                s += self.data[row][col] + '|'
            s += '\n'

        s += (2*self.width + 1) * '-'   # bottom of the board

        # and the numbers underneath here

        return s       # the board is complete, return it

    def addMove(self,col,ox):
        """This method takes two arguments: the first, col, 
        represents the index of the column to which the checker will be 
        added. The second argument, ox, will be a 1-character string 
        representing the checker to add to the board. That is, ox should 
        either be 'X' or 'O' (again, capital O, not zero).
        """
        H = self.height
        for row in range(0, H):
            if self.data[row][col] != ' ':
                self.data[row-1][col] = ox
                return
        self.data[H-1][col] = ox


    def clear(self):
        """clears out the board"""
        self.data = [ [' ']*W for row in range(H) ]   

    def setBoard(self, moveString):
        """Accepts a string of columns and places
           alternating checkers in those columns,
           starting with 'X'.

           For example, call b.setBoard('012345')
           to see 'X's and 'O's alternate on the
           bottom row, or b.setBoard('000000') to
           see them alternate in the left column.

           moveString must be a string of one-digit integers.
        """
        nextChecker = 'X'   # start by playing 'X'
        for colChar in moveString:
            col = int(colChar)
            if 0 <= col <= self.width:
                self.addMove(col, nextChecker)
            if nextChecker == 'X':
                nextChecker = 'O'
            else:
                nextChecker = 'X'

    def allowsMove(self,c):
        """this method should check to be sure that c is within the range 
        from 0 to the last column and make sure that there is still room 
        left in the column!
        """
        H = self.height
        W = self.width
        D = self.data

        if c not in range(self.width):
            return False
        else:
            for i in range(self.height):
                if self.data[i][c] == ' ':
                    return True
                else:
                    return False
        

    def isFull(self):
        """checks if board is full"""
        W = self.width
        D = self.data
        for a in range(W):
            if self.allowsMove(a) == True:
                return False
        return True    

    def delMove(self, c):
        """removes top checker from column c"""
        H = self.height
        for row in range(0, H):
            if self.data[row][c] != ' ':
                self.data[row][c] = ' '
                return    

    def winsFor(self,ox):
        """checks if someone wins the game"""
        H = self.height
        W = self.width
        D = self.data

        for r_start in range(H):
            for c_start in range(W):
                if inarow_Neast( ox, r_start, c_start, D, 4 ) == True:
                    return True 
                elif inarow_Nsouth( ox, r_start, c_start, D, 4 ) == True:
                    return True 
                elif inarow_Nnortheast( ox, r_start, c_start, D, 4 ) == True:
                    return True 
                elif inarow_Nsoutheast( ox, r_start, c_start, D, 4 )== True:
                    return True
        return False

    def colsToWin(self, ox):
        """the colsToWin method should return the list of columns 
        where ox can move in the next turn in order to win and finish 
        the game. arguments:ox, which will be either the string 'X' or 
        the string 'O'
        return value: list 
        """
        x = []
        for col in range(self.width):
            if self.allowsMove(col) == True:
                self.addMove(col, ox)
                if self.winsFor(ox) == True:
                    x+= [col]
                self.delMove(col)
        return x

    def aiMove(self, ox):
        """ accepts a single argument, ox, which will be either 
        the string 'X' or the string 'O'. aiMove returns a single integer, 
        which must be a legal column in which to make a move. 
        """
        if ox == 'O':
            opponent = 'X'
        else:
            opponent = 'Y'

        x = self.colsToWin(ox)
        y = self.colsToWin(opponent)
        options = list(range(self.width))  

        if x == []:  #this means you can't win 
            if y != []: #but opponent can win
                return (y[0])  #block opponent's winning move 
            else:
                while True:
                    choice = random.choice(options)
                    if self.allowsMove(choice) == True:
                        return (choice)     # plays random move if no one can win in this turn 
        else:
            return (x[0])                    

    def hostGame(self):
        """host connect4
        """
        print()
        print("Welcome to this game of Connect 4!")
        print (self)
        print()
        print("Choose your fighter!")
        ox = input("X,O, or Neither")

        while True:
            if ox == "Neither": #AI plays against itself
                users_col =self.aiMove('X')
            elif ox == "O": # user chooses to play O
                users_col = self.aiMove('X')
            else:
                users_col = int(input("X. Choose a column:"))
                while self.allowsMove(users_col) == False:
                    users_col = int(input("O. Choose a column"))      
            self.addMove(users_col, "X")    
          
            print(self)
            if self.winsFor("X") == True:
                print("Nicely done! You won")
                break
            if self.isFull() == True:
                print("Board is full! Better luck next time")
                break

            if ox =='X' or ox == 'Neither':
                users_col = self.aiMove('O')
            else:
                users_col = int(input("O. Choose a column:"))   
                while self.allowsMove(users_col) == False:
                    users_col = int(input("X. Choose a column")) 
            self.addMove(users_col,"O")
            print(self)
            if self.winsFor("O") == True:
                print("Nicely done! You won")
                break
            if self.isFull() == True:
                print("Board is full! Better luck next time")
                break    




    def playGame(self, px, po):
        """ calls nextMove for two objects (px and po) of type Player in order to
            play a game 
        """
        nextCheckerToMove = 'X'


        while True:
            if nextCheckerToMove == 'X':
                plr = px
            else:
                plr = po
                
            #print C4 board
            print (self)
            if plr != 'human':
                col = -1
                while not self.allowsMove( col ):
                    col = plr.nextMove(self)
                self.addMove( col, nextCheckerToMove )
            else:
                col = -1
                while not self.allowsMove( col ):
                    col = input('Next col for ' + nextCheckerToMove + ': ')
                self.addMove( col, nextCheckerToMove )
            
            #check if the game is over
            if self.winsFor( nextCheckerToMove ):
                print (self)
                print ('\n' + nextCheckerToMove + ' wins! Good job!\n\n')
                break
            if self.isFull():
                print (self)
                print ('\nThe game is a tie. What a bummer! \n\n')
                break

            #connect 4 variation: pieces swapped with opponent's pieces
            if random.choice(range(15)) == 0:
                print ('Oops! The board has magically swapped all of your pieces with your opponents. Player X, continue playing the X pieces. Player O, continue playing the O pieces. Can you beat your own strategy?')
                print ('Good luck!')
                for row in range(0, self.height):
                    for col in range(0, self.width):
                        if self.data[row][col] == 'X':
                            self.data[row][col] = 'O'
                        elif self.data[row][col] == 'O':
                            self.data[row][col] = 'X'      



            # switch players
            if nextCheckerToMove == 'X':
                nextCheckerToMove = 'O'
            else:
                nextCheckerToMove = 'X'

        print ('Byyyyyyeeeee')







class Player:
    """An AI player for Connect Four."""

    def __init__(self, ox, tbt, ply):
        """Construct a player for a given checker, tie-breaking type,
           and ply.
        """
        self.ox = ox
        self.tbt = tbt
        self.ply = ply

    def __repr__(self):
        """Create a string represenation of the player.
        """
        s = "Player for " + self.ox + "\n"
        s += "  with tiebreak type: " + self.tbt + "\n"
        s += "  and ply == " + str(self.ply) + "\n\n"
        return s


    def oppCh(self): 
        """ return the other kind of checker or playing piece, i.e., 
        the piece being played by self's opponent.
        """
        if self.ox == 'X':
            return 'O'
        else: 
            return 'X'

    def scoreBoard(self, b):
        """returns a single float value representing the score of 
        the input b, which you may assume will be an object of type Board. 
        This should return 100.0 if the board b is a win for self. It should 
        return 50.0 if it is neither a win nor a loss for self, and it should 
        return 0.0 if it is a loss for self (i.e., the opponent has won)"""
        if b.winsFor(self.ox):
            return 100
        elif b.winsFor(self.oppCh()):  
            return 0
        else:
            return 50    

    def tiebreakMove(self, scores):
        """This method takes in scores, which will be a nonempty list of 
        floating-point numbers, and returns its column number. If there is 
        more than one highest score because of a tie, this method should return 
        the COLUMN number of the highest score appropriate to the player's 
        tiebreaking type."""
        maxIndices = []
        maxscores = max(scores)
        for x in range(len(scores)):
            if maxscores == scores[x]:
                maxIndices += [x]
        if len(maxIndices) == 1:
            return maxIndices[0] 
        else:          
            if self.tbt == 'RIGHT':
                return maxIndices[len(maxIndices)-1]
            elif self.tbt == 'LEFT':
                return maxIndices[0]
            elif self.tbt == 'RANDOM':
                c = random.choice(range(len(maxIndices)))
                return maxIndices[c]   

    def scoresFor(self,b):
        """returns a list of scores, with the cth score representing 
        the "goodness" of the input board after the player moves to column c. 
        And, "goodness" is measured by what happens in the game after self.ply 
        moves """
        scores= [50,50,50,50,50,50,50]
        for col in range(7):
            if b.allowsMove(col) == False:
                scores[col] = -1
            elif b.winsFor(self.ox) == True:
                scores[col] = 100
            elif b.winsFor(self.oppCh()) == True:
                scores[col] = 0
            elif self.ply == 0:
                scores [col] = 50
            else:
                b.addMove(col,self.ox)
                if b.winsFor(self.ox) == True:
                    scores[col]=100
                else:
                    op = Player(self.oppCh(), self.tbt, self.ply-1)
                    opsc = op.scoresFor(b)
                    opscmax = max(opsc)
                    scores[col] = (100 - opscmax)
                b.delMove(col)
                
        return scores     

    def nextMove(self, b):
        """ accepts b and returns an integer which represents the column number 
            that the calling object (player) chooses to move to."""
        return self.tiebreakMove(self.scoresFor(b))

# File: CodeMeasure/TestScripts/tetris.py
# tetris.py

# wow! it's the final project!


class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.data = [[' ']*width for row in range(height)]

        # We do not need to return anything from a constructor!

    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = ''                          # the string to return
        for row in range(0, self.height):
            s += '|'
            for col in range(0, self.width):
                s += self.data[row][col] + '|'
            s += '\n'

        s += (2*self.width + 1) * '-'   # bottom of the board

        # and the numbers underneath here
        s += '\n'
        for i in range(0, col+1):
            s += ' ' + str((i)%10)


        return s       # the board is complete, return it
    
    def addMove(self, col, ox):
        """ addMove takes arguments col (index of column) and ox (1-character
            string X or O).
        """
        H = self.height
        for row in range(0, H):
            if self.data[row][col] != ' ':
                self.data[row-1][col] = ox
                return
        
        self.data[H-1][col] = ox

    def clear(self):
        """ clear should clear the board """
        for r in range(0, self.height):
            for c in range(0, self.width):
                if self.data[r][c] != ' ':
                    self.data[r][c] = ' '
        
        return self

    def setBoard(self, moveString):
        """Accepts a string of columns and places
           alternating checkers in those columns,
           starting with 'X'.

           For example, call b.setBoard('012345')
           to see 'X's and 'O's alternate on the
           bottom row, or b.setBoard('000000') to
           see them alternate in the left column.

           moveString must be a string of one-digit integers.
        """
        nextChecker = 'X'   # start by playing 'X'
        for colChar in moveString:
            col = int(colChar)
            if 0 <= col <= self.width:
                self.addMove(col, nextChecker)
            if nextChecker == 'X':
                nextChecker = 'O'
            else:
                nextChecker = 'X'
    
    def allowsMove(self, c):
        """ Returns True if the calling object allows a move into column c. 
            Returns False if column c is not a legal column number.
            Returns false if column c is full.
        """
        
        if c in range(0, self.width):
            if self.data[0][c] != ' ':
                return False          
            elif self.data[0][c] == ' ':
                return True
        else:
            return False
    
    def isFull(self):
        """ returns True if calling object is full.
            returns False otherwise.
        """

        for col in range(0, self.width):
            for row in range(0, self.height):
                if self.data[row][col] == ' ':
                    return False
                
        return True

    def delMove(self, c):
        """ Removes top checker from column c. If column empty, it does nothing. """

        H = self.height
        for row in range(0, H):
            if self.data[row][c] != ' ':
                self.data[row][c] = ' '
                return
        
        self.data[H-1][c] = ' '
    

    def winsFor(self, ox):
        """ takes 'X' or 'O' as an argument. 
            returns True if there are four checkers of type ox in a row on the board.
            returns False otherwise.
        """
        H = self.height
        W = self.width
        D = self.data
        # Check for horizontal wins
        for row in range(0, H):
            for col in range(0, W - 3):
                if D[row][col] == ox and \
                   D[row][col + 1] == ox and \
                   D[row][col + 2] == ox and \
                   D[row][col + 3] == ox:
                    return True
        #vertical wins
        for col in range(0, W):
            for row in range(0, H-3):
                if D[row][col] == ox and \
                   D[row+1][col] == ox and \
                   D[row+2][col] == ox and \
                   D[row+3][col] == ox:
                    return True
        #diagonal wins (1)
        for col in range(0, W-3):
            for row in range(0, H-3):
                if D[row][col] == ox and \
                   D[row+1][col+1] == ox and \
                   D[row+2][col+2] == ox and \
                   D[row+3][col+3] == ox:
                    return True
        #diagonal wins (2)
        for col in range(3, W):
            for row in range(0, H-3):
                if D[row][col] == ox and \
                   D[row+1][col-1] == ox and \
                   D[row+2][col-2] == ox and \
                   D[row+3][col-3] == ox:
                    return True
        else: 
            return False

    def colsToWin(self, ox):
        """ intakes an argument 'O' or 'X' and returns the list of columns where ox
            can move in the next turn to win the game... """
        
        W = self.width
        D = self.data
        L = []

        for col in range(0, W):
            if self.allowsMove(col) == True:
                self.addMove(col, ox)
                if self.winsFor(ox) == True:
                    L += [col]
                self.delMove(col)
        return L
                
    def aiMove(self, ox):
        """ accepts 'O' or 'X' and returns an integer, which is a column
            in which to make a move. """
        
        W = self.width
        L = self.colsToWin(ox)

        if L != []:
            return int(L[0])
        else: 
            if ox == 'O':
                oppx = 'X'
                M = self.colsToWin(oppx)
                if M != []:
                   return int(M[0])
                else:
                    if self.allowsMove(0) == True:
                        return 0
                    elif self.allowsMove(W/2) == True:
                        return int(W/2)
                    else:
                        return int(W)
                    
            else:
                oppo = 'O'
                N = self.colsToWin(oppo)
                if N != []:
                   return int(N[0])
                else:
                    if self.allowsMove(0) == True:
                        return 0
                    elif self.allowsMove(W/2) == True:
                        return int(W/2)
                    else:
                        return int(W)
            #check if blocking is possible

    def checkRow(self):
        """ checkRow checks if row r is full; returns True if full.
        """
        W = self.width
        H = self.height
        
        for c in range(0, W):
            if self.data[H-1][c] == ' ':
                return False
        return True


    def delRow(self, r):
        """ delRow deletes row r and then makes everything fall.
        """

        W = self.width
        H = self.height

        for r in range(r-1, -1, -1):
            for c in range(0, W):
                self.data[r+1][c] = self.data[r][c]
        for c in range(0, W):
            self.data[0][c] = ' '       
        
      




    def hostGame(self):
        """ hosts a game of Connect Four """

        print()
        print('hi. let us play Connect Four.')
        print()
        print(self)
        print()

        while True:
            print()
            users_col = int(input("X's choice: "))
            print()  
            while self.allowsMove(users_col) == False:
                users_col = int(input("Choose a column: "))
        
            self.addMove(users_col, 'X')
            print(self)

            if self.winsFor('X') == True:
                print('X wins!')
                print(self)
                break
            elif self.isFull() == True:
                print('tie!')
                print(self)
                break


            print()
            o_col = int(aiMove('O'))
            print()
        
            self.addMove(o_col, 'O')
            print(self)
        
            if self.winsFor('O') == True:
                print('O wins!')
                print(self)
                break
            elif self.isFull() == True:
                print('tie!')
                print(self)
                break

    def playGame(self, px, po):
        """Plays a game of Connect Four.
            p1 and p2 are objects of type Player OR
            the string 'human'.
        """

        nextCheckerToMove = 'X'
        nextPlayerToMove = px

        while True:

            # print the current board
            print(self)

            # choose the next move
            if nextPlayerToMove == 'human':
                col = -1
                while not self.allowsMove(col):
                    col = int(input('Next col for ' + nextCheckerToMove + ': '))
            else: # it's a computer player
                col = nextPlayerToMove.nextMove(self)

            # add the checker to the board
            self.addMove(col, nextCheckerToMove)

            # check if game is over
            if self.winsFor(nextCheckerToMove):
                print(self)
                print('\n' + nextCheckerToMove + ' wins! Congratulations!\n\n')
                break
            if self.isFull():
                print(self)
                print('\nThe game is a draw.\n\n')
                break
            
            #check if bottom row is full
            if self.checkRow() == True:
                self.delRow(5)
                print('Tetris :))')
                print(self)

            # swap players
            if nextCheckerToMove == 'X':
                nextCheckerToMove = 'O'
                nextPlayerToMove = po
            else:
                nextCheckerToMove = 'X'
                nextPlayerToMove = px

        print('Thanks for playing!')



class Player:
    """An AI player for Connect Four."""

    def __init__(self, ox, tbt, ply):
        """Constructs a player for a given checker, tie-breaking type,
           and ply."""
        self.ox = ox
        self.tbt = tbt
        self.ply = ply

    def __repr__(self):
        """Creates a string represenation of the player."""
    
        s = "\n" "Player for " + self.ox + "\n"
        s += "  tiebreak type: " + self.tbt + "\n"
        s += "  ply == " + str(self.ply) + "\n\n"
        return s

    def oppCh(self):
        """Returns the other playing piece."""

        if self.ox == 'O':    
            s = 'X'
            return s
        elif self.ox == 'X':    
            s = 'O'
            return s

    def scoreBoard(self, b):
        """ Returns single float value representing score of input b
            (of type board). 
                Returns 100.0 if b is a win for self
                Returns 50.0 if b is a tie for self
                Returns 0.0 if b is a loss for self
        """
        a = self.ox
        d = self.oppCh()

        if b.winsFor(d) == True:
            return 0.0
        elif b.winsFor(a) == True:
            return 100.0
        else:
            return 50.0
    
    def tiebreakMove(self, scores): # ????
        """ Takes in scores, a nonempty list of floating-point numbers.
            
            If there's only one highest score in the list, returns COLUMN NUMBER.
            If there's more than one highest score, returns COLUMN NUMBER 
            based on tiebreak type.
        """

        m = max(scores) # max of the scores
        maxInd = []
        
        for n in range(0, len(scores)):
            if scores[n] == m:
                maxInd += [n]
        
        # wow I can't believe i voluntarily wrote a for loop 
        # what have I become

        if self.tbt == 'LEFT':
            mcol = maxInd[0]
            return mcol 
        elif self.tbt == 'RIGHT':
            l = len(maxInd) - 1
            mcol = maxInd[l]
            return mcol

    def scoresFor(self, b):
        """ Returns list of scores with cth score representing how 'good' the 
            input board is after the player moves to column c, as measured by
            what follows once self.ply moves.
        """

        scores = [50]*b.width
        H = b.height
        W = b.width
        D = b.data

        a = self.ox
        d = self.oppCh()

        for c in range (0, W):
            if b.allowsMove(c) != True:
                scores[c] = -1.0
            elif b.winsFor(a) == True:
                scores[c] = 100.0
            elif b.winsFor(d) == True:
                scores[c] = 0.0
            elif self.ply == 0:
                scores[c] = 50.0
            else:
                b.addMove(c, a)
                op = Player(self.oppCh(), self.tbt, self.ply-1)
                m = max(op.scoresFor(b))
                s = 100 - m
                scores[c] = s
                b.delMove(c)
        return scores

    def nextMove(self, b):
        """ Accepts b (board) and returns integer (column number that the 
            calling object chooses to move to).
        """

        return self.tiebreakMove(self.scoresFor(b))
# final.py

# wow! it's the final project!


class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.data = [[' ']*width for row in range(height)]

        # We do not need to return anything from a constructor!

    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = ''                          # the string to return
        for row in range(0, self.height):
            s += '|'
            for col in range(0, self.width):
                s += self.data[row][col] + '|'
            s += '\n'

        s += (2*self.width + 1) * '-'   # bottom of the board

        # and the numbers underneath here
        s += '\n'
        for i in range(0, col+1):
            s += ' ' + str((i)%10)


        return s       # the board is complete, return it
    
    def addMove(self, col, ox):
        """ addMove takes arguments col (index of column) and ox (1-character
            string X or O).
        """
        H = self.height
        for row in range(0, H):
            if self.data[row][col] != ' ':
                self.data[row-1][col] = ox
                return
        
        self.data[H-1][col] = ox

    def clear(self):
        """ clear should clear the board """
        for r in range(0, self.height):
            for c in range(0, self.width):
                if self.data[r][c] != ' ':
                    self.data[r][c] = ' '
        
        return self

    def setBoard(self, moveString):
        """Accepts a string of columns and places
           alternating checkers in those columns,
           starting with 'X'.

           For example, call b.setBoard('012345')
           to see 'X's and 'O's alternate on the
           bottom row, or b.setBoard('000000') to
           see them alternate in the left column.

           moveString must be a string of one-digit integers.
        """
        nextChecker = 'X'   # start by playing 'X'
        for colChar in moveString:
            col = int(colChar)
            if 0 <= col <= self.width:
                self.addMove(col, nextChecker)
            if nextChecker == 'X':
                nextChecker = 'O'
            else:
                nextChecker = 'X'
    
    def allowsMove(self, c):
        """ Returns True if the calling object allows a move into column c. 
            Returns False if column c is not a legal column number.
            Returns false if column c is full.
        """
        
        if c in range(0, self.width):
            if self.data[0][c] != ' ':
                return False          
            elif self.data[0][c] == ' ':
                return True
        else:
            return False
    
    def isFull(self):
        """ returns True if calling object is full.
            returns False otherwise.
        """

        for col in range(0, self.width):
            for row in range(0, self.height):
                if self.data[row][col] == ' ':
                    return False
                
        return True

    def delMove(self, c):
        """ Removes top checker from column c. If column empty, it does nothing. """

        H = self.height
        for row in range(0, H):
            if self.data[row][c] != ' ':
                self.data[row][c] = ' '
                return
        
        self.data[H-1][c] = ' '
    

    def winsFor(self, ox):
        """ takes 'X' or 'O' as an argument. 
            returns True if there are four checkers of type ox in a row on the board.
            returns False otherwise.
        """
        H = self.height
        W = self.width
        D = self.data
        # Check for horizontal wins
        for row in range(0, H):
            for col in range(0, W - 3):
                if D[row][col] == ox and \
                   D[row][col + 1] == ox and \
                   D[row][col + 2] == ox and \
                   D[row][col + 3] == ox:
                    return True
        #vertical wins
        for col in range(0, W):
            for row in range(0, H-3):
                if D[row][col] == ox and \
                   D[row+1][col] == ox and \
                   D[row+2][col] == ox and \
                   D[row+3][col] == ox:
                    return True
        #diagonal wins (1)
        for col in range(0, W-3):
            for row in range(0, H-3):
                if D[row][col] == ox and \
                   D[row+1][col+1] == ox and \
                   D[row+2][col+2] == ox and \
                   D[row+3][col+3] == ox:
                    return True
        #diagonal wins (2)
        for col in range(3, W):
            for row in range(0, H-3):
                if D[row][col] == ox and \
                   D[row+1][col-1] == ox and \
                   D[row+2][col-2] == ox and \
                   D[row+3][col-3] == ox:
                    return True
        else: 
            return False

    def colsToWin(self, ox):
        """ intakes an argument 'O' or 'X' and returns the list of columns where ox
            can move in the next turn to win the game... """
        
        W = self.width
        D = self.data
        L = []

        for col in range(0, W):
            if self.allowsMove(col) == True:
                self.addMove(col, ox)
                if self.winsFor(ox) == True:
                    L += [col]
                self.delMove(col)
        return L
                
    def aiMove(self, ox):
        """ accepts 'O' or 'X' and returns an integer, which is a column
            in which to make a move. """
        
        W = self.width
        L = self.colsToWin(ox)

        if L != []:
            return int(L[0])
        else: 
            if ox == 'O':
                oppx = 'X'
                M = self.colsToWin(oppx)
                if M != []:
                   return int(M[0])
                else:
                    if self.allowsMove(0) == True:
                        return 0
                    elif self.allowsMove(W/2) == True:
                        return int(W/2)
                    else:
                        return int(W)
                    
            else:
                oppo = 'O'
                N = self.colsToWin(oppo)
                if N != []:
                   return int(N[0])
                else:
                    if self.allowsMove(0) == True:
                        return 0
                    elif self.allowsMove(W/2) == True:
                        return int(W/2)
                    else:
                        return int(W)
            #check if blocking is possible
            
        
      




    def hostGame(self):
        """ hosts a game of Connect Four """

        print()
        print('hi. let us play Connect Four.')
        print()
        print(self)
        print()

        while True:
            print()
            users_col = int(input("X's choice: "))
            print()  
            while self.allowsMove(users_col) == False:
                users_col = int(input("Choose a column: "))
        
            self.addMove(users_col, 'X')
            print(self)

            if self.winsFor('X') == True:
                print('X wins!')
                print(self)
                break
            elif self.isFull() == True:
                print('tie!')
                print(self)
                break


            print()
            o_col = int(aiMove('O'))
            print()
        
            self.addMove(o_col, 'O')
            print(self)
        
            if self.winsFor('O') == True:
                print('O wins!')
                print(self)
                break
            elif self.isFull() == True:
                print('tie!')
                print(self)
                break

    def playGame(self, pForX, pForO):
        """Plays a game of Connect Four.
            p1 and p2 are objects of type Player OR
            the string 'human'.
        """

        nextCheckerToMove = 'X'
        nextPlayerToMove = pForX

        while True:

            # print the current board
            print(self)

            # choose the next move
            if nextPlayerToMove == 'human':
                col = -1
                while not self.allowsMove(col):
                    col = int(input('Next col for ' + nextCheckerToMove + ': '))
            else: # it's a computer player
                col = nextPlayerToMove.nextMove(self)

            # add the checker to the board
            self.addMove(col, nextCheckerToMove)

            # check if game is over
            if self.winsFor(nextCheckerToMove):
                print(self)
                print('\n' + nextCheckerToMove + ' wins! Congratulations!\n\n')
                break
            if self.isFull():
                print(self)
                print('\nThe game is a draw.\n\n')
                break

            # swap players
            if nextCheckerToMove == 'X':
                nextCheckerToMove = 'O'
                nextPlayerToMove = pForO
            else:
                nextCheckerToMove = 'X'
                nextPlayerToMove = pForX

        print('Thanks for playing!')




class Player:
    """An AI player for Connect Four."""

    def __init__(self, ox, tbt, ply):
        """Constructs a player for a given checker, tie-breaking type,
           and ply."""
        self.ox = ox
        self.tbt = tbt
        self.ply = ply

    def __repr__(self):
        """Creates a string represenation of the player."""
    
        s = "\n" "Player for " + self.ox + "\n"
        s += "  tiebreak type: " + self.tbt + "\n"
        s += "  ply == " + str(self.ply) + "\n\n"
        return s

    def oppCh(self):
        """Returns the other playing piece."""

        if self.ox == 'O':    
            s = 'X'
            return s
        elif self.ox == 'X':    
            s = 'O'
            return s

    def scoreBoard(self, b):
        """ Returns single float value representing score of input b
            (of type board). 
                Returns 100.0 if b is a win for self
                Returns 50.0 if b is a tie for self
                Returns 0.0 if b is a loss for self
        """
        a = self.ox
        d = self.oppCh()

        if b.winsFor(d) == True:
            return 0.0
        elif b.winsFor(a) == True:
            return 100.0
        else:
            return 50.0
    
    def tiebreakMove(self, scores): # ????
        """ Takes in scores, a nonempty list of floating-point numbers.
            
            If there's only one highest score in the list, returns COLUMN NUMBER.
            If there's more than one highest score, returns COLUMN NUMBER 
            based on tiebreak type.
        """

        m = max(scores) # max of the scores
        maxInd = []
        
        for n in range(0, len(scores)):
            if scores[n] == m:
                maxInd += [n]
        
        # wow I can't believe i voluntarily wrote a for loop 
        # what have I become

        if self.tbt == 'LEFT':
            mcol = maxInd[0]
            return mcol 
        elif self.tbt == 'RIGHT':
            l = len(maxInd) - 1
            mcol = maxInd[l]
            return mcol

    def scoresFor(self, b):
        """ Returns list of scores with cth score representing how 'good' the 
            input board is after the player moves to column c, as measured by
            what follows once self.ply moves.
        """

        scores = [50]*b.width
        H = b.height
        W = b.width
        D = b.data

        a = self.ox
        d = self.oppCh()

        for c in range (0, W):
            if b.allowsMove(c) != True:
                scores[c] = -1.0
            elif b.winsFor(a) == True:
                scores[c] = 100.0
            elif b.winsFor(d) == True:
                scores[c] = 0.0
            elif self.ply == 0:
                scores[c] = 50.0
            else:
                b.addMove(c, a)
                op = Player(self.oppCh(), self.tbt, self.ply-1)
                m = max(op.scoresFor(b))
                s = 100 - m
                scores[c] = s
                b.delMove(c)
        return scores

    def nextMove(self, b):
        """ Accepts b (board) and returns integer (column number that the 
            calling object chooses to move to).
        """

        return self.tiebreakMove(self.scoresFor(b))

