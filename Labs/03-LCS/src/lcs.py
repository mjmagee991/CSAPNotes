"""
CSAP/X In-Lab
03-Searching and Sorting
Least Common Subsumers

This program uses a linear method to find the least common subsumers among
concepts in an ontology.

author: Matthew Magee
"""
from ontology import Ontology, Concept
from dataclasses import dataclass


@dataclass
class ConceptPair:
    concept1: Concept
    concept2: Concept
    similarity: float


def main() -> None:
    """
    Uses an ontology generated from a local file. Then, prints the lowest common
    subsumer of to pairs of concepts to show effectiveness of linear method.
    :return: None
    """
    o = Ontology("../data/simple.kb")
    dog = o.getConcept("dog")
    reptile = o.getConcept("reptile")
    cat = o.getConcept("cat")
    mammal = o.getConcept("mammal")
    print(linearLCS(dog, reptile))
    print(linearLCS(cat, mammal))


def linearLCS(concept1: Concept, concept2: Concept) -> Concept:
    """
    Uses a linear approach to find the lowest common subsumer (LCS) of concept1
    and concept2
    :param concept1: First concept for finding LCS
    :param concept2: Second concept for finding LCS
    :return: LCS of concept1 and concept2
    """
    # Get paths to both concepts and identify the shorter of the two
    # If lengths are equal, order doesn't matter
    path1 = concept1.getPathToTop()
    path2 = concept2.getPathToTop()
    if len(path1) < len(path2):
        shorterPath = path1
        longerPath = path2
    else:
        shorterPath = path2
        longerPath = path1
    # Iterate backwards through the paths, stopping when reaching the beginning
    # of the shorter path
    for i in range(-1, -1 * len(shorterPath) - 1, -1):
        # If the concept at position i is different in the paths for each
        # concept, the LCS is one layer above i
        if shorterPath[i] != longerPath[i]:
            return shorterPath[len(shorterPath) + i + 1]
    # If it reaches the beginning without finding a difference, the LCS is the
    # concept with the shorter path
    return shorterPath[0]


if __name__ == "__main__":
    main()
