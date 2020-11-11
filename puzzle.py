from logic import Symbol, And, Not, Or, Implication, model_check

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

Nothing= Symbol("")

ppl= [[AKnight, AKnave], [BKnight, BKnave], [CKnight, CKnave]]
Rules= And()

for person in ppl:
    for x in range(2):
        Rules.add(
            Implication(person[x], Not(person[x-1]))
            )

for person in ppl:
    Rules.add(Or(person[x], person[x-1]))
    
    
def give_info(sentences):
    quotes= sentences
    info=And()
    for x in range(len(quotes)):
        info.add(Or(
            And(quotes[x], ppl[x][0]),
            And(Not(quotes[x]), ppl[x][1])
            ))
    info.add(Rules)
    return info
    
# Puzzle 0
# A says "I am both a knight and a knave."
quotes0= [And(AKnight, AKnave)]
knowledge0= give_info(quotes0)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
quotes1= [And(AKnave, BKnave), Nothing]
knowledge1 = give_info(quotes1)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
quotes2=   [Or(And(AKnight, BKnight), And(AKnave, BKnave)),
           Or(And(AKnight, BKnave), And(AKnave, BKnight))]

knowledge2= give_info(quotes2)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
quotes3= [Or(AKnight, AKnave),
         And(AKnave, CKnave), 
         AKnight]

knowledge3= give_info(quotes3)



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