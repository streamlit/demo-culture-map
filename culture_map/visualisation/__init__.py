import matplotlib.pyplot as plt
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
