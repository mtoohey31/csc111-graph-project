""" Recommendation and Similarity Algorithms used to analyze and return the similarities between
pages within certain Wikipedia Categories"""
import networkx as nx
from typing import Any
import wiki_graph
import algorithms
import wikipediaapi as w

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def wiki_link_pages(lst: list) -> list:
    """ Takes a list of page names and similarity scores and returns a tuple with page names
    and page urls.
    """
    wiki = w.Wikipedia('en')
    urls_so_far = []

    # Retrieving the URL for each page and appending it to a list tuple.
    if type(lst[0]) is tuple:
        for elem in lst:
            page_py = wiki.page(elem[1])
            urls_so_far.append((elem[1], page_py.fullurl))
    else:
        for elem in lst:
            page_py = wiki.page(elem)
            urls_so_far.append((elem, page_py.fullurl))

    return urls_so_far


def top_wiki_pages(g: nx.Graph, n: int) -> list:
    """ Returns a list of size n wiki pages within this category that hold the most connections
    to other pages, and the number of their connections, sorted in descending order. If there is
    less than n pages within this category, the list will return that amount instead. This is a
    more basic and straightforward ranking approach compared to top_wiki_pagerank_pages().

    >>> import wiki_graph
    >>> test_graph = wiki_graph.create_digraph('Prolog programming language family')
    >>> top_wiki_pages(test_graph, 3)
    [(15, 'Prolog'), (7, 'Logtalk'), (6, 'Comparison of Prolog implementations')]
    """
    page_links_so_far = []

    # Appending a tuple that consists of the number of links of a node and that node aswell.
    for page in set(g.nodes):
        page_links_so_far.append((len(g.adj[page]), page))

    # Sorting the list accumulator and then taking the last n elements of that list to
    # Obtain the top n wikipages
    return reverse_list_sort(page_links_so_far, n)


def top_wiki_pagerank_pages(g: nx.Graph, n: int) -> list:
    """Returns a list of size n of wiki pages within this category that hold the most importance,
    according to pagerank's numerical weighting algorithms. The list is sorted in descending order,
    where each tuple's first element is the importance score and the second is the name of the page.
    If there is less than n pages within this category, the list will return that amount instead.
    """
    page_links_so_far = []
    dict_pages = algorithms.calculate_pagerank(g)

    # Appending each node and it's pagerank using the calculate_pagerank function from algorithms
    for page in dict_pages:
        page_links_so_far.append((dict_pages[page], page))

    # Sorting the list accumulator and then taking the last n elements of that list to
    # Obtain the top n wikipages
    return reverse_list_sort(page_links_so_far, n)


def top_wiki_page_recommendations(page: str, n: int, g: nx.Graph) -> list:
    """ Returns a list of n wikipage recommendations and their score of how similar they are to all
    other nodes within the graph. Sorted in descending order, pages with a similarity score of 0
    will not be included in this list. The list may be less than size n if there are fewer
    recommendations that meet the criteria.
    """
    # Turns the networkx node objects into a readable set
    pages = set(g.nodes)
    pages.remove(page)
    scores_so_far = []

    # Calculate the similarity score between page and each elem in pages
    for elem in pages:
        if elem not in scores_so_far:
            score = similarity_score(page, elem, g)
            if score > 0:
                scores_so_far.append((score, elem))

    # Returns n pages with the greatest similarity scores.
    return reverse_list_sort(scores_so_far, n)


def similarity_score(self: Any, other: Any, g: nx.Graph) -> float:
    """Return the similarity score between self and other. Based upon the similarity score from
    A3.
    """
    if len(g.adj[self]) == 0 or len(g.adj[other]) == 0:
        return 0.0
    else:
        self_adj = set(g.adj[self])
        other_adj = set(g.adj[other])

        # Number of wikipages that are adjacent to both nodes
        num_adjacent_both = len(self_adj.intersection(other_adj))

        # Number of wikipages that are adjacent to either node
        num_adjacent_either = len(self_adj.union(other_adj))

        return num_adjacent_both / num_adjacent_either


def reverse_list_sort(lst: list, n: int) -> list:
    """ Helper function that takes a list and returns the n greatest elements from it.
    """
    # Sort the list using pythons built in sort function, and creates accumulator for the
    # reversed version of this list
    lst.sort()
    reversed_lst = []

    if n > len(lst):
        n = len(lst)

    count = -1
    while count != -n - 1:
        reversed_lst.append((lst[count][0], lst[count][1]))
        count -= 1

    return reversed_lst


def visualize_rankings(cat: str, n: int) -> None:
    """ A graphical visualization comparison of the results of the top wiki pages
    in different categories using the two ranking approaches.
    """
    # Ensuring that we avoid a lengthy exception block if the user enters a category that does
    # not exist
    cond = False
    try:
        wiki_graph.create_digraph(cat)
    except ValueError:
        print('That category doesn\'t exist! Try recalling the function with another one.')
        cond = True

    # Catching for user input errors
    if cond:
        pass
    elif n < 0:
        print('You can\'t ask for an empty visualization!'
              '\nTry recalling this function and asking for at least one or more top pages.')
    else:
        # Creating the networkx graph for the visualization and it's respective ranked lists
        g = wiki_graph.create_digraph(cat)
        lst_basic = top_wiki_pages(g, n)
        lst_pagerank = top_wiki_pagerank_pages(g, n)

        # Unpacking each list tuple and separating them into two lists for reach ranked list
        x_basic = []
        y_basic = []

        for elem in lst_basic:
            x_basic.append(elem[1])
            y_basic.append(elem[0])

        x_pagerank = []
        y_pagerank = []

        for elem in lst_pagerank:
            x_pagerank.append(elem[1])
            y_pagerank.append(elem[0])

        n = max(len(x_basic), len(y_basic))

        # Creating the subplots for each Figure on the page
        fig = make_subplots(rows=3, cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.1,
                            specs=[[{"type": "table"}],
                                   [{"type": "xy"}],
                                   [{"type": "xy"}]],
                            subplot_titles=("Comparison Chart of Top Ranked Pages from Both "
                                            "Algorithms", "Top Ranked Wikipedia Pages using the"
                                            " Basic Algorithm (Pages vs Number of Connections)",
                                            "Top Ranked Wikipedia Pages using Pagerank's Page"
                                            " Importance Algorithm (Pages vs Page Importance"
                                            " Score)"))

        # Creating our Table Figure
        fig.add_trace(
            go.Table(
                header=dict(
                    values=['RANK', 'BASIC ALGORITHM: PAGE NAME', 'BASIC ALGORITHM: CONNECTION'
                                                                  ' SCORE', 'PAGERANK: PAGE NAME',
                            'PAGERANK: IMPORTANCE SCORE'],
                    font=dict(size=10),
                    align="left"
                ),
                cells=dict(
                    values=[
                        [x for x in range(1, n + 1)],
                        x_basic,
                        y_basic,
                        x_pagerank,
                        y_pagerank
                    ],
                    align="left")
            ),
            row=1, col=1
        )
        # Creating our first Bar Graph Figure
        fig.add_trace(go.Bar(x=x_basic, y=y_basic,
                             marker=dict(color=[x for x in range(1, len(x_basic) + 1)])),
                      row=2, col=1)
        # Creating our second Bar Graph Figure
        fig.add_trace(go.Bar(x=x_pagerank, y=y_pagerank,
                             marker=dict(color=[x for x in range(1, len(x_pagerank) + 1)])),
                      row=3, col=1)

        fig.update_layout(title_text="Top Ranking Wikipedia Pages within Category: " + cat,
                          showlegend=False)
        fig.show()


def visualize_recommendation(page: str, n: int, g: nx.Graph) -> None:
    """ A chart visualization of the (at most) top n recommendations of wiki pages given to the user
    for a particular wikipedia page.
    """
    # Error Catching
    if page not in g.nodes:
        print('That page doesn\'t seem to exist in this category!\n'
              'Try recalling the function with another one.')
    elif n < 1:
        print('You can\'t ask for an empty graph!\nTry recalling the function and asking for at '
              'least one or more recommendations.')
    else:

        # Obtaining list of recommendations and their successive URLs
        lst = top_wiki_page_recommendations(page, n, g)
        lst_urls = wiki_link_pages(lst)

        n = len(lst)

        # Updating the above lists to obtain the values for our chart
        page_names = [lst[x][1] for x in range(0, n)]
        similarity_scores = [lst[x][0] for x in range(0, n)]
        urls = [lst_urls[x][1] for x in range(0, n)]

        header_color = 'blue'
        row_even_color = '#D1EEEE'
        row_odd_color = 'white'

        # Creating the chart figure using the above list and other personalized specifics
        fig = go.Figure(data=[go.Table(
            columnwidth=[150, 80, 320],
            header=dict(
                values=['<b>RECOMMENDED PAGES</b>', '<b>SIMILARITY SCORE</b>', '<b>URL</b>'],
                line_color='darkslategray',
                fill_color=header_color,
                align=['left', 'center'],
                font=dict(color='white', size=12)
            ),
            cells=dict(
                values=[
                    page_names,
                    similarity_scores,
                    urls],
                line_color='darkslategray',

                # 2-D list of colors for alternating rows
                fill_color=[[row_odd_color, row_even_color] * n],
                align=['left', 'center'],
                font=dict(color='darkslategray', size=11)
            ))
        ])
        fig.update_layout(
            title_text='<b>Based on your interest in<b> \"' + page + '\", <b>here\'s<b> '
                       + str(n) + ' <b>other Wikipages we recommend you visit.<b>'
        )

        fig.show()


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['networkx', 'graph', 'wikipediaapi'],
        'max-nested-blocks': 4
    })

    # import wiki_graph

    # test_graph = wiki_graph.create_digraph(
    #     'Procedural programming languages')

    # test = top_wiki_pages(test_graph, 25)
    # test2 = top_wiki_pagerank_pages(test_graph, 25)
    # top_wiki_page_recommendations(test[0][1], 15, test_graph)

    # visualize_recommendation(test[0][1], 100, test_graph)
    # visualize_rankings('Procedural programming languages', 100)
