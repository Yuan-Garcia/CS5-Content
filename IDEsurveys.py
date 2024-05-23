# IDE Survey data analysis

# import
import math
#import mathplotlib.pyplot as plt

# data
allData = "CS5, E80, N/A, Prob/stats for engineering, Bio 46, CS 42, CS5, Bio42, Phys024A, CS5, BIOL108, N/A, CS 5, CS5, N/A, CS5, Bio 154, Bio 54, MCB 118B, CS5, Bio 46, Math 73, CS5, Math 56, Cs5, cs70, CS5, N/A, CS70, CS 5, Bio 46, CS060 and CS5, CS42, E80 sometimes, N/A, Math 19, CS5, CS60, Bio 46, personal projects, CS5, CS70, CS81, 5, 70, 81, 140, 131, 105, 181Y, 181V, CS5, N/A, Bio 46, CS 5, CS 60, CS42, CS70, and all of the frosh/soph math/physics classes, MATH19, CS5, MATH73, CS5, Biology 46, CS5, CS60, cs5, Cs5, Cs70, cs105, cs81, Combinatorics, CS5 Black, CS70, CS81, CS105, CS5, Bio046, CS42, CS70, CS140, E85, E80, CS70, CS5, Bio, Physics 64 (Mathematical and Computational Methods for Physicists) and CSCI005, CS101, Experimental Engineering, CS5, E80, CS42, CS5, CS60, CS Classes in High School, CSCI042, BIOL046, CS 5, E80, MATH 56, CS5, CS50, MATH19, MATH73, CS 5, Probstats, CS70, bio 46, phys 24A, cs 42, CS 42, Phys 24A, Chem 24, CS42, BIOL46, Math 56 (Stats/Probability for Engineers), E80 (Experimental Engineering), Biology, CS5, Phys64, CS5, cs5, cs70, cs81 (one time), cs105, cs131, all my electives, N/A, CS5, CS70, CS81, Math131 (for latex), CS42, PHYS64, research, CS5 and BIO46, CS 5, 60, 70, 105 + PHYS 064, E80, PHYS64 (Math Comp Methods for Physicists), CS5, CORE79, CS5, bio46, CS 5, bio, cs42, CS5, Bio46, CS5 Gold, CS5, CS5, N/A, CS5, Used it for basically all cs classes CS42, CS70, CS81 (a little), CS131, CS105, CS158, CS152, CS123, CS140, Math187, Core79, Bio23, all cs major courses, cs42, cs70, physics 64, math 55, CS42, Phys24A, CS5, CS70, CS 42, CS5: Gold, Research in Physics, Cs5, N/A, Cs5, e80, Cs5, CS5, Math164, CS5 Gold, MCB118b (Intro to Computational Biology), CS5, CS70, Math189, CS5, CS5, CS70, PHYS64: Math & Computational Methods for Physicists, CSCI042, BIOL046, MATH073, PHYS024A, CS5"
splitData = allData.split(", ")
splitData = [x.lower() for x in splitData]
print(splitData)

# counting each class
cs5 = 0
cs42 = 0
cs70 = 0
cs60 = 0
cs81 = 0
cs101 = 0
cs105 = 0
cs131 = 0
cs140 = 0
cs152 = 0

math19 = 0
math55 = 0
math56 = 0
math73 = 0
math164 = 0
math157 = 0
math187 = 0
math189 = 0
math131 = 0

phys24 = 0
phys64 = 0

bio23 = 0
bio46 = 0
bio54 = 0
bio108 = 0
mcb118b = 0

for i in splitData:
    if i.contains("cs5") or i.contains("cs 5") or i.contains("cs5 gold") or i.contains("cs5 black"):
        cs5 += 1
    if i.contains("42"):
        cs42 += 1
    if i.contains("70"):
        cs70 += 1
    if i.contains("60"):
        cs60 += 1
    if i.contains("81"):
        cs81 += 1
    if i.contains("101"):
        cs101 += 1
    if i.contains("105"):
        cs105 += 1
    if i.contains("131"):
        cs131 += 1

    


