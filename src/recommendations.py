""" Recommendation and Similarity Algorithms used to analyze and return the similarities between
pages within certain Wikipedia Categories"""
import networkx as nx
from typing import Any

import wikipediaapi as w
import algorithms

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
    to other pages and the number of their connections, sorted in descending order. If there is
    less than n pages within this category, the list will return that amount instead. Wikipages
    with the same total number of edges will be sorted alphabetically. This is a more basic and
    straightforward ranking approach compared to top_wiki_pagerank_pages().

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
    where the first element is the most important wiki page in this category. If there is less than
    n pages within this category, the list will return that amount instead. Wikipages that happen
    to have the same value of importance are sorted alphabetically.
    """
    page_links_so_far = []
    dict = algorithms.calculate_pagerank(g)

    # Appending each node and it's pagerank using the calculate_pagerank function from algorithms
    for page in dict:
        page_links_so_far.append((dict[page], page))

    # Sorting the list accumulator and then taking the last n elements of that list to
    # Obtain the top n wikipages
    return reverse_list_sort(page_links_so_far, n)


def top_wiki_page_recommendations(page: str, n: int, g: nx.Graph) -> list:
    """ Returns a list of n wikipage recommendations based on the similarity score of
    page and all other nodes within this nx.graph. Sorted in descending order, pages with
    a similarity score of 0 will not be included in this list. The list may be less than
    size n if there are fewer recommendations that meet the criteria.
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


def similarity_score(self: Any, other: Any, g: nx.graph) -> float:
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
        reversed_lst.append((lst[count][0],lst[count][1]))
        count -= 1

    return reversed_lst


def visualize_rankings(g: nx.Graph, n: int) -> None:
    """ A graphical visualization comparison of the results of the top wiki pages
    in different categories using the two ranking approaches.
    """

    # fig = make_subplots(
    #     rows=3, cols=1,
    #     shared_xaxes=True,
    #     vertical_spacing=0.03,
    #     specs=[[{"type": "table"}],
    #            [{"type": "scatter"}],
    #            [{"type": "scatter"}]]
    # )
    #
    # fig.add_trace(
    #
    # )
    #
    # fig.add_trace(
    #
    # )
    #
    # fig.add_trace(
    #     go.Table(
    #         header=dict(
    #             values=["Date", "Number<br>Transactions", "Output<br>Volume (BTC)",
    #                     "Market<br>Price", "Hash<br>Rate", "Cost per<br>trans-USD",
    #                     "Mining<br>Revenue-USD", "Trasaction<br>fees-BTC"],
    #             font=dict(size=10),
    #             align="left"
    #         ),
    #         cells=dict(
    #             values=,
    #             align="left")
    #     ),
    #     row=1, col=1
    # )
    # fig.update_layout(
    #     height=800,
    #     showlegend=False,
    #     title_text="Bitcoin mining stats for 180 days",
    # )
    #
    # fig.show()



def visualize_recommendation(page: str) -> None:
    """ A graphical visualization of the top recommendations of wiki pages given to the user
    for a particular wikipedia page.
    """




if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'extra-imports': ['networkx', 'graph', 'wikipediaapi'],
    #     'max-nested-blocks': 4
    # })

    import wiki_graph

    # test_graph = wiki_graph.create_digraph(
    #     'Procedural programming languages')  # Large Test
    test_graph = wiki_graph.create_digraph(
        'Prolog programming language family')  # Small Test

    top_wiki_pages(test_graph, 5)
    test = top_wiki_pages(test_graph, 5)
    test2 = top_wiki_pagerank_pages(test_graph, 5)
    
    top_wiki_page_recommendations(test[0][1], 10, test_graph)
