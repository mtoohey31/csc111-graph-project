"""Algorithms for analyzing NetworkX DiGraphs based on Wikipedia articles."""
import networkx as nx
import wikipediaapi as wa


def calculate_pagerank(graph: nx.Graph) -> dict:
    """Use the NetworkX PageRank implementation to
    calculate the PageRanks for all nodes in the graph.
    Returns a dictionary of nodes with PageRanks as values.

    >>> import wiki_graph
    >>> g = wiki_graph.create_digraph('Logic programming languages')
    >>> from math import isclose
    >>> page_ranks = calculate_pagerank(g)
    >>> isclose(sum(val for val in page_ranks.values()), 1)
    True
    """
    return nx.algorithms.link_analysis.pagerank(graph)


def calculate_pagerank_manual(g: nx.Graph, alpha: float = 0.85,
                              max_iter: int = 100, tol=1.0e-6) -> dict:
    """A manual implementation of the PageRank algorithm.
    Calculates the PageRanks for all nodes in the graph, and returns
    a dictionary of nodes with PageRanks as values.
    Uses the iterative computation method from https://en.wikipedia.org/wiki/PageRank.

    >>> import wiki_graph
    >>> g = wiki_graph.create_digraph('Logic programming languages')
    >>> from math import isclose
    >>> page_ranks = calculate_pagerank_manual(g)
    >>> isclose(sum(val for val in page_ranks.values()), 1)
    True
    """
    if not g.is_directed():
        graph = g.to_directed()
    else:
        graph = g
    page_ranks = {}
    size = len(graph.nodes)
    for node in graph.nodes:
        page_ranks[node] = 1 / size
    for _ in range(max_iter):
        page_ranks_last = page_ranks
        for node in graph.nodes:
            page_ranks[node] = (1 - alpha) / size
            neighbors = graph.predecessors(node)
            for n in neighbors:
                outgoing_degree = graph.out_degree[n]
                page_ranks[node] += alpha * (page_ranks[n] / outgoing_degree)
        error = sum(abs(page_ranks[n] - page_ranks_last[n]) for n in page_ranks)
        if error < len(graph.nodes) * tol:
            return page_ranks
    raise ValueError(f'pagerank calculation failed to converge in {max_iter} iterations')


def assign_pagerank(graph: nx.Graph, manual: bool = False) -> None:
    """Calculate and assign PageRank values to the graph
    as node attributes.

    >>> import wiki_graph
    >>> g = wiki_graph.create_digraph('Logic programming languages')
    >>> from math import isclose
    >>> assign_pagerank(g)
    >>> isclose(sum(node[1]['pagerank'] for node in g.nodes(data=True)), 1)
    True
    """
    # Calculate PageRanks for the nodes, and assign them as node attributes
    if manual:
        page_ranks = calculate_pagerank_manual(g)
    else:
        page_ranks = calculate_pagerank(graph)
    for node in graph.nodes():
        graph.nodes[node]["pagerank"] = page_ranks[node]


def assign_link_stats(graph: nx.Graph) -> None:
    """Calculate link statistics the given graph and assign them as node attributes."""
    category = graph.graph['category']

    wiki = wa.Wikipedia('en')
    cat = wiki.page(f'Category:{category}')

    for node in graph.nodes:
        node_object = graph.nodes[node]['object']
        graph.add_node(node, local_links=len(
            set(node_object.links).intersection(set(cat.categorymembers))))
        graph.add_node(node, local_backlinks=len(
            set(node_object.backlinks).intersection(set(cat.categorymembers))))
        graph.add_node(node, links=len(node_object.links))
        graph.add_node(node, backlinks=len(node_object.backlinks))


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

    # PageRank test
    # assign_pagerank(test_graph)
    # print(test_graph.nodes(data=True))

    # Stats test
    assign_link_stats(test_graph)
    print(test_graph.nodes(data=True))
