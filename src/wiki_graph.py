"""CSC111 Winter 2021: Project Phase 2

Module Description
==================
This module is for creating NetworkX graphs given a Wikipedia category title.

Copyright and Usage Information
===============================
The usage of this program should follow the GNU General Public License.

This file is Copyright (c) 2021 Gabe Guralnick, Matthew Toohey, Nathan Hansen, and Azka Azmi.
"""
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
    digraph = nx.DiGraph(category=category)

    # Add each page to the graph and add its wikipediaapi object to the node as an attribute
    for page in mems:
        digraph.add_node(page, object=mems[page])

    # Add links between pages within the cateogory
    for page in mems:
        for linked in mems[page].links:
            if linked in mems:
                digraph.add_edge(page, linked)

    return digraph


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['networkx', 'wikipediaapi'],
        'max-nested-blocks': 4
    })
