"""
CSAP/X Lab
02-Recursion
Sun Star

This program draws a sun star. A sun star is a shape similar to a polygon but
such that each normal side of the polygon is a line with a triangular
outcropping with more triangular outcroppings coming off the first in a
recursive manner.

author: Matthew Magee
"""
import math
import re
import turtle


def draw_side(n: float, level: int, angle: int) -> float:
    """
    Draws one line with level recursive triangular outcroppings coming off it
    and a length n
    :param n: Length of the line to be drawn in the direction of the base
    :param level: Number of recursive triangular outcroppings to be drawn
    :param angle: Deflection angle of the triangular outcroppings
    :return: Total length of the line drawn
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
        turtle.left(angle)
        dist += draw_side((n / 4) / math.cos(angle * math.pi / 180), level - 1,
                          angle)
        # Draws the right side of the outcropping
        turtle.right(angle * 2)
        dist += draw_side((n / 4) / math.cos(angle * math.pi / 180), level - 1,
                          angle)
        turtle.left(angle)
        # Draws the base to the right side of the triangular outcropping
        turtle.forward(n / 4)
        dist += n / 4
    return dist


def draw_sides(n: float, level: int, angle: int, num_sides: int) -> float:
    """
    Draws a Sun Star with num_sides sides of length n, levels of complexity
    level, and deflection angle angle.
    :param n: Initial length of each side of the Sun Star
    :param level: Number of recursive triangular outcroppings in each side of
    the Sun Star
    :param angle: Angle of deflection of each side triangular outcropping
    :param num_sides:
    :return: Total perimeter of the Sun Star
    """
    perim = 0
    # Iterates through the input number of sides, drawing each, one at a time
    for _ in range(num_sides):
        perim += draw_side(n, level, angle)
        # Turns by 360 / num_sides to make the Sun Star a closed shape
        # Derived from formula for exterior angle of a polygon
        turtle.right(360 / num_sides)
    return perim


def main():
    """
    The main program prompts for the number of recursions that should be used to
    draw the figure then draws it and prints the total length.
    """
    turtle.speed(0)
    # Initializes each variable to -1, so it can be checked against a <0 loop
    numSides = -1
    sideLength = -1
    num_levels = -1
    deflAngle = -1

    # Gets numSides
    while numSides < 0:
        inpt = input('Number of sides: ')
        if re.fullmatch("[0-9]+", inpt):
            numSides = int(inpt)
        else:
            print("Value must be an integer. You entered", inpt)
    # Gets sideLength
    while sideLength < 0:
        inpt = input('Length of initial side: ')
        if re.fullmatch("[0-9]+.?[0-9]*|.[0-9]+", inpt):
            sideLength = float(inpt)
        else:
            print("Value must be a decimal. You entered", inpt)
    # Gets num_levels
    while num_levels < 0:
        inpt = input('Number of levels: ')
        if re.fullmatch("[0-9]+", inpt):
            num_levels = int(inpt)
        else:
            print("Value must be an integer. You entered", inpt)

    # If num_levels is 1, don't bother asking for an angle, just draw
    if num_levels == 1:
        print("Total length is",
              draw_sides(sideLength, num_levels, 0, numSides))
    else:
        # Gets deflAngle
        while deflAngle < 0:
            inpt = input('Deflection angle: ')
            if re.fullmatch("[0-9]+.?[0-9]*|.[0-9]+", inpt):
                deflAngle = float(inpt)
            else:
                print("Value must be a decimal. You entered", inpt)
        print("Total length is",
              draw_sides(sideLength, num_levels, deflAngle, numSides))

    turtle.mainloop()


if __name__ == '__main__':
    main()
