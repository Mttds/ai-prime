from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
puzzle = And(AKnight, AKnave)
knowledge0 = And(
    Or(AKnave, AKnight), # each charater is a Knave or a Knight
    Biconditional(AKnave, Not(AKnight)), # If a char is a Knave it is not a Knight and viceversa
    Implication(AKnight, puzzle), # if a knight says something then it is true
    Implication(AKnave, Not(puzzle)) # opposite goes for a Knave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
puzzle = And(AKnave, BKnave)
knowledge1 = And(
    Or(AKnave, AKnight), # each charater is a Knave or a Knight
    Or(BKnave, BKnight),

    Biconditional(AKnave, Not(AKnight)), # If a char is a Knave it is not a Knight and viceversa
    Biconditional(BKnave, Not(BKnight)),

    Implication(AKnight, puzzle), # if a knight says something then it is true
    Implication(AKnave, Not(puzzle)) # opposite goes for a Knave
    # B says nothing so nothing is inferred
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
puzzle_A = Or(And(AKnave, BKnave), And(AKnight, BKnight))
puzzle_B = Or(And(AKnave, BKnight), And(BKnave, AKnight))
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Implication(AKnight, puzzle_A),
    Implication(AKnave, Not(puzzle_A)),
    Implication(BKnight, puzzle_B),
    Implication(BKnave, Not(puzzle_B)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
puzzle_A = Or(AKnight, AKnave)
puzzle_B = CKnave
puzzle_C = AKnight
knowledge3 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),

    # A
    And(
        Implication(AKnight, puzzle_A), 
        Implication(AKnave, Not(puzzle_A)),
    ),

    # B
    Implication(BKnight, Implication(AKnave, AKnight)),

    Implication(BKnight, puzzle_B),
    Implication(BKnave, Not(puzzle_B)),

    # C
    Implication(CKnight, puzzle_C),
    Implication(CKnave, Not(puzzle_C)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
