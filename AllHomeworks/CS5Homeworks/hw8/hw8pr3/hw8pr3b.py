# hw8pr3b.py
# Name:
# Date: 

# imports
import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# starter code
def dart():
    """Throws one dart between (-1,-1) and (1,1).
    Returns True if it lands in the unit circle; otherwise, False.
    """
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    
    
    
    if x**2 + y**2 < 1:
        return True, x, y  # HIT (within the unit circle)
    else:
        return False, x, y  # miss (landed in one of the corners)
    
def animate_forpi(n):
    """Throws N darts, estimating pi with animation."""
    throws = 0
    hits = 0
    estimates = []
    hit_points = []
    miss_points = []
    errors = []

    """ creates three separate plots:
        1. Dart throws
        2. Estimation of Pi Over Time
        3. Error graph over time
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))

    # provides us with a frame by frame animation of our graphs as darts are being thrown
    def update(frame):
        nonlocal throws, hits

        # throws dart, checks for hit or miss, estimates pi, calcuates error
        hit, x, y = dart()
        throws += 1
        if hit:
            hits += 1
            hit_points.append((x, y))
        else:
            miss_points.append((x, y))
        pi_estimate = 4 * hits / throws
        estimates.append(pi_estimate)
        errors.append(abs(pi_estimate - math.pi) / math.pi)

        #clear the axis
        ax1.clear()
        ax2.clear()
        ax3.clear()

        # Plotting the dart throws
        ax1.set_title('Dart Throws')
        ax1.set_xlim(-1, 1)
        ax1.set_ylim(-1, 1)
        if hit_points:
            hit_x, hit_y = zip(*hit_points)
        else:
            hit_x, hit_y = [], []
        if miss_points:
            miss_x, miss_y = zip(*miss_points)
        else:
            miss_x, miss_y = [], []
        ax1.scatter(hit_x, hit_y, color='red', label='Hits')
        ax1.scatter(miss_x, miss_y, color='blue', label='Misses')
        ax1.legend()

        # Plotting the estimation of pi over time
        ax2.set_title('Estimation of Pi Over Time')
        ax2.set_xlim(0, n)
        ax2.set_ylim(2, 4)
        ax2.plot(range(1, throws+1), estimates)
        ax2.axhline(y=math.pi, color='r', linestyle='--', label='Actual Pi')
        ax2.legend()

        # To do!! Plotting absolute error over time: 
        ax3.set_title('Absolute Error Over Time')
        # set x limit
        # set y limit
        # plot ranges of throws and errors
        # plot the zero error line, see estimation of pi over time for refference
        # set legend

        # To do!! add a label that keeps track of the running pi value
    
    ani = FuncAnimation(fig, update, frames=range(n), interval = 20, repeat=False)
    plt.show()

# testing animate_forpi, should display the three graphs as darts are thrown
animate_forpi(1000)

# Now write the animate_whilepi(error) function here, following the logic of animate_forpi(n)
def animate_whilepi(error):
    """ remember your docstrings and comments for each section of code
        this will make your code organized and readable!
    """



    # uncomment these two lines of code when you are done, don't edit frames=range(100) to anything over 200
    # because it may crash your python kernel and you will have to force quit the application
    # ani = FuncAnimation(fig, update, frames=range(100), interval = 20, repeat=False)
    # plt.show()