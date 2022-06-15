from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    #Initialize game logic for A
    Or(AKnight, AKnave),
    Or(Not(AKnight), Not(AKnave)),

    #Logic representing A's statement
    Biconditional(AKnight, And(AKnight, AKnave)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    #Initialize game logic for A
    Or(AKnight, AKnave),
    Or(Not(AKnight), Not(AKnave)),
    #Initialize game logic for B
    Or(BKnight, BKnave),
    Or(Not(BKnight), Not(BKnave)),

    #Logic representing A's statement
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    #Initialize game logic for A
    Or(AKnight, AKnave),
    Or(Not(AKnight), Not(AKnave)),
    #Initialize game logic for B
    Or(BKnight, BKnave),
    Or(Not(BKnight), Not(BKnave)),

    #Logic representing A's statement
    Biconditional(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    #Logic representing B's statement
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    #Initialize game logic for A
    Or(AKnight, AKnave),
    Or(Not(AKnight), Not(AKnave)),
    #Initialize game logic for B
    Or(BKnight, BKnave),
    Or(Not(BKnight), Not(BKnave)),
    #Initialize game logic for C
    Or(CKnight, CKnave),
    Or(Not(CKnight), Not(CKnave)),

    #Logic representing A's statement
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    #Logic representing B's first statement
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    #Logic representing B's second statement
    Biconditional(BKnight, CKnave),
    #Logic representing C's statement
    Biconditional(CKnight, AKnight),
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
