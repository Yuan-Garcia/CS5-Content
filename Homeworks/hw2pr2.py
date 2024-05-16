import time
import random  

def rs():
    """rs chooses a random step and returns it. 
       Note that a call to rs() requires parentheses.
       Arguments: none at all!
    """
    return random.choice([-2,-1,1,2])

def rwpos(startX, startY, nsteps):
    """ rwpos models a random walker that
        * starts at the coordinate, (startX, startY)
        * takes the int # of steps, nsteps

        rwpos returns the final position of the walker.
    """
    time.sleep(0.1)
    print('location is', startX, startY)
    if nsteps == 0:
        return startX, startY
    else:
        randDirection = rs()
        if randDirection % 2 == 0:
             newposX = startX + randDirection/2
        else: 
             newposY = startY + randDirection  # take one step

        return rwpos(newposX, newposY, nsteps - 1)
    
def rwsteps(startX, startY, lowX, lowY, hiX, hiY):
    """ rwsteps models a random walker which
        * is currently at start 
        * is in a walkway from low (usually 0) to hi (max location) 
          
        rwsteps returns the # of steps taken 
        when the walker reaches an edge
    """
    walkway = ("_"*(hiX-lowX)+"\n")*(hiY-lowY)    # create a walkway of underscores
    posX = (startX-lowX) 
    posY = (startY-lowY)          # this is our sleepwalker's location, start-low
    S = posX*posY
    
    walkway = walkway[:S] + "S" + walkway[S+1:]  # put our sleepwalker, "S", there
    print(walkway)
'''
    walkway = " " + walkway + " "              # surround with spaces, for now...

    print(walkway, "    ", start, low, hi)     # print everything to keep track...
    time.sleep(0.05)                               # ignore this

    if start <= low or start >= hi:            # base case: no steps if we're at an endpt
        return 0
    
    else:
        newstart = start + rs()                # takes one step, from start to newstart
        return 1 + rwsteps(newstart, low, hi)  # counts one step, recurses for the rest!
'''
print(rwsteps(0,0,-5,-5,5,5))
