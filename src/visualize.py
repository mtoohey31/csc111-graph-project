"""A module to visualize NetworkX graphs in Plotly."""

from decimal import Decimal
from typing import Any, Union

import networkx as nx
from plotly.graph_objs import Scatter, Figure
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import algorithms


def visualize_digraph(graph: nx.DiGraph, node_size: int = 20, arrows: bool = False) -> None:
    """Visualize the given NetworkX DiGraph."""
    pos = getattr(nx, 'spring_layout')(
        graph, k=1 / (graph.number_of_nodes() ** (1/4)))

    x_values = [pos[k][0] for k in graph.nodes]
    y_values = [pos[k][1] for k in graph.nodes]

    labels = list(graph.nodes())

    visualize(x_values, y_values, node_size, labels, graph, pos, arrows)


def visualize_histograms(graph: nx.DiGraph, bins: int = 100) -> None:
    """This function graphs histograms of the inbound and outbound links per page.
    Preconditions:
      - len(test_graph.nodes) > 0
      - bins > 0
    """

    # extract graph data
    page_names = [node[0] for node in graph.nodes(data=True)]
    link_data = [len(node[1]['object'].links)
                 for node in graph.nodes(data=True)]
    backlink_data = [len(node[1]['object'].backlinks)
                     for node in graph.nodes(data=True)]
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


def visualize_pagerank(graph: nx.DiGraph, min_size: int = 10, max_size: int = 50,
                       link_stats: bool = True, arrows: bool = False) -> None:
    """Visualize the given NetworkX DiGraph and its PageRank properties."""
    pos = getattr(nx, 'spring_layout')(
        graph, k=1 / (graph.number_of_nodes() ** (1/4)))

    x_values = [pos[k][0] for k in graph.nodes]
    y_values = [pos[k][1] for k in graph.nodes]

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

    visualize(x_values, y_values, sizes, labels, graph, pos, arrows)


def visualize(x_values: list, y_values: list, sizes: Union[list, int], labels: list,
              graph: nx.DiGraph, pos: Any, arrows: bool = False) -> None:
    """Generate the visualization of the given graph, with the given
    node coordinates, labels, and sizes."""
    fig = Figure()

    if arrows:
        for edge in graph.edges():
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
                opacity=0.25
            )
    else:
        x_edges = []
        y_edges = []
        for edge in graph.edges():
            x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
            y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

        fig.add_trace(Scatter(x=x_edges,
                              y=y_edges,
                              mode='lines',
                              name='edges',
                              line=dict(width=1),
                              opacity=0.25,
                              hoverinfo='none'
                              ))

    fig.add_trace(Scatter(x=x_values,
                          y=y_values,
                          mode='markers',
                          name='nodes',
                          marker=dict(symbol='circle-dot',
                                      size=sizes,
                                      line=dict(width=0.5),
                                      ),
                          text=labels,
                          hovertemplate='%{text}',
                          hoverlabel={'namelength': 0}
                          ))

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
