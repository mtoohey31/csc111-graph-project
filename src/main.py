#!/usr/bin/env python3
"""The Main python file that hosts the functionability of this program."""
from typing import Any, Callable, Union
import wiki_graph
import visualize
import algorithms
import recommendations


graph = None


def main_menu() -> None:
    """The main menu of the program. Prints a menu for the user and allows access to the different
    parts of the program.
    """
    # Get the global graph variable
    global graph

    # Check if a graph has been chosen
    if graph is None:
        choose({
            "Select Category": cat_select,
            "Category Visualizations (Please select a category first)": None,
            "Category Recommendations (Please select a category first)": None,
            "Exit": exit})

    else:
        choose({
            f"Select Category (Currently selected \"{graph.graph['category']}\")": cat_select,
            "Category Visualizations": cat_visualize,
            "Category Recommendations": cat_recommend,
            "Exit": exit})


def choose(choices: dict[str, Union[Callable, None, tuple[Callable, Any],
                                    list[Union[Callable, tuple[Callable, Any]]]]]) -> None:
    """Helper function that asks for valid user input, then calls the corresponding function,
    unless that function is None.
    """
    # Print the first header
    print("\nSelect an Option:\n")

    # Print out the options
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

    # Parse the different combinations of data structures, calling the appropriate functions with
    # the provided arguments
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
    # Prompt the user for input and collect that input
    print("'\nPlease select a category.\n")
    choice = input("Cateogry Name: ")

    # Ensure the graph is created without issue before returning to the main menu.
    try:
        # Get the global graph variable
        global graph
        graph = wiki_graph.create_digraph(choice)
    except ValueError:
        print(
            "This category wasn't found on Wikipedia, please"
            " ensure that you are entering the title without "
            "the cateogry prefix, ex.: \"Logic programming languages\"")
        cat_select()

    # Return to the main menu
    main_menu()


def cat_visualize() -> None:
    """Allow the user to visualize the selected category."""
    # Get the global graph variable
    global graph

    # Prompt the user to choose a visualization or return to the main menu
    choose({"Visualize Graph": [(visualize.visualize_digraph, graph), cat_visualize],
            "Visualize PageRank Graph": [(algorithms.assign_pagerank, graph),
                                         (visualize.visualize_pagerank, graph), cat_visualize],
            "Visualize Link Histograms": (visualize.visualize_histograms, graph),
            "Main Menu": main_menu})


def cat_recommend() -> None:
    """ Allows the user to access the recommendation systems and visualizations.
    """
    # Assigning our variables, these variables get reassigned each time the function is called
    global graph
    n = list_input()
    page = list_input(True)

    # Our dictionary to list mapping our functions to their function calls
    choose({"List of Top Ranked Wikipedia Pages (Basic)":
            [(recommendations.print_lst, [1, graph, n]),
             cat_recommend],
            "List of Top Ranked Wikipedia Pages (Pagerank Importance)":
                [(recommendations.print_lst, [2, graph, n]),
                 cat_recommend],
            "List of Top Page Recommendations for " + page + ", based on Similarity Scores":
                [(recommendations.print_lst, [3, graph, n, page]), cat_recommend],
            "Comparison Visual of Top Ranked Pages":
                [(recommendations.visualize_rankings, [graph, n]), cat_recommend],
            f"Chart Visual of Top  Page Recommendations for {page}, based on Similarity Scores":
                [(recommendations.visualize_recommendation,
                  [page, n, graph]), cat_recommend],
            "Main Menu": main_menu})


def list_input(page: bool = False) -> Union[int, str]:
    """ Asks the user for an int input, and returns that integer.
    """
    global graph

    # Checks for whether the return value is a string
    if page:
        # Asks the user to choose a valid node within our graph
        print('\nHere is a list of all the pages within your category:')
        print(graph.nodes)
        n = input('\nEnter a page from this list you\'d like recommendations for'
                  ' (Spelling counts!):')

        # Loops until user chooses a node that exists in the Graph
        while True:
            if n in graph.nodes:
                break
            else:
                print(
                    '\nThat page is not in this category, choose one from this list and try again:')
                print(graph.nodes)

            n = input('\nPage: ')

    # Else return value is an integer
    else:
        # Loop until user gives valid input
        while True:
            n = input('\nAt MOST, how many recommendations did you want to see?')

            if str.isnumeric(n) and int(n) > 0:
                n = int(n)
                break
            else:
                print("\nThat isn't valid input please try again!")

    # Returns valid user input
    return n


if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'extra-imports': ['wiki_graph', 'visualize', 'algorithms', 'recommendations'],
    #     'max-nested-blocks': 4
    # })

    # Print the initial welcome message
    print('\n~Comparing & Mapping Wikipedia Articles: A Simulation~')
    print('A program by: Gabe Guralnick, Matthew Toohey, Nathan Hansen & Azka Azmi')

    # Start the main menu
    main_menu()
