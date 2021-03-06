"""CSC111 Winter 2021: Project Phase 2

Module Description
==================
This module uses Plotly and Networkx to generate visualizations of the graphs and data
computed in the other modules.

Copyright and Usage Information
===============================
The usage of this program should follow the GNU General Public License.

This file is Copyright (c) 2021 Gabe Guralnick, Matthew Toohey, Nathan Hansen, and Azka Azmi.
"""
from decimal import Decimal
from typing import Any, Union
import networkx as nx
from plotly.graph_objs import Scatter, Figure, Histogram
import algorithms


def visualize(values: tuple[list, list, Any], sizes: Union[list, int], labels: list,
              graph: nx.DiGraph, arrows: bool = False) -> None:
    """Generate the visualization of the given graph, with the given node coordinates, labels, and
    sizes.

    Preconditions:
      - all(size > 0 for size in sizes)
    """
    x_values, y_values, pos = values

    fig = Figure()

    if arrows:
        # If arrows, add multiple arrow annotations to the figure for each link and backlink
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
        # If not arrows, add a single trace with multiple lines for all the links and backlinks
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

    # Add the nodes to the figure
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


def visualize_pagerank(graph: nx.DiGraph, min_size: int = 10, max_size: int = 50,
                       link_stats: bool = True, arrows: bool = False) -> None:
    """Visualize the given NetworkX DiGraph and its PageRank properties.

    Preconditions:
      - min_aize > 0
      - max_size > min_size
      - algorithms.assign_pagerank has been called on graph
    """
    # Create a list of partitions using a spring layout
    if graph.number_of_nodes() != 0:
        pos = nx.spring_layout(graph, k=(1 / (graph.number_of_nodes() ** (1 / 4))))
    else:
        pos = nx.spring_layout(graph)

    # If link_stats, create labels using the link stats method, otherwise, use titles
    if link_stats:
        algorithms.assign_link_stats(graph)
        labels = []

        for node in graph.nodes(data=True):
            sci_score = '%.2E' % Decimal(node[1]['pagerank'])
            local_links = node[1]['local_links']
            local_backlinks = node[1]['local_backlinks']
            links = node[1]['links']
            backlinks = node[1]['backlinks']
            labels.append(f'{node[0]} - Score: {sci_score}, Local Links: {local_links},'
                          f' Local Backlinks: {local_backlinks}, Links: {links},'
                          f' Backlinks: {backlinks}')
    else:
        labels = list(graph.nodes())

    if graph.number_of_nodes() != 0:
        sizes = [g_node[1]['pagerank'] for g_node in graph.nodes(data=True)]

        # Calculate a modifier to scale the scores by
        size_modifier = (max_size - min_size) / (max(sizes) - min(sizes))

        # Create a list of sizes for each node using the size modifier and specified size variables
        sizes = [min_size + (size * size_modifier) for size in sizes]
    else:
        sizes = []

    # Use the created variables to call the main visualize function
    visualize(([pos[k][0] for k in graph.nodes], [pos[k][1] for k in graph.nodes], pos),
              sizes, labels, graph, arrows)


def visualize_digraph(graph: nx.DiGraph, node_size: int = 20, arrows: bool = False) -> None:
    """Visualize the given NetworkX DiGraph.

    Preconditions:
      - node_size > 0
    """
    # Create a list of positions using a spring layout
    if graph.number_of_nodes() != 0:
        pos = nx.spring_layout(graph, k=(1 / (graph.number_of_nodes() ** (1 / 4))))
    else:
        pos = nx.spring_layout(graph)

    # Create a list of x values based on the positions
    x_values = [pos[k][0] for k in graph.nodes]
    y_values = [pos[k][1] for k in graph.nodes]

    # Create a list of labels using the graph's nodes
    labels = list(graph.nodes())

    # Use the created variables to call the main visualize function
    visualize((x_values, y_values, pos), node_size, labels, graph, arrows)


def visualize_histograms(graph: nx.DiGraph, local: bool = True) -> None:
    """This function graphs histograms of the inbound and outbound links per page.

    Preconditions:
      - len(graph.nodes) > 0
      - bins > 0
    """
    fig = Figure()

    if local:
        # Extract graph data
        local_links = [node[1]['local_links'] for node in graph.nodes(data=True)]
        local_backlinks = [node[1]['local_backlinks'] for node in graph.nodes(data=True)]

        # Create both traces
        fig.add_trace(Histogram(name='Local Backlinks', x=local_backlinks, bingroup=1))
        fig.add_trace(Histogram(name='Local Links', x=local_links, bingroup=1))

        # Set the barmode and appropriate title
        fig.update_layout(barmode='overlay',
                          title_text="Number of local links vs. local backlinks per page")
    else:
        # Extract graph data
        links = [node[1]['links'] for node in graph.nodes(data=True)]
        backlinks = [node[1]['backlinks'] for node in graph.nodes(data=True)]

        # Create both traces
        fig.add_trace(Histogram(name='Backlinks', x=backlinks, bingroup=1))
        fig.add_trace(Histogram(name='Links', x=links, bingroup=1))

        # Set the barmode and appropriate title
        fig.update_layout(barmode='overlay', title_text="Number of links vs. backlinks per page")

    fig.update_xaxes(title_text='Number of Links')
    fig.update_yaxes(title_text='Number of Pages')
    fig.update_traces(opacity=0.75)

    fig.show()


def visualize_convergence(graph: nx.DiGraph, log_yaxis: bool = True) -> None:
    """Visualize the convergence of the manual PageRank algorithm."""
    # construct dictionary mapping article to a list of PageRank scores, one for each iteration
    all_page_ranks = algorithms.calculate_pagerank_manual(graph)
    article_convergences = dict.fromkeys(all_page_ranks[0].keys(), [])
    for article in article_convergences:
        article_convergences[article] = [iteration[article]
                                         for iteration in all_page_ranks]

    # generate line graph using plotly
    times = list(range(len(all_page_ranks)))
    fig = Figure()
    for article in article_convergences:
        article_scatter = Scatter(x=times,
                                  y=article_convergences[article],
                                  mode='lines+markers',
                                  name=article,
                                  text=article)
        fig.add_trace(article_scatter)
    fig.update_layout(showlegend=True,
                      title=graph.graph['category'] + ' PageRank convergence',
                      xaxis_title='Iteration #',
                      yaxis_title='PageRank Score',
                      legend_title='Articles')
    fig.update_xaxes(showgrid=True, zeroline=True, visible=True)
    if log_yaxis:
        fig.update_yaxes(showgrid=True, zeroline=True,
                         visible=True, type="log")
    else:
        fig.update_yaxes(showgrid=True, zeroline=True, visible=True)
    fig.show()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['networkx', 'plotly.graph_objs', 'decimal', 'algorithms'],
        'max-nested-blocks': 4
    })
