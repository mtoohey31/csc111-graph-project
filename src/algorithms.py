"""CSC111 Winter 2021: Project Phase 2

Module Description
==================
This module contains algorithms for analyzing NetworkX DiGraphs which were generated from
Wikipedia articles.

Copyright and Usage Information
===============================
The usage of this program should follow the GNU General Public License.

This file is Copyright (c) 2021 Gabe Guralnick, Matthew Toohey, Nathan Hansen, and Azka Azmi.
"""
import networkx as nx


def calculate_pagerank_manual(graph: nx.DiGraph, alpha: float = 0.85, max_iter: int = 100,
                              tol: float = 1.0e-6) -> list[dict]:
    """A manual implementation of the PageRank algorithm. Calculates the PageRanks for all nodes in
    the graph, and returns a dictionary of nodes with PageRanks as values. Uses the iterative
    computation method from https://en.wikipedia.org/wiki/PageRank. Note that the results of this
    algorithm differ slightly from the NetworkX implementation.

    Preconditions:
        - 0 <= alpha <= 1
        - max_iter >= 1

    >>> import wiki_graph
    >>> g = wiki_graph.create_digraph('Logic programming languages')
    >>> from math import isclose
    >>> page_ranks = calculate_pagerank_manual(g)
    >>> isclose(sum(val for val in page_ranks[-1].values()), 1, abs_tol=0.05)
    True
    """
    all_page_ranks = []
    page_ranks = {}
    size = len(graph.nodes)

    # initialize each node's score to 1/N
    for node in graph.nodes:
        page_ranks[node] = 1.0 / size

    # find nodes with no out edges
    dangling_nodes = [n for n in graph.nodes if graph.out_degree[n] == 0.0]

    for _ in range(max_iter):
        page_ranks_last = page_ranks.copy()
        all_page_ranks.append(page_ranks_last)
        danglesum = alpha * sum(page_ranks[n] for n in dangling_nodes)

        # PR(P) = (1-d)/N + d(sum(PR(i))/(L(i)) for neighbors of P) + d(sum of dangling edge scores)
        for node in graph.nodes:
            neighbors = graph.predecessors(node)
            page_ranks[node] = alpha * sum(page_ranks[n] / graph.out_degree[n]
                                           for n in neighbors)
            page_ranks[node] += (1.0 - alpha) / size + danglesum / float(size)

        # check for convergence
        error = sum(abs(page_ranks[n] - page_ranks_last[n])
                    for n in page_ranks)
        if error < len(graph.nodes) * tol:
            return all_page_ranks + [page_ranks]
    raise ValueError(
        f'pagerank calculation failed to converge in {max_iter} iterations')


def calculate_pagerank(graph: nx.DiGraph) -> dict:
    """Use the NetworkX PageRank implementation to calculate the PageRanks for all nodes in the
    graph. Returns a dictionary of nodes with PageRanks as values.

    >>> import wiki_graph
    >>> g = wiki_graph.create_digraph('Logic programming languages')
    >>> from math import isclose
    >>> page_ranks = calculate_pagerank(g)
    >>> isclose(sum(val for val in page_ranks.values()), 1)
    True
    """
    return nx.algorithms.link_analysis.pagerank(graph)


def assign_pagerank(graph: nx.DiGraph, manual: bool = False) -> None:
    """Calculate and assign PageRank values to the graph as node attributes.

    >>> import wiki_graph
    >>> g = wiki_graph.create_digraph('Logic programming languages')
    >>> from math import isclose
    >>> assign_pagerank(g)
    >>> isclose(sum(node[1]['pagerank'] for node in g.nodes(data=True)), 1)
    True
    """
    # Calculate PageRanks for the nodes
    if manual:
        # If using the manual function, use the final set of values
        page_ranks = calculate_pagerank_manual(graph)[-1]
    else:
        page_ranks = calculate_pagerank(graph)
    # Assign the values as node attributes
    for node in graph.nodes():
        graph.nodes[node]["pagerank"] = page_ranks[node]


def assign_link_stats(graph: nx.DiGraph) -> None:
    """Calculate link statistics for the given graph and assign them as node attributes.

    >>> import wiki_graph
    >>> g = wiki_graph.create_digraph('Prolog programming language family')
    >>> assign_link_stats(g)
    >>> node = list(g.nodes(data=True))[0][1]
    >>> node['links']
    12
    >>> node['backlinks']
    4
    >>> node['local_links']
    1
    >>> node['local_backlinks']
    0
    """
    for node in graph.nodes:
        node_object = graph.nodes[node]['object']
        graph.add_node(node, local_links=len(graph.out_edges(node)),
                       local_backlinks=len(graph.in_edges(node)), links=len(node_object.links),
                       backlinks=len(node_object.backlinks))


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['networkx', 'wiki_graph'],
        'max-nested-blocks': 4
    })
