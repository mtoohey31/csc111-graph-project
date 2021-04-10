"""Algorithms for analyzing NetworkX DiGraphs based on Wikipedia articles."""

import networkx as nx


def calculate_pagerank(graph: nx.Graph) -> dict:
    """Use the NetworkX PageRank implementation to
    calculate the PageRanks for all nodes in the graph.
    Returns a dictionary of nodes with PageRanks as values.

    >>> import graph
    >>> g = graph.create_digraph('Logic programming languages')
    >>> from math import isclose
    >>> page_ranks = calculate_pagerank(g)
    >>> isclose(sum(val for val in page_ranks.values()), 1)
    True
    """
    return nx.algorithms.link_analysis.pagerank(graph)


def assign_pagerank(graph: nx.Graph) -> None:
    """Calculate and assign PageRank values to the graph
    as node attributes.

    >>> import graph
    >>> g = graph.create_digraph('Logic programming languages')
    >>> from math import isclose
    >>> assign_pagerank(g)
    >>> isclose(sum(node[1]['pagerank'] for node in g.nodes(data=True)), 1)
    True
    """
    # Calculate PageRanks for the nodes, and assign them as node attributes
    page_ranks = calculate_pagerank(graph)
    for node in graph.nodes():
        graph.nodes[node]["pagerank"] = page_ranks[node]


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'extra-imports': ['networkx', 'graph'],
    #     'max-nested-blocks': 4
    # })

    # import graph
    # test_graph = graph.create_digraph(
    #     'Procedural programming languages')  # Large Test
    # test_graph = graph.create_digraph(
    #     'Prolog programming language family')  # Small Test
    # assign_pagerank(test_graph)
    # print(test_graph.nodes(data=True))
