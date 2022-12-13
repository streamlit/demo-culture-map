import math

import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns

DEFAULT_COLORMAP = "coolwarm_r"
DEFAULT_FORMAT = '.0f'
DEFAULT_TEXT_ROTATION_DEGREES = 80


def generate_heatmap(distances, show_clusters: bool):
    fig, ax = plt.subplots()
    plt.xticks(rotation=DEFAULT_TEXT_ROTATION_DEGREES)
    if show_clusters:
        fig = sns.clustermap(distances, cmap=DEFAULT_COLORMAP, annot=True, fmt=DEFAULT_FORMAT)
    else:
        sns.heatmap(distances, ax=ax, cmap=DEFAULT_COLORMAP, annot=True, fmt=DEFAULT_FORMAT)
        fig.tight_layout()
    return fig


def generate_scatterplot(coords):
    fig, ax = plt.subplots()
    cmap = cm.get_cmap('Spectral')
    coords.plot.scatter(x=coords.columns[0], y=coords.columns[1], ax=ax, s=120, linewidth=0,
                        c=range(len(coords)),  colormap=cmap)
    for k, v in coords.iterrows():
        ax.annotate(k, v,
                    xytext=(10, -5), textcoords='offset points',
                    family='sans-serif', fontsize=9, color='darkslategrey')
    return fig


def generate_radar_plot(dimensions):
    my_dpi = 96
    fig = plt.figure(figsize=(1000/my_dpi, 1000/my_dpi), dpi=my_dpi)

    # Create a color palette:
    my_palette = plt.cm.get_cmap("Set2", len(dimensions.columns))

    # Loop to plot
    for idx, country in enumerate(dimensions.columns):
        make_spider(idx, country, my_palette(idx), dimensions)

    return fig


def make_spider(col, title, color, dimensions):

    # number of variable
    categories=list(dimensions.index)
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(4, 4, col+1, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=8)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0, 20, 40, 60, 80, 100], ["0", "20", "40", "60", "80", "100"], color="grey", size=7)
    plt.ylim(0, 100)

    # Ind1
    values=dimensions[title].values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
    ax.fill(angles, values, color=color, alpha=0.4)

    # Add a title
    plt.title(title, size=11, color=color, y=1.2)
