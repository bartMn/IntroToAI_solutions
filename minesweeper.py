import itertools
import random
import copy

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if not self:
            return None
        if len(self.cells)== self.count:
            return self.cells
        else:
            return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if not self:
            return None
        if self.count==0:
            return self.cells
        else:
            return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count-=1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
                self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()
        self.unexplored= set()
        for i in range(self.height):
            for j in range(self.width):
                self.unexplored.add((i, j))

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            
   
        
    def new_knowledge(self):
        new_info=[]
        for sen1 in self.knowledge:
            for sen2 in self.knowledge:
                trigger=0
                if sen1==sen2:
                    continue
                if (sen1.cells & sen2.cells)== sen1.cells:
                    ns_cells= sen2.cells - sen1.cells
                    ns_count= sen2.count - sen1.count
                    trigger=1
                elif (sen1.cells & sen2.cells)== sen2.cells:
                    ns_cells= sen1.cells - sen2.cells
                    ns_count= sen1.count - sen2.count
                    trigger=1
                if trigger==1:
                    new_sen= Sentence(ns_cells, ns_count)
                    if new_sen not in new_info:
                        if new_sen not in self.knowledge:
                            new_info.append(new_sen)
             
        return new_info
        

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made       \done
            2) mark the cell as safe                            \done
            3) add a new sentence to the AI's knowledge base    \done
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        self.moves_made.add(cell)
        self.mark_safe(cell)
        neigbours= set()
        
        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                if (i, j)== cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) in self.mines:
                        count-= 1
                    elif (i, j) not in self.safes:
                        neigbours.add((i, j))
                        
    
        if len(neigbours) != 0:
            new_sen= Sentence(neigbours, count)
            self.knowledge.append(new_sen)
            #finding new safes, new mines and updating
        while True:
            temp= set()
            control= 0
            for sen in self.knowledge:
                if sen.known_mines() is not None:
                    temp= copy.copy(sen.known_mines())
                    control= 1
                    break
                            
                elif sen.known_safes() is not None:
                    temp= copy.copy(sen.known_safes())
                    control= 2
                    break
   
            if control != 0:
                for sen in self.knowledge:
                    if sen.cells== temp:
                        self.knowledge.remove(sen)
                if control== 1:
                    for m in temp:
                        self.mark_mine(m)
                    continue
                elif control == 2:
                    for s in temp:
                        self.mark_safe(s)
                    continue
            
            new_k= self.new_knowledge()
            if not new_k:
                return
            else:
                for ns in new_k:
                    self.knowledge.append(ns)
  
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        available_moves= self.safes-self.moves_made
        if len(available_moves) != 0:
            safe_move= random.choice(tuple(available_moves))
            return safe_move
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        self.unexplored= self.unexplored- (self.mines | self.moves_made)
        if len(self.unexplored) != 0:
            guess= random.choice(tuple(self.unexplored))
            self.moves_made.add(guess)
            return guess
        else:
            return None
        
        