class Board:
    """A data type representing a Connect-4 board with an arbitrary number of rows and columns."""
    
    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.data = [[' ']*width for row in range(height)]
    
    def __repr__(self):
        """This method returns a string representation for an object of type Board."""
        s = ''                          # The string to return
        for row in range(0, self.height):
            s += '|'
            for col in range(0, self.width):
                s += self.data[row][col] + '|'
            s += '\n'
        s += (2*self.width + 1) * '-' + "\n"   # Bottom of the board
        s += ' '.join(str(i % 10) for i in range(self.width)) + "\n"
        return s
    
    def addMove(self, col, ox):
        """Adds a move to the board in column col for player ox."""
        for row in range(self.height-1, -1, -1):
            if self.data[row][col] == ' ':
                self.data[row][col] = ox
                return
    
    def clear(self):
        """Clears the board."""
        self.data = [[' ']*self.width for row in range(self.height)]
    
    def setBoard(self, moveString):
        """Accepts a string of columns and places alternating checkers in those columns, starting with 'X'."""
        nextChecker = 'X'
        for colChar in moveString:
            col = int(colChar)
            if 0 <= col < self.width:
                self.addMove(col, nextChecker)
            nextChecker = 'O' if nextChecker == 'X' else 'X'
    
    def allowsMove(self, c):
        """Checks if a move is allowed in column c."""
        if 0 <= c < self.width and self.data[0][c] == ' ':
            return True
        return False
    
    def isFull(self):
        """Checks if the board is full."""
        for col in range(self.width):
            if self.allowsMove(col):
                return False
        return True
    
    def delMove(self, c):
        """Removes the top checker from the column c."""
        for row in range(self.height):
            if self.data[row][c] != ' ':
                self.data[row][c] = ' '
                return
    
    def winsFor(self, ox):
        """Checks if the player ox has won the game."""
        H = self.height
        W = self.width
        D = self.data
        
        def inarow_Neast(ch, r_start, c_start, A, N):
            """Check for N eastward."""
            if c_start + N > len(A[0]):
                return False
            for i in range(N):
                if A[r_start][c_start + i] != ch:
                    return False
            return True
        
        def inarow_Nsouth(ch, r_start, c_start, A, N):
            """Check for N southward."""
            if r_start + N > len(A):
                return False
            for i in range(N):
                if A[r_start + i][c_start] != ch:
                    return False
            return True
        
        def inarow_Nsoutheast(ch, r_start, c_start, A, N):
            """Check for N southeastward."""
            if r_start + N > len(A) or c_start + N > len(A[0]):
                return False
            for i in range(N):
                if A[r_start + i][c_start + i] != ch:
                    return False
            return True
        
        def inarow_Nsouthwest(ch, r_start, c_start, A, N):
            """Check for N southwestward."""
            if r_start + N > len(A) or c_start - N < -1:
                return False
            for i in range(N):
                if A[r_start + i][c_start - i] != ch:
                    return False
            return True
        
        for row in range(H):
            for col in range(W):
                if (inarow_Neast(ox, row, col, D, 4) or
                    inarow_Nsouth(ox, row, col, D, 4) or
                    inarow_Nsoutheast(ox, row, col, D, 4) or
                    inarow_Nsouthwest(ox, row, col, D, 4)):
                    return True
        return False
    
    def hostGame(self):
        """Hosts a full game of Connect Four."""
        print("Welcome to Connect Four!\n")
        while True:
            print(self)
            for player in ['X', 'O']:
                while True:
                    col = int(input(f"{player}'s choice: "))
                    if self.allowsMove(col):
                        break
                    else:
                        print("Invalid move. Try again.")
                self.addMove(col, player)
                if self.winsFor(player):
                    print(self)
                    print(f"{player} wins--Congratulations!")
                    return
                if self.isFull():
                    print(self)
                    print("It's a tie!")
                    return

# Below are some boards that will be re-created each time the file is run:
bigb = Board(15, 5)
b = Board(7, 6)

# This is the end of the Board class
# Below are some boards that will be re-created each time the file is run:

bigb = Board(15,5)
b = Board(7,6)

b = Board(7, 6)

b.setBoard('23344545515')


print(b)