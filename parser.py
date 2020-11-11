import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adj -> "big" | "blue" | "small" | "dry" | "wide"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"| "it"
N -> "smile" | "thursday" | "walk" | "we" | "word"
N -> "she" | "city" | "car" | "street" | "dog" | "binoculars"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
V -> "saw" | "walked"| "died"
P -> "at" | "before" | "in" | "of" | "on" | "to"
P -> "on" | "over" | "before" | "below" | "with"
"""

NONTERMINALS = """
S -> NP VP| S Conj S| S Conj VP
NP -> N| Det NP| AP NP
VP -> V| V NP| V PP| Adv VP| VP Adv| VP PP
AP -> Adj| Adj AP
PP -> P NP| NP PP| NP Adv
"""
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)
    print(list(parser.parse(s)))
    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tokens = nltk.word_tokenize(sentence)
    new_sen= []
    for item in tokens:
        item= item.lower()
        if item.islower():
            new_sen.append(item)
    return new_sen


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    result= []
    for subtree in tree.subtrees():
        if subtree.label() == "NP":  
            x=0
            for branch in subtree.subtrees():
                if len(subtree)== 1:
                    x=1
                    break
                if branch.label() == "N":
                    x-=1
                elif branch.label() == "NP":
                    x+=1
            if x== 1:
                is_in = False
                for i in result:
                    if subtree in i:
                        is_in = True
                if is_in == False:
                    result.append(subtree)
    return result

if __name__ == "__main__":
    main()
