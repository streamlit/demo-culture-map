import math

import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns

DEFAULT_COLORMAP = "coolwarm_r"
DEFAULT_FORMAT = '.0f'
DEFAULT_TEXT_ROTATION_DEGREES = 80
POLAR_PLOT_Y_TICKS_RANGE = [i for i in range(0, 120, 20)]
POLAR_Y_TICKS_SIZE = 7
POLAR_X_TICKS_SIZE = 8
COLOR_GREY = "grey"
COLOR_DARKS_LATE_GREY = "darkslategrey"
FONT_FAMILY_SANS_SERIF = 'sans-serif'
MAX_VALUE_PER_DIMENSION = 100
SOLID_LINE_STYLE = 'solid'
SCATTERPLOT_COLOR_MAP = 'Spectral'
SCATTERPLOT_FONT_SIZE = 9
RADAR_PLOTS_COLOR_MAP = "Set2"
RADAR_PLOTS_PADDING = 1.5
RADAR_PLOT_SIZE = 1000
DISPLAY_DPI = 96
RADAR_PLOT_TITLE_FONT_SIZE = 11
RADAR_PLOT_TITLE_Y_POSITION = 1.2
RADAR_PLOT_ALPHA_CHANNEL = 0.4
TEXT_COORDS_OFFSET_POINTS = 'offset points'


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
    cmap = cm.get_cmap(SCATTERPLOT_COLOR_MAP)
    coords.plot.scatter(x=coords.columns[0], y=coords.columns[1], ax=ax, s=120, linewidth=1,
                        c=range(len(coords)),  colormap=cmap, alpha=0.5)
    ax.grid(True, linestyle='--')
    for k, v in coords.iterrows():
        ax.annotate(k, v,
                    xytext=(10, -5), textcoords=TEXT_COORDS_OFFSET_POINTS,
                    family=FONT_FAMILY_SANS_SERIF, fontsize=SCATTERPLOT_FONT_SIZE, color=COLOR_DARKS_LATE_GREY)
    ax.set_title("Cultural distance in 2D")
    return fig


def generate_radar_plot(dimensions):
    fig = plt.figure(figsize=(RADAR_PLOT_SIZE/DISPLAY_DPI, RADAR_PLOT_SIZE/DISPLAY_DPI), dpi=DISPLAY_DPI)

    # Create a color palette:
    my_palette = plt.cm.get_cmap(RADAR_PLOTS_COLOR_MAP, len(dimensions.columns))

    # Loop to plot
    for idx, country in enumerate(dimensions.columns):
        make_spider(idx, country, my_palette(idx), dimensions)

    fig.tight_layout(pad=RADAR_PLOTS_PADDING)
    return fig


def make_spider(col, title, color, dimensions):

    # number of variable
    categories = list(dimensions.index)
    num_categories = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(num_categories) * 2 * math.pi for n in range(num_categories)]
    angles += angles[:1]

    # Initialise the spider plot
    side_len = math.ceil(math.sqrt(len(dimensions.columns)))
    ax = plt.subplot(side_len, side_len, col+1, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color=COLOR_GREY, size=POLAR_X_TICKS_SIZE)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks(POLAR_PLOT_Y_TICKS_RANGE, list(map(str, POLAR_PLOT_Y_TICKS_RANGE)),
               color=COLOR_GREY, size=POLAR_Y_TICKS_SIZE)
    plt.ylim(0, MAX_VALUE_PER_DIMENSION)

    # Ind1
    values = dimensions[title].values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, color=color, linewidth=2, linestyle=SOLID_LINE_STYLE)
    ax.fill(angles, values, color=color, alpha=RADAR_PLOT_ALPHA_CHANNEL)

    # Add a title
    plt.title(title, size=RADAR_PLOT_TITLE_FONT_SIZE, color=color, y=RADAR_PLOT_TITLE_Y_POSITION)
