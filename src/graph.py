"""Module for creating NetworkX graphs given a Wikipedia cateogry title."""

import networkx as nx
import wikipediaapi as wa


def create_digraph(category: str) -> nx.DiGraph:
    """Return a NetworkX DiGraph of the given Wikipedia category.

    >>> graph = create_digraph('Logic programming languages')
    >>> len(graph.nodes())
    45
    >>> len(graph.edges())
    86
    >>> 'Prolog' in graph.nodes()
    True
    """
    # Create necessary api variables
    wiki = wa.Wikipedia('en')
    cat = wiki.page(f'Category:{category}')

    # Throw an error if the provided category doesn't exist
    if not cat.exists():
        raise ValueError('Category not found.')

    mems = cat.categorymembers
    G = nx.DiGraph()

    # Add each page to the graph and add its wikipediaapi object to the node as an attribute
    for page in mems:
        G.add_node(page, obj=mems[page])

    # Add links between pages within the cateogory
    for page in mems:
        for linked in mems[page].links:
            if linked in mems:
                G.add_edge(page, linked)

    # Calculate PageRanks for the nodes, and assign them as node attributes
    page_ranks = calculate_pagerank(G)
    for node in G.nodes():
        G.nodes[node]["pagerank"] = page_ranks[node]
    return G


def calculate_pagerank(graph: nx.Graph) -> dict:
    """Use the NetworkX PageRank implementation to
    calculate the PageRanks for all nodes in the graph.
    Returns a dictionary of nodes with PageRanks as values."""
    return nx.algorithms.link_analysis.pagerank(graph)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'extra-imports': ['networkx', 'wikipediaapi'],
    #     'max-nested-blocks': 4
    # })
