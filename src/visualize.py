"""A module to visualize NetworkX graphs in Plotly."""

from decimal import Decimal
import networkx as nx
from plotly.graph_objs import Scatter, Figure

# https://www.nordtheme.com/
NORD = ['#2E3440', '#3B4252', '#434C5E', '#4C566A', '#D8DEE9', '#E5E9F0', '#ECEFF4', '#8FBCBB',
        '#88C0D0', '#81A1C1', '#5E81AC', '#BF616A', '#D08770', '#EBCB8B', '#A3BE8C', '#B48EAD']


def visualize_digraph(graph: nx.DiGraph,
                      layout: str = 'spring_layout', node_size: int = 20) -> None:
    """Visualize the given NetworkX DiGraph."""
    pos = getattr(nx, layout)(graph)

    x_values = [pos[k][0] for k in graph.nodes]
    y_values = [pos[k][1] for k in graph.nodes]

    labels = list(graph.nodes())

    colours = []
    for i in range(len(graph.nodes)):
        colours.append(NORD[7:][i % len(NORD[7:])])

    fig = Figure(data=[
        Scatter(x=x_values,
                y=y_values,
                mode='markers',
                name='nodes',
                marker=dict(symbol='circle-dot',
                            size=node_size,
                            color=colours,
                            line=dict(color=NORD[1], width=0.5),
                            ),
                text=labels,
                hovertemplate='%{text}',
                hoverlabel={'namelength': 0}
                )])

    for edge in graph.edges:
        fig.add_annotation(
            x=pos[edge[0]][0],
            y=pos[edge[0]][1],
            ax=pos[edge[1]][0],
            ay=pos[edge[1]][1],
            xref='x',
            yref='y',
            axref='x',
            ayref='y',
            text='',
            showarrow=True,
            arrowhead=3,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=NORD[1]
        )

    fig.show()


def visualize_pagerank(graph: nx.DiGraph, layout: str = 'spring_layout',
                       min_size: int = 10, max_size: int = 50) -> None:
    """Visualize the given NetworkX DiGraph and its PageRank properties."""
    pos = getattr(nx, layout)(graph)

    x_values = [pos[k][0] for k in graph.nodes]
    y_values = [pos[k][1] for k in graph.nodes]

    colours = []
    for i in range(len(graph.nodes)):
        colours.append(NORD[7:][i % len(NORD[7:])])

    scores = [node[1]['pagerank'] for node in graph.nodes(data=True)]

    labels = [node[0] + ' - Score: ' + '%.2E' % Decimal(node[1]['pagerank']) + ', Links: ' + str(
        len(node[1]['object'].backlinks)) + ', Backlinks: ' + str(len(node[1]['object'].backlinks))
        for node in graph.nodes(data=True)]

    scalar = (max_size - min_size) / (max(scores) - min(scores))

    sizes = [min_size + (size * scalar) for size in scores]

    fig = Figure(data=[
        Scatter(x=x_values,
                y=y_values,
                mode='markers',
                name='nodes',
                marker=dict(symbol='circle-dot',
                            size=sizes,
                            color=colours,
                            line=dict(color=NORD[1], width=0.5),
                            ),
                text=labels,
                hovertemplate='%{text}',
                hoverlabel={'namelength': 0}
                )])

    for edge in graph.edges:
        fig.add_annotation(
            x=pos[edge[0]][0],
            y=pos[edge[0]][1],
            ax=pos[edge[1]][0],
            ay=pos[edge[1]][1],
            xref='x',
            yref='y',
            axref='x',
            ayref='y',
            text='',
            showarrow=True,
            arrowhead=3,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=NORD[1],
            opacity=0.25
        )

    fig.show()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['networkx', 'plotly.graph_objs', 'graph', 'decimal', 'algorithms'],
        'max-nested-blocks': 4
    })

    import graph

    # test_graph = graph.create_digraph(
    #     'Procedural programming languages')  # Large Test
    test_graph = graph.create_digraph(
        'Prolog programming language family')  # Small Test

    # DiGraph test
    # visualize_digraph(test_graph)

    # PageRank test
    import algorithms
    algorithms.assign_pagerank(test_graph)
    visualize_pagerank(test_graph)
