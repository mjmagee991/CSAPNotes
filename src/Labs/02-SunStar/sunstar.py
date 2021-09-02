"""
CSAP/X In-Lab Activity
02-Recursion
Sun Star

This program draws a line with a triangular outcropping with more triangular
outcroppings coming off the first in a recursive manner.
"""
import math
import turtle

ANGLE = 70
LENGTH = 100


def draw_side(n: float, level: int) -> float:
    """
    Draws one line with level recursive triangular outcroppings coming off it
    and a length n
    :param n: Length of the line to be drawn in the direction of the base
    :param level: Number of recursive triangular outcroppings to be drawn
    :return: Returns the total perimeter length of the line drawn
    """
    dist = 0
    # Base case
    if level == 1:
        # Draws a single straight line
        turtle.forward(n)
        dist = n
    # Recursive case
    else:
        # Draws the base to the left side of the triangular outcropping
        turtle.forward(n / 4)
        dist += n / 4
        # Draws the left side of the outcropping
        turtle.left(ANGLE)
        dist += draw_side((n / 4) / math.cos(ANGLE * math.pi / 180), level - 1)
        # Draws the right side of the outcropping
        turtle.right(ANGLE * 2)
        dist += draw_side((n / 4) / math.cos(ANGLE * math.pi / 180), level - 1)
        turtle.left(ANGLE)
        # Draws the base to the right side of the triangular outcropping
        turtle.forward(n / 4)
        dist += n / 4
    return dist


def main():
    """
    The main program prompts for the number of recursions that should be used to
    draw the figure then draws it and prints the total length.
    """
    turtle.speed(0)
    recNum = int(input('Number of recursions: '))
    print("Total length is", draw_side(LENGTH, recNum))
    turtle.mainloop()


if __name__ == '__main__':
    main()
