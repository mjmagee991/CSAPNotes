"""
CSAP/X Lab
03-Searching and Sorting
Least Common Subsumers

This program opens a knowledge base file in a folder called "data" on the same
level as the "src" folder. It gets the file name from the command line input.
This knowledge base file should hold information about an ontology of concepts.
This program then puts the information about this ontology into an Ontology
instance and gives the similarity score for every pair of concepts in the
ontology, printing them out from least score to greatest.

author: Matthew Magee
"""
import sys

from ontology import Ontology, Concept
from dataclasses import dataclass


@dataclass
class ConceptPair:
    """
    Class that holds two concepts and their concept score to make sorting easier
    """
    c1: Concept
    c2: Concept
    simScore: float


def main() -> None:
    """
    Uses an ontology generated from a local file. Then, calculates the
    similarity score for every pair of concepts in the ontology and prints them
    from least to greatest
    :return: None
    """
    # Gets the ontology from the file
    o = Ontology("../data/" + sys.argv[1])

    # Sets up lists of concepts for iteration
    concepts = o.getAllConcepts()
    conceptPairs = []

    # Iterates through every pair of concepts, creating ConceptPair instances
    for i in range(len(concepts)):
        for j in range(i, len(concepts)):
            c1 = concepts[i]
            c2 = concepts[j]
            conceptPairs.append(ConceptPair(c1, c2, sim(c1, c2, o)))

    # Sorts concept pairs by their similarity score
    conceptPairs.sort(key=lambda cp: [cp.simScore])

    # Prints out every concept pair with its similarity score
    for cp in conceptPairs:
        print("sim(" + str(cp.c1) + ", " + str(cp.c2) + " ) = " + str(
            round(cp.simScore, 3)))


def linearLCS(c1: Concept, c2: Concept) -> Concept:
    """
    Uses a linear approach to find the lowest common subsumer (LCS) of c1 and c2
    :param c1: First concept for finding LCS
    :param c2: Second concept for finding LCS
    :return: LCS of concept1 and concept2
    """
    # Get paths to both concepts and identify the shorter of the two
    # If lengths are equal, order doesn't matter
    path1 = c1.getPathToTop()
    path2 = c2.getPathToTop()
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


def binaryLCS(c1: Concept, c2: Concept, o: Ontology) -> Concept:
    """
    Uses a binary approach to find the lowest common subsumer (LCS) of c1 and c2
    :param c1: First concept for finding LCS
    :param c2: Second concept for finding LCS
    :param o: Ontology containing c1 and c2
    :return: LCS of concept1 and concept2
    """
    searchPath = c1.getPathToTop()
    # Starting index of the current step in the search
    start = 0
    # Ending index of the current step in the search
    end = len(searchPath)

    # While the searching section of the list is more than 1 element
    while start != end:
        # Get the middle value
        midIndex = (start + end) // 2
        midValue = searchPath[midIndex]
        # If the middle value subsumes c2, the answer is midValue or left of it
        if o.subsumes(midValue, c2):
            # Eliminate values to the right of midValue
            end = midIndex
        # If not, the answer is right of midValue
        else:
            # Eliminate midValue and values to its left
            start = midIndex + 1

    # Return the remaining value
    return searchPath[start]


def sim(c1: Concept, c2: Concept, o: Ontology) -> float:
    """
    Calculates the similarity score of c1 and c2 in ontology o
    :param c1: First concept being compared
    :param c2: Second concept being compared
    :param o: Ontology containing c1 and c2
    :return: Similarity score of c1 and c2
    """
    # Gets Lowest Common Subsumer
    lcs = binaryLCS(c1, c2, o)
    # Calculates similarity score
    s1 = len(c1.getPathToTop())
    s2 = len(c2.getPathToTop())
    s3 = len(lcs.getPathToTop())
    return s3 / (s1 + s2 - s3)


if __name__ == "__main__":
    main()
