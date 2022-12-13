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