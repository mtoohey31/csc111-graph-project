"""A module to visualize NetworkX graphs in Plotly."""

from decimal import Decimal
from typing import Any, Union

import networkx as nx
from plotly.graph_objs import Scatter, Figure
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# https://www.nordtheme.com/
NORD = ['#2E3440', '#3B4252', '#434C5E', '#4C566A', '#D8DEE9', '#E5E9F0', '#ECEFF4', '#8FBCBB',
        '#88C0D0', '#81A1C1', '#5E81AC', '#BF616A', '#D08770', '#EBCB8B', '#A3BE8C', '#B48EAD']


def visualize_digraph(graph: nx.DiGraph,
                      layout: str = 'kamada_kawai_layout', node_size: int = 20) -> None:
    """Visualize the given NetworkX DiGraph."""
    pos = getattr(nx, layout)(graph)

    x_values = [pos[k][0] for k in graph.nodes]
    y_values = [pos[k][1] for k in graph.nodes]

    labels = list(graph.nodes())

    colours = []
    for i in range(len(graph.nodes)):
        colours.append(NORD[7:][i % len(NORD[7:])])

    visualize(x_values, y_values, node_size, colours, labels, graph, pos)


def visualize_histograms(graph: nx.DiGraph, bins: int = 100) -> None:
    """This function graphs histograms of the inbound and outbound links per page.
    Preconditions:
      - len(test_graph.nodes) > 0
      - bins > 0
    """

    # extract graph data
    page_names = [node[0] for node in graph.nodes(data=True)]
    link_data = [len(node[1]['object'].links) for node in graph.nodes(data=True)]
    backlink_data = [len(node[1]['object'].backlinks) for node in graph.nodes(data=True)]
    # create dataframe
    df = pd.DataFrame()
    df['page_name'] = page_names
    df['links'] = link_data
    df['backlinks'] = backlink_data
    # create histogram
    fig = go.Figure()
    fig.add_trace(go.Histogram(name='Links', x=link_data, nbinsx=bins))
    fig.add_trace(go.Histogram(name='Backlinks', x=backlink_data, nbinsx=bins))

    fig.update_layout(barmode='overlay', title_text="Number of links vs. backlinks per page",
                      legend_title_text='Link Type:')
    fig.update_xaxes(title_text='Number of Links')
    fig.update_yaxes(title_text='Number of Pages')
    fig.update_traces(opacity=0.75)

    fig.show()


def visualize_pagerank(graph: nx.DiGraph, layout: str = 'spring_layout',
                       min_size: int = 10, max_size: int = 50, link_stats: bool = True) -> None:
    """Visualize the given NetworkX DiGraph and its PageRank properties."""
    pos = getattr(nx, layout)(graph)

    x_values = [pos[k][0] for k in graph.nodes]
    y_values = [pos[k][1] for k in graph.nodes]

    colours = []
    for i in range(len(graph.nodes)):
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

    visualize(x_values, y_values, sizes, colours, labels, graph, pos)


def visualize(x_values: list, y_values: list, sizes: Union[list, int], colours: list,
              labels: list, graph: nx.DiGraph, pos: Any) -> None:
    """Generate the visualization of the given graph, with the given
    node coordinates, labels, sizes and colours."""
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
            arrowhead=5,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=NORD[1],
            opacity=0.25
        )

    fig.update_layout(showlegend=False, title=graph.graph['category'])
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

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

    test_graph = wiki_graph.create_digraph(
        'Procedural programming languages')  # Large Test
    # test_graph = wiki_graph.create_digraph(
    #     'Prolog programming language family')  # Small Test

    # DiGraph test
    # visualize_digraph(test_graph)

    # PageRank test
    # import algorithms
    # algorithms.assign_pagerank(test_graph)
    # visualize_pagerank(test_graph)

    # Dual Histogram test
    visualize_histograms(test_graph)
