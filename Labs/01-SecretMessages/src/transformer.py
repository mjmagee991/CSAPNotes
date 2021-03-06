"""
CSAPX Lab 1: Secret Messages

A program that encodes/decodes a message by applying a set of transformation
    operations.
The transformation operations are:
    shift - Sa[,n] changes letter at index a by moving it n letters fwd in the
        alphabet
    rotate - R[n] rotates the string n positions to the right
    duplicate - Da[,n] follows character at index a with n copies of itself
    trade - T[(g)]a,b swaps the places of the a-th and b-th groups of g total
    flip - F[a] swaps the strings in front of and behind the ath character

All indices and group numbers are 0-based.

author: Matthew Magee
"""

# Constants
ALPHABET_LENGTH = 26
FIRST_LETTER_OF_ALPHABET = "A"


def transform(msg: str, opStr: str, decrypt: bool) -> str:
    """
    Takes a string message and a string of transformation operations and applies
        the transformation operations to the message string
    :param msg: String message
    :param opStr: String of transformation operations
    :param decrypt: Boolean that stores true for decryption and false for
        encryption
    :return: None
    """
    # Gets list of operations separated by ";"
    operations = opStr.split(";")
    # If function is decrypting, reverses the order of transformations
    if decrypt:
        operations.reverse()
    # Iterates through the operations, carrying out one at a time
    for operation in operations:
        # Separates operation type from parameters
        opType = operation[0]
        paramStr = operation[1:]
        parameters = []
        # Decides which operation to do based on the type
        # Operation Shift (S)
        if opType == "S":
            # Gets index and numShifts out of the operation string
            paramStrList = paramStr.split(",")
            for i in range(len(paramStrList)):
                parameters.append(int(paramStrList[i]))
            # If only 1 parameter is provided, numShifts is assumed to be 1
            if len(parameters) < 2:
                msg = shift(msg, parameters[0], 1, decrypt)
            # If both parameters are provided, both are used
            else:
                msg = shift(msg, parameters[0], parameters[1], decrypt)
        # Operation Rotate (R)
        elif opType == "R":
            # Gets numRot out of the operation string if given
            if len(paramStr) > 0:
                msg = rotate(msg, int(paramStr), decrypt)
            else:
                msg = rotate(msg, 1, decrypt)
        # Operation Duplicate (D)
        elif opType == "D":
            # Gets index and numDup out of the operation string
            paramStrList = paramStr.split(",")
            for i in range(len(paramStrList)):
                parameters.append(int(paramStrList[i]))
            # If only 1 parameter is provided, numDup is assumed to be 1
            if len(parameters) < 2:
                msg = duplicate(msg, parameters[0], 1, decrypt)
            # If both parameters are provided, both are used
            else:
                msg = duplicate(msg, parameters[0], parameters[1], decrypt)
        # Operation Trade (T)
        elif opType == "T":
            # Set default value for numGroups
            numGroups = len(msg)
            # If value of numGroups is given, replace the default value
            if paramStr.startswith("("):
                endParenthesisInd = paramStr.index(")")
                numGroups = int(paramStr[1:endParenthesisInd])
                paramStr = paramStr[endParenthesisInd + 1:]
            # Gets indices 1 and 2 out of the operation string
            paramStrList = paramStr.split(",")
            for i in range(len(paramStrList)):
                parameters.append(int(paramStrList[i]))
            msg = trade(msg, numGroups, parameters[0], parameters[1])
        elif opType == "F":
            # Gets axisIndex out of the operation string if given
            if len(paramStr) > 0:
                msg = flip(msg, int(paramStr))
            else:
                # If axisIndex isn't given, the axisIndex is the middle if the
                # message length is odd or one to the right of the middle if the
                # message length is even
                msg = flip(msg, len(msg) // 2)
    return msg


def shift(msg: str, index: int, numShifts: int, decrypt: bool) -> str:
    """
    Shifts the character of msg at position index alphabetically forward
        numShifts times
    :param msg: String message being transformed
    :param index: Position of character being shifted
    :param numShifts: Number of times character is being shifted
    :param decrypt: Boolean that stores true for decryption and false for
        encryption
    :return: String message after transformation is completed
    """
    # If decrypting, reverses the shift
    if decrypt:
        numShifts *= -1
    # Gets the ASCII value of the character and adds an integer representing the
    # shift
    newCharVal = ord(msg[index]) + numShifts
    # Rolls the ASCII value back to the beginning of the alphabet if it passes
    # the end or to the end of the alphabet if it passes the beginning
    newCharVal -= ord(FIRST_LETTER_OF_ALPHABET)
    newCharVal %= ALPHABET_LENGTH
    newCharVal += ord(FIRST_LETTER_OF_ALPHABET)
    # Returns the original string with the character at the index replaced by
    # the character with the calculated ASCII value
    return msg[:index] + chr(newCharVal) + msg[index + 1:]


def rotate(msg: str, numRot: int, decrypt: bool) -> str:
    """
    Takes numRot characters off the back of msg and rotates them to the front
    :param msg: String message being transformed
    :param numRot: Number of characters to be rotated
    :param decrypt: Boolean that stores true for decryption and false for
        encryption
    :return: String message after transformation is completed
    """
    # If decrypting, reverses the rotation
    if decrypt:
        numRot *= -1
    # Eliminate extra rotations if the number of rotations is more than the
    # length of the string
    numRot %= len(msg)
    # Takes numRot characters off the end of the string and moves them to the
    # front
    return msg[-numRot:] + msg[:-numRot]


def duplicate(msg: str, index: int, numDup: int, decrypt: bool) -> str:
    """
    Duplicates the character of msg at index numDup times
    :param msg: String message being transformed
    :param index: Index of character to be duplicated
    :param numDup: Number of times the character is duplicated
    :param decrypt: Boolean that stores true for decryption and false for
        encryption
    :return: String message after transformation is completed
    """
    # If decrypting, removes numDup characters instead of adding them
    if decrypt:
        return msg[:index] + msg[index + numDup:]
    return msg[:index] + msg[index] * numDup + msg[index:]


def trade(msg: str, numGroups: int, index1: int, index2: int) -> str:
    """
    Trades the groups of characters at the two given indices
    :param msg: String message being transformed
    :param numGroups: Number of equally sized groups of characters msg will be
        split into
    :param index1: Index of first group involved in trade
    :param index2: Index of second group involved in trade
    :return: String message after transformation is completed
    """
    # Breaks the string into a list with numGroups groups of characters
    groups = []
    groupSize = len(msg) // numGroups
    for i in range(numGroups):
        groups.append(msg[groupSize * i:groupSize * (i + 1)])
    # Switches the groups of characters at index1 and index2
    temp = groups[index1]
    groups[index1] = groups[index2]
    groups[index2] = temp
    # Joins the list of groups of characters into a string
    return "".join(groups)


def flip(msg: str, axisIndex: int):
    """
    Replaces the string of characters to the left of the axis with the string of
        characters to the right of the axis, flipping msg
    :param msg: String message being transformed
    :param axisIndex: Index of the axis of the flip
    :return: String message after transformation
    """
    return msg[axisIndex + 1:] + msg[axisIndex] + msg[:axisIndex]


def main() -> None:
    """
    The main program is responsible for getting the input details from user and
        writing the output file with the results of decrypting or decrypting the
        message file applying the transformations from the operation file.
    :return: None
    """
    msgFileName = input("Enter the message file name: ")
    opFileName = input("Enter the operation file name: ")
    outFileName = input("Enter output file name: ")
    decrypt = input("(E)ncrypt or (D)ecrypt?: ") == "D"

    print("Generating output ...")
    with open(msgFileName) as msgFile, open(opFileName) as opFile, open(
            outFileName, "w") as outFile:
        # Gets the first line of each file and strips whitespace
        msgLine = msgFile.readline().strip()
        opLine = opFile.readline().strip()
        # Loops through each line in the file
        while msgLine != "":
            # Applies transformation to the message
            outFile.write(transform(msgLine, opLine, decrypt) + "\n")
            # Gets a new line from each file
            msgLine = msgFile.readline().strip()
            opLine = opFile.readline().strip()
            print()


if __name__ == '__main__':
    main()
