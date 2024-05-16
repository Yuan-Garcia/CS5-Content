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
    
    
