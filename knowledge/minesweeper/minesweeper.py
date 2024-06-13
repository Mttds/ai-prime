import itertools
import random


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
        self.cells = set(cells) # for example {(0,0), (0,1)}
        self.count = count # for example 2, with the above cells would mean both of them are mines

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # Our AI would construct the sentence {E, F, H} = 3. Intuitively, we can infer that all of E, F, and H are mines.
        # More generally, any time the number of cells is equal to the count, we know that all of that sentence’s cells must be mines.
        mines = set()
        if len(self.cells) == self.count:
            mines = self.cells
        
        return mines


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # Using the knowledge from the lower-left number, we could construct the sentence {D, E, G} = 0
        # to mean that out of cells D, E, and G, exactly 0 of them are mines.
        # Intuitively, we can infer from that sentence that all of the cells must be safe.
        # By extension, any time we have a sentence whose count is 0, we know that all of that sentence’s cells must be safe.
        safes = set()
        if self.count == 0:
            safes = self.cells

        return safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # if the cell is in the set of cells representing this sentence
        # then we remove it from the set and we reduce the count
        # for example, {(0,1),(1,1),(1,0)} = 2 and we now know that (1,1) is a mine
        # we remove it from the set resulting in {(0,1), (1,0)} = 1 so before there were 2 mines
        # out of the 3 and now since we removed a mine we know either (0,1) or (1,0) must be the other mine

        # Likewise, if our AI knew the sentence {A, B, C} = 2, and we were told that C is a mine, we could remove C
        # from the sentence and decrease the value of count (since C was a mine that contributed to that count),
        # giving us the sentence {A, B} = 1. This is logical: if two out of A, B, and C are mines,
        # and we know that C is a mine, then it must be the case that out of A and B, exactly one of them is a mine.
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # For example, if our AI knew the sentence {A, B, C} = 2, we don’t yet have enough information to conclude anything.
        # But if we were told that C were safe, we could remove C
        # from the sentence altogether, leaving us with the sentence {A, B} = 2 (which, incidentally, does let us draw some new conclusions.)
        # same logic as mark_mine, but since we are removing a safe we don't decrease the mines counter
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

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        Algo:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1
        self.moves_made.add(cell)

        # 2
        self.mark_safe(cell)

        # 3
        # Loop over all cells within one row and column
        neighbors = []
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) in self.mines:
                        count -= 1
                    elif (i, j) not in self.safes:
                        neighbors.append((i, j))

        s = Sentence(neighbors, count)
        if s not in self.knowledge:
            self.knowledge.append(s) 

        # 4
        for s in self.knowledge:
            safes = s.known_safes()
            mines = s.known_mines()
            if mines:
                self.mines = self.mines.union(mines)
            if safes:
                self.safes = self.safes.union(safes)

        # 5
        for i in range(len(self.knowledge)):
            for j in range(i + 1, len(self.knowledge)):
                sentence_row = self.knowledge[i]
                sentence_column = self.knowledge[j]

                if sentence_row.cells.issubset(sentence_column.cells):
                    new = Sentence(sentence_column.cells - sentence_row.cells, sentence_column.count - sentence_row.count)
                    if new not in self.knowledge:
                        self.knowledge.append(new)
                elif sentence_column.cells.issubset(sentence_row.cells):
                    new = Sentence(sentence_row.cells - sentence_column.cells, sentence_row.count - sentence_column.count)
                    if new not in self.knowledge:
                        self.knowledge.append(new)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = []
        for row in range(self.height):
            for column in range(self.width):
                if (row, column) not in self.moves_made:
                    if (row, column) not in self.mines:
                        possible_moves.append((row, column))

        random.shuffle(possible_moves)
        if len(possible_moves) > 0:
            return possible_moves[0]
