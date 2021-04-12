"""A module to visualize NetworkX graphs in Plotly."""

from decimal import Decimal
from typing import Any, Union

import networkx as nx
from plotly.graph_objs import Scatter, Figure

# https://www.nordtheme.com/
NORD = ['#2E3440', '#3B4252', '#434C5E', '#4C566A', '#D8DEE9', '#E5E9F0', '#ECEFF4', '#8FBCBB',
        '#88C0D0', '#81A1C1', '#5E81AC', '#BF616A', '#D08770', '#EBCB8B', '#A3BE8C', '#B48EAD']


def visualize_digraph(graph: nx.DiGraph, node_size: int = 20, arrows: bool = False) -> None:
    """Visualize the given NetworkX DiGraph."""
    pos = getattr(nx, 'spring_layout')(
        graph, k=1 / (graph.number_of_nodes() ** (1/4)))

    x_values = [pos[k][0] for k in graph.nodes]
    y_values = [pos[k][1] for k in graph.nodes]

    labels = list(graph.nodes())

    colours = []
    for i in range(graph.number_of_nodes()):
        colours.append(NORD[7:][i % len(NORD[7:])])

    visualize(x_values, y_values, node_size,
              colours, labels, graph, pos, arrows)


def visualize_pagerank(graph: nx.DiGraph, min_size: int = 10, max_size: int = 50,
                       link_stats: bool = True, arrows: bool = False) -> None:
    """Visualize the given NetworkX DiGraph and its PageRank properties."""
    pos = getattr(nx, 'spring_layout')(
        graph, k=1 / (graph.number_of_nodes() ** (1/4)))

    x_values = [pos[k][0] for k in graph.nodes]
    y_values = [pos[k][1] for k in graph.nodes]

    colours = []
    for i in range(graph.number_of_nodes()):
        colours.append(NORD[7:][i % len(NORD[7:])])

    scores = [node[1]['pagerank'] for node in graph.nodes(data=True)]

    if link_stats:
        algorithms.assign_link_stats(graph)
        labels = []

        for node in graph.nodes(data=True):
            title = node[0]
            sci_score = '%.2E' % Decimal(node[1]['pagerank'])
            local_links = node[1]['local_links']
            local_backlinks = node[1]['local_backlinks']
            links = node[1]['links']
            backlinks = node[1]['backlinks']
            labels.append(f'{title} - Score: {sci_score}, Local Links: {local_links},' +
                          f' Local Backlinks: {local_backlinks}, Links: {links},' +
                          f' Backlinks: {backlinks}')
    else:
        labels = list(graph.nodes())

    size_modifier = (max_size - min_size) / (max(scores) - min(scores))

    sizes = [min_size + (size * size_modifier) for size in scores]

    visualize(x_values, y_values, sizes, colours, labels, graph, pos, arrows)


def visualize(x_values: list, y_values: list, sizes: Union[list, int], colours: list,
              labels: list, graph: nx.DiGraph, pos: Any, arrows: bool = False) -> None:
    """Generate the visualization of the given graph, with the given
    node coordinates, labels, sizes and colours."""
    fig = Figure()

    if arrows:
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
                arrowhead=5,
                arrowsize=1,
                arrowwidth=1,
                arrowcolor=NORD[1],
                opacity=0.25
            )
    else:
        x_edges = []
        y_edges = []
        for edge in graph.edges:
            x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
            y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

        fig.add_trace(Scatter(x=x_edges,
                              y=y_edges,
                              mode='lines',
                              name='edges',
                              line=dict(color=NORD[1], width=1),
                              opacity=0.25,
                              hoverinfo='none'
                              ))

    fig.add_trace(Scatter(x=x_values,
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
                          ))

    fig.update_layout(showlegend=False, title=graph.graph['category'])
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False,)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False,)

    fig.show()


def visualize_convergence(graph: nx.Graph) -> None:
    """Visualize the convergence of the manual PageRank algorithm.
    Note that the results of this algorithm differ slightly from the NetworkX implementation.
    """
    all_page_ranks = algorithms.calculate_pagerank_manual(graph)
    article_convergences = dict.fromkeys(all_page_ranks[0].keys(), [])
    for article in article_convergences:
        article_convergences[article] = [iteration[article] for iteration in all_page_ranks]
    times = [i for i in range(len(all_page_ranks))]
    fig = Figure()
    for article in article_convergences:
        article_scatter = Scatter(x=times,
                                  y=article_convergences[article],
                                  mode='lines+markers',
                                  name=article)
        fig.add_trace(article_scatter)
    fig.update_layout(showlegend=True, title=graph.graph['category'] + ' PageRank convergence')
    fig.update_xaxes(showgrid=True, zeroline=True, visible=True)
    fig.update_yaxes(showgrid=True, zeroline=True, visible=True)
    fig.show()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'extra-imports': ['networkx', 'plotly.graph_objs', 'graph', 'decimal', 'algorithms'],
    #     'max-nested-blocks': 4
    # })

    import wiki_graph

    # test_graph = wiki_graph.create_digraph(
    #     'Procedural programming languages')  # Large Test
    test_graph = wiki_graph.create_digraph(
        'Prolog programming language family')  # Small Test

    # DiGraph test
    # visualize_digraph(test_graph)

    # PageRank test
    import algorithms
    algorithms.assign_pagerank(test_graph)
    visualize_convergence(test_graph)
    # visualize_pagerank(test_graph, arrows=False)
