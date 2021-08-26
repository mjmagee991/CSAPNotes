"""
CSAPX Lab 1: Secret Messages

A program that encodes/decodes a message by applying a set of transformation operations.
The transformation operations are:
    shift - Sa[,n] changes letter at index a by moving it n letters fwd in the alphabet
    rotate - R[n] rotates the string n positions to the right
    duplicate - Da[,n] follows character at index a with n copies of itself
    trade - T[(g)]a,b swaps the places of the a-th and b-th groups of g total

All indices and group numbers are 0-based.

author: Matthew Magee
"""


def transform(msgStr: str, opStr: str) -> None:
    """
    Takes a string message and a string of transformation operations and applies
    the transformation operations to the message string
    :param msgStr: String message
    :param opStr: String of transformation operations
    :return: None
    """
    # Loops through each operation separated by ";"
    for operation in opStr.split(";"):
        # Separates operation type from parameters
        opType = operation[0]
        parameters = operation[1:]
        # Decides which operation to do based on the type
        if opType == "S":
            print("Operation Shift (S) - Parameters: " + parameters)
        elif opType == "R":
            print("Operation Rotate (R) - Parameters: " + parameters)
        elif opType == "D":
            print("Operation Duplicate (D) - Parameters: " + parameters)
        else:
            print("Operation Trade (T) - Parameters: " + parameters)


def main() -> None:
    """
    The main program is responsible for getting the input details from user and
    writing the output file with the results of encrypting or decrypting the
    message file applying the transformations from the operation file.
    :return: None
    """
    msgFileName = input("Enter the message file name: ")
    opFileName = input("Enter the operation file name: ")

    print("Generating output ...")
    with open(msgFileName) as msgFile, open(opFileName) as opFile:
        # Gets the first line of each file and strips whitespace
        msgLine = msgFile.readline().strip()
        opLine = opFile.readline().strip()
        # Loops through each line in the file
        while msgLine != "":
            # Applies transformation to the message
            print("Transforming message: " + msgLine)
            print("Applying...")
            transform(msgLine, opLine)
            # Gets a new line from each file
            msgLine = msgFile.readline().strip()
            opLine = opFile.readline().strip()
            print()


if __name__ == '__main__':
    main()
