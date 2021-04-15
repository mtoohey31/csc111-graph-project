#!/usr/bin/env python3

"""The Main python file that hosts the functionability of this program."""
from typing import Any, Callable, Union

import wiki_graph
import visualize
import algorithms


graph = None


def intro() -> None:
    """ Prints an introduction of this program for the user.
    """
    ...


def main_menu() -> None:
    """ The function responsible for running the entire program.
    Puts out a menu for the user and allows access to the different parts of the program.
    """
    global graph

    if graph is None:
        choose({
            "Introduction to the Program": intro,
            "Select Category": cat_select,
            "Category Visualizations (Please select a category first)": None,
            "Category Recommendations (Please select a category first)": None,
            "Exit": exit})

    else:
        choose({
            "Introduction to the Program": intro,
            f"Select Category (Currently selected \"{graph.graph['category']}\")": cat_select,
            "Category Visualizations": cat_visualize,
            "Category Recommendations": cat_recommend,
            "Exit": exit})


def choose(choices: dict[str, Union[Callable, None, tuple[Callable, list],
                                    list[Union[Callable, tuple[Callable, Any]]]]]) -> None:
    """Helper function that asks for valid user input, then calls the corresponding function, unless that function is None.
    """
    print("\nSelect an Option:\n")
    index = 1
    for option in choices:
        if choices[option] is not None:
            print(f'{index} - {option}')
            index += 1
        else:
            print(f'X - {option}')

    valid = [str(i) for i in range(index)]

    # Ensuring the user enters valid input
    while True:
        choice = input("Choice: ").strip()

        if choice not in valid:
            print("That isn't an option, please try again.")
        else:
            break

    action = [value for value in choices.values(
    ) if value is not None][int(choice) - 1]

    if isinstance(action, list):
        for step in action:
            if isinstance(step, tuple):
                if isinstance(step[1], list):
                    step[0](*step[1])
                else:
                    step[0](step[1])
            else:
                step()
    elif isinstance(action, tuple):
        if isinstance(action[1], list):
            action[0](*action[1])
        else:
            action[0](action[1])
    else:
        action()


def cat_select() -> None:
    """Allow the user to select a category."""
    print("'\nPlease select a category.\n")

    choice = input("Cateogry Name: ")

    try:
        global graph
        graph = wiki_graph.create_digraph(choice)
    except:
        print("This category wasn't found on Wikipedia, please ensure that you are entering the title without the cateogry prefix, ex.: \"Logic programming languages\"")
        cat_select()

    main_menu()


def cat_visualize() -> None:
    """Allow the user to visualize the selected category."""
    global graph

    choose({"Visualize Graph": [(visualize.visualize_digraph, graph), cat_visualize],
            "Visualize PageRank Graph": [(algorithms.assign_pagerank, graph), (visualize.visualize_pagerank, graph), cat_visualize],
            "Visualize Link Histograms": [(visualize.visualize_histograms, graph)],
            "Main Menu": main_menu})


def cat_recommend() -> None:
    choose()


if __name__ == '__main__':
    print('\n~Comparing & Mapping Wikipedia Articles: A Simulation~')
    print('A program by: Gabe Guralnick, Matthew Toohey, Nathan Hansen & Azka Azmi')

    main_menu()
