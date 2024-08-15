from collections import deque
import copy

class SudokuSolver:
    """
    A class to represent a Sudoku solver with step-by-step visualization.

    Attributes:
    -----------
    board : list
        The 9x9 Sudoku board to be solved, represented as a 2D list.
    snapshots : deque
        A queue to store snapshots of the board during the solving process.
    is_solved : bool
        A flag to indicate if the Sudoku puzzle is solved.

    Methods:
    --------
    solve():
        Initiates the solving process.
    _solve():
        Recursively solves the Sudoku puzzle using backtracking.
    valid(num, pos):
        Checks if placing a number at a specific position is valid.
    find_empty():
        Finds an empty cell on the Sudoku board.
    get_snapshots():
        Returns a list of all snapshots taken during the solving process.
    """

    def __init__(self, board):
        """
        Constructs all the necessary attributes for the SudokuSolver object.

        Parameters:
        -----------
        board : list
            The 9x9 Sudoku board to be solved, represented as a 2D list.
        """
        self.board = board
        self.snapshots = deque()  # Queue to store board snapshots
        self.is_solved = False

    def solve(self):
        """
        Initiates the solving process for the Sudoku board.

        If the board is already solved, it returns immediately.
        Otherwise, it calls the private _solve() method to start solving.
        """
        if self.is_solved:
            return
        self._solve()  # Call a private solve method to avoid recursion limit issues

    def _solve(self):
        """
        Recursively solves the Sudoku puzzle using backtracking.

        Takes snapshots of the board at each step for visualization.
        Returns True if the puzzle is solved, otherwise backtracks.
        """
        find = self.find_empty()
        if not find:
            self.is_solved = True
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(i, (row, col)):
                self.board[row][col] = i
                # Store a snapshot after a valid number is placed
                self.snapshots.append((copy.deepcopy(self.board), (row, col), True))
                
                if self._solve():
                    return True
                
                # Reset the cell and store a snapshot after backtracking
                self.board[row][col] = 0
                self.snapshots.append((copy.deepcopy(self.board), (row, col), False))

        return False

    def valid(self, num, pos):
        """
        Checks if placing a number at a specific position is valid.

        Parameters:
        -----------
        num : int
            The number to place in the cell.
        pos : tuple
            The (row, col) position of the cell on the board.

        Returns:
        --------
        bool
            True if the placement is valid, False otherwise.
        """
        # Check the row
        for i in range(len(self.board[0])):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False
        
        # Check the column
        for i in range(len(self.board)):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False
            
        # Check the 3x3 box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def find_empty(self):
        """
        Finds an empty cell on the Sudoku board.

        Returns:
        --------
        tuple or None
            The (row, col) position of an empty cell, or None if no empty cell exists.
        """
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def get_snapshots(self):
        """
        Returns a list of all snapshots taken during the solving process.

        Returns:
        --------
        list
            A list of tuples containing the board snapshot, the position,
            and a boolean indicating if the placement was valid.
        """
        return list(self.snapshots)
