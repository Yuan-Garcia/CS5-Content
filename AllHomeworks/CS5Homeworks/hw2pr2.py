import random
import time

# the following uncommented code is entirely AI generated to "test" the homework assignment
def rs():
    """rs chooses a random step and returns it.
       Note that a call to rs() requires parentheses.
       Arguments: none at all!
    """
    return random.choice([-1, 1])

def rwpos(start, nsteps):
    """ rwpos models a random walker that
        * starts at the int argument, start
        * takes the int # of steps, nsteps

        rwpos returns the final position of the walker.
    """
    time.sleep(0.1)
    print('location is', start)
    if nsteps == 0:
        return start
    else:
        new_position = start + rs()
        return rwpos(new_position, nsteps - 1)

def rwsteps(start, low, hi):
    """rwsteps models a random walker which
       * is currently at start 
       * is in a walkway from low (usually 0) to hi (max location)
       rwsteps returns the # of steps taken 
       when the walker reaches an edge
    """
    # Print the initial walkway with the walker's position
    walkway = ['_'] * (hi - low + 1)
    walker_position = start - low
    walkway[walker_position] = 'S'
    print(''.join(walkway))
    time.sleep(0.05)

    # Base case: if the walker reaches or goes beyond the boundaries
    if start <= low or start >= hi:
        return 0
    else:
        # Recursive case: move the walker and print the new position
        new_position = start + rs()
        steps_taken = 1 + rwsteps(new_position, low, hi)

        # Update the walkway with the new position
        walkway = ['_'] * (hi - low + 1)
        walker_position = new_position - low
        if walker_position >= 0 and walker_position < len(walkway):
            walkway[walker_position] = 'S'
        print(''.join(walkway))
        time.sleep(0.05)

        return steps_taken
print("Final steps taken:", rwsteps(5, 0, 10))
'''
#hw2pr2 2D extra-credit
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
    time.sleep(0.05) 
    if startX <= lowX or startX >= hiX:            # base case: no steps if we're at an endpt
        return 0
    elif startY <= lowY or startY >= hiY: 
        return 0
    else:
        newstart = rwpos(startX, startY, 1)                # takes one step, from start to newstart
        return 1 + rwsteps(newstart, lowX, lowY, hiX, hiY)  # counts one step, recurses for the rest!

    walkway = " " + walkway + " "              # surround with spaces, for now...

    print(walkway, "    ", start, low, hi)     # print everything to keep track...
   

print(rwsteps(0,0,-5,-5,5,5))'''