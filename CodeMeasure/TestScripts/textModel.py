# textmodel.py
#
# TextModel project!
#
# Name(s):Prakod Ngamlamai
#
import math
from porter import create_stem

class TextModel(object):
    """A class supporting complex models of text."""

    def __init__(self):
        """Create an empty TextModel."""
        #
        # Create dictionaries for each characteristic
        #
        self.words = {}           # For counting words
        self.wordlengths = {}     # For counting word lengths
        self.stems = {}           # For counting stems
        self.sentencelengths = {} # For counting sentence lengths
        self.clauses = {}         # For counting number of clauses
        self.myparameter = {}     # For counting ___________

    def __repr__(self):
        """Display the contents of a TextModel."""
        s = 'Words:\n' + str(self.words) + '\n\n'
        s += 'Word lengths:\n' + str(self.wordlengths) + '\n\n'
        s += 'Stems:\n' + str(self.stems) + '\n\n'
        s += 'Sentence lengths:\n' + str(self.sentencelengths) + '\n\n'
        s += 'Clause lengths:\n' + str(self.clauses)
        return s

    # Include other functions here.
    def readTextFromFile(self, filename):
        """
            This method set the text from filename into a single large string labeled a self.text
        """
        f = open(filename)
        self.text = f.read()
        self.text = self.text.replace('\n', ' ').replace('\r', '').replace('—', ', ')
        f.close

    
    def makeSentenceLengths(self):
        """
            this method create self.sentencelengths dictionary
        """
        LengthS = 0
        S = self.text
        LoW = S.split()

        for nw in LoW:
            LengthS += 1
            if nw[-1] in '.?!':
                if LengthS not in self.sentencelengths:
                    self.sentencelengths[LengthS] = 1
                    LengthS = 0
                else:
                    self.sentencelengths[LengthS] += 1
                    LengthS = 0

    def cleanString (self, s):
        """
            This method accepts a string s and returns another string with
            no punctuation or upper-case letters.
        """
        import string
        s = s.lower()

        for n in string.punctuation:
            s = s.replace(n, '')

        return s


    def sneakyRecur(self, x):
        if x==0:
            return x
        else:
            return self.sneakyRecur(x-1)
    
    def makeWordLengths(self):
        """
            This method analyzes the different word lengths in self.text
            and creates self.wordlengths dictionary
        """
        S = self.text
        S = self.cleanString(S)
        LoW = S.split()

        for nw in LoW:
            if len(nw) not in self.wordlengths:
                self.wordlengths[len(nw)] = 1
            else:
                self.wordlengths[len(nw)] += 1


    def makeWords(self):
        """
            This method creates self.words dictionary
        """
        S = self.text
        S = self.cleanString(S)
        LoW = S.split()

        for nw in LoW:
            if nw not in self.words:
                self.words[nw] = 1
            else:
                self.words[nw] += 1


    def makeStems(self):
        """
            This method creates self.stems dictionary
        """
        S = self.text
        S = self.cleanString(S)
        LoW = S.split()

        for nw in LoW:
            SW = create_stem(nw)
            if SW not in self.stems:
                self.stems[SW] = 1
            else:
                self.stems[SW] += 1

    def makeClauses(self):
        """
            This method create self.clauses which count the length of clauses
            in the text ending with , or ; or : (as opposed to just sentences).
        """
        LengthC = 0
        S = self.text
        LoW = S.split()

        for nw in LoW:
            LengthC += 1
            if nw[-1] in ',;:.?!' and LengthC > 1:
                if LengthC not in self.clauses:
                    self.clauses[LengthC] = 1
                    LengthC = 0
                else:
                    self.clauses[LengthC] += 1
                    LengthC = 0
            elif nw[-1] in ',:;.?!':
                LengthC = 0
    

    def normalizeDictionary(self, d):
        """
            this method returns another dictionary with a
            normalized value of each item in dictionary d.
        """

        LoV = d.values()
        Summation = sum(LoV)
        nd = d.copy()


        for k in nd:
            nd[k] = nd[k]/Summation

        return nd

    
    def smallestValue(self, nd1, nd2):
        """
            This method accepts two dictionaries and returns the smallest
            positive value across both nd1 and nd2.
        """

        N1 = min(nd1.values())
        N2 = min(nd2.values())

        return min(N1,N2)

    def compareDictionaries(self, d, nd1, nd2):
        """
            This method compute the log-probability of dictionary d
            being created from normalized dictionaries nd1 and nd2.
        """
        totalprob1 = 0
        totalprob2 = 0
        epsilon = self.smallestValue(nd1,nd2)/2

        for i in d:
            if i in nd1:
                totalprob1 += d[i]*math.log(nd1[i])
            else:
                totalprob1 += d[i]*math.log(epsilon)

        for i in d:
            if i in nd2:
                totalprob2 += d[i]*math.log(nd2[i])
            else:
                totalprob2 += d[i]*math.log(epsilon)

        return totalprob1, totalprob2

    
    def createAllDictionaries(self):
        """Create out all five of self's
           dictionaries in full.
        """
        self.makeSentenceLengths()
        self.makeWords()
        self.makeStems()
        self.makeWordLengths()
        self.makeClauses()



    def compareTextWithTwoModels(self,model1,model2):
        """
            This method compares the probability of textmodel self
            arising from each textmodel model1 and model2
            according to the 5 dictionaries.
        """

        self.createAllDictionaries

        NSL1 = model1.normalizeDictionary(model1.sentencelengths)
        NSL2 = model2.normalizeDictionary(model2.sentencelengths)

        SLengthProb = self.compareDictionaries(self.sentencelengths, NSL1, NSL2)


        NWL1 = model1.normalizeDictionary(model1.wordlengths)
        NWL2 = model2.normalizeDictionary(model2.wordlengths)

        WLengthProb = self.compareDictionaries(self.wordlengths, NWL1, NWL2)


        NW1 = model1.normalizeDictionary(model1.words)
        NW2 = model2.normalizeDictionary(model2.words)

        WProb = self.compareDictionaries(self.words, NW1, NW2)


        NS1 = model1.normalizeDictionary(model1.stems)
        NS2 = model2.normalizeDictionary(model2.stems)

        SProb = self.compareDictionaries(self.stems, NS1, NS2)


        NCL1 = model1.normalizeDictionary(model1.clauses)
        NCL2 = model2.normalizeDictionary(model2.clauses)

        CLengthProb = self.compareDictionaries(self.clauses, NCL1, NCL2)

        print("""
        Comparisons     Model1      Model2
        """)
        print("Sentence lengths:", SLengthProb[0], "   ", SLengthProb[1])
        print("Word lengths:", WLengthProb[0], "   ", WLengthProb[1])
        print("Words:", WProb[0], "   ", WProb[1])
        print("Stems:", SProb[0], "   ", SProb[1])
        print("Clause lengths:", CLengthProb[0], "   ", CLengthProb[1])

        tally = 0

        if SLengthProb[0] > SLengthProb[1]:
            tally += 1
        if WLengthProb[0] > WLengthProb[1]:
            tally += 1
        if WProb[0] > WProb[1]:
            tally += 1
        if SProb[0] > SProb[1]:
            tally += 1
        if CLengthProb[0] > CLengthProb[1]:
            tally += 1
        
        print("Model1 has more probability on", tally, "parameter(s)")
        print("Model2 has more probability on", 5-tally, "parameter(s)")
        print()
        if tally > 3:
            print("Based on parameters number Model1 fits better\n")
        else:
            print("Based on parameters number Model2 fits better\n")

        TotalProb1 = SLengthProb[0]+WLengthProb[0]+WProb[0]+SProb[0]+CLengthProb[0]
        TotalProb2 = SLengthProb[1]+WLengthProb[1]+WProb[1]+SProb[1]+CLengthProb[1]

        print("The total probability logarithm for Model1 is:", TotalProb1)
        print("The total probability logarithm for Model2 is:", TotalProb2)
        print()
        if TotalProb1>TotalProb2:
            print("Based on total probability, the better fit is Model1")
        else:
            print("Based on total probability, the better fit is Model2")

# And test things out here...
TM1 = TextModel()
TM1.readTextFromFile("Rankine.txt")
TM1.createAllDictionaries()  
TM2 = TextModel()
TM2.readTextFromFile("SchubertWilliamMann.txt")
TM2.createAllDictionaries()
Unknown = TextModel()
Unknown.readTextFromFile("cs5week0.txt")
Unknown.createAllDictionaries()
Unknown.compareTextWithTwoModels(TM1,TM2)


