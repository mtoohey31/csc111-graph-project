"""The Main python file that hosts the functionability of this program."""
from typing import Any


def intro() -> None:
    """ Prints an introduction of this program for the user.
    """
    ...


def run() -> Any:
    """ The function responsible for running the entire program.
    Puts out a menu for the user and allows access to the different parts of the program.
    """
    # Printing out the menu
    print("\nHere's your list of options:"
          "\n\n1 - Introduction to the Program"
          "\n2 - Category Visualizations"
          "\n3 - Category Recommendations"
          "\n4 - Exit"
          "\n\nEnter the number of your option of choice,")

    # Taking in user input
    op = choice()

    # Processing input to determine the corresponding function
    if op == 1:
        ...
    elif op == 2:
        ...
    elif op == 3:
        ...
    elif op == 4:
        print("Thank you for using this program! If at any time you\'d like to rerun, "
              "just type in run()."
              "\n~This program has ended.~")


def choice() -> int:
    """ Helper function that checks for valid user input.
    """
    # Set of allowable inputs
    val = {str(x) for x in range(1, 5)}

    # Ensuring the user enters valid input
    while True:
        choice = input("Choice:")

        if choice not in val:
            print("\nThat isn't an option, please try again,")
        else:
            return int(choice)


if __name__ == '__main__':

    print('\n~Comparing & Mapping Wikipedia Articles: A Simulation~')
    print('A program by: Gabe Guralnick, Matthew Toohey, Nathan Hansen & Azka Azmi')

    run()
