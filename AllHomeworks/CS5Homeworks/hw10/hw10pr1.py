#
# hw10pr1.py 
#
# Name:
#

# First, the class definition
#
# ++ ALSO ++  below, we define several useful objects of type Date
#  +++ keep those and/or add your own! +++


class Date:
    """A user-defined data structure that
       stores and manipulates dates.
    """

    # The constructor is always named __init__ !
    def __init__(self, month, day, year):
        """Construct a Date with the given month, day, and year."""
        self.month = month
        self.day = day
        self.year = year


    # The "printing" function is always named __repr__ !
    def __repr__(self):
        """This method returns a string representation for the
           object of type Date that calls it (named self).

           ** Note that this function _can_ be called explicitly, but
              it more often is used implicitly via the print statement
              or simply by expressing self's value.
        """
        d = self.day
        m = self.month
        y = self.year
        string = f"{m:02d}/{d:02d}/{y:04d}"
        # The "d" after the integer stands for "_d_ecimal integer..."
        return string

        #
        # Note that we could have also written:
        #
        # return f"{self.month:02d}/{self.day:02d}/{self.year:04d}"


    # Here is an example of a "method" of the Date class:
    def isLeapYear(self):
        """Returns True if the calling object is
           in a leap year; False otherwise."""
        if self.year % 400 == 0:
            return True
        elif self.year % 100 == 0:
            return False
        elif self.year % 4 == 0:
            return True
        return False




#
# Be sure to add code for the Date class ABOVE--indented inside the class
# definition
#

#
# Lots of dates to work with...
#
# The nice thing about putting them here is that they get redefined with
#   each run of the software (needed for testing!)
#

d = Date(6, 18, 2024)     # Today? Yesterday?
d2 = Date(5, 11, 2024)    # Start of summer break
ny = Date(1, 1, 2025)     # New year
nd = Date(1, 1, 2030)     # New decade
nc = Date(1, 1, 2100)     # New century
graduation = Date(5, 14, 2028)    # Alter to suit!
nextsemester = Date(9, 3, 2024)  # Start of classes next semester
wd = Date(11, 12, 2013)   # A popular wedding day
wd2 = Date(11, 12, 2013)  # A copy of wd, to check == and .equals()
wd10 = Date(10, 10, 2010)  # 10/10/10
sm1 = Date(10, 28, 1929)  # One stock market crash
sm2 = Date(10, 19, 1987)  # Another crash: October Mondays are risky!