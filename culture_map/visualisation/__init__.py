import math

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LabelSet, ImageURL
import matplotlib.pyplot as plt
from culture_map.visualisation.country_urls import COUNTRY_URLS
import seaborn as sns
import plotly.express as px

from culture_map import distance_calculations

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
SCATTERPLOT_LINE_STYLE = '--'
SCATTERPLOT_TITLE = "Cultural distance in 2D"
RADAR_PLOTS_COLOR_MAP = "Set2"
RADAR_PLOTS_PADDING = 1.5
RADAR_PLOT_SIZE = 1000
DISPLAY_DPI = 96
RADAR_PLOT_TITLE_FONT_SIZE = 11
RADAR_PLOT_TITLE_Y_POSITION = 1.2
RADAR_PLOT_ALPHA_CHANNEL = 0.4
TEXT_COORDS_OFFSET_POINTS = 'offset points'


def generate_heatmap(
        distances: distance_calculations.PandasDataFrame,
        show_clusters: bool
) -> plt.Figure:
    fig, ax = plt.subplots()
    plt.xticks(rotation=DEFAULT_TEXT_ROTATION_DEGREES)
    if show_clusters:
        fig = sns.clustermap(distances, cmap=DEFAULT_COLORMAP, annot=True, fmt=DEFAULT_FORMAT)
    else:
        sns.heatmap(distances, ax=ax, cmap=DEFAULT_COLORMAP, annot=True, fmt=DEFAULT_FORMAT)
        fig.tight_layout()
    return fig


def generate_scatterplot(
        coords: distance_calculations.PandasDataFrame
) -> plt.Figure:
    data = {str(key): val for key, val in coords.to_dict(orient="list").items()}
    data["names"] = coords.index
    max_x, max_y = max(data['0']), max(data['1'])
    min_x, min_y = min(data['0']), min(data['1'])
    x_margin, y_margin = (max_x - min_x) * 0.2, (max_y - min_y) * 0.2
    fig = figure(width=800, height=800, x_range=(min_x - x_margin, max_x + x_margin),
                 y_range=(min_y - y_margin, max_y + y_margin), title="Culture distance in 2D")
    source = ColumnDataSource(data=data)
    labels = LabelSet(x='0', y='1', text='names',
                      x_offset=10, y_offset=10, source=source, render_mode='canvas')
    fig.add_layout(labels)
    for country_name, country_coords in coords.iterrows():
        img = ImageURL(url=dict(value=COUNTRY_URLS[country_name]), x=country_coords[0],
                       y=country_coords[1], w=5, h=2, anchor="center")
        fig.add_glyph(source, img)
    return fig


def generate_radar_plot(
        dimensions: distance_calculations.PandasDataFrame,
        reference: distance_calculations.PandasDataFrame | None = None
) -> plt.Figure:
    fig = plt.figure(figsize=(RADAR_PLOT_SIZE/DISPLAY_DPI, RADAR_PLOT_SIZE/DISPLAY_DPI), dpi=DISPLAY_DPI)

    # Create a color palette:
    my_palette = plt.cm.get_cmap(RADAR_PLOTS_COLOR_MAP, len(dimensions.columns))

    # Loop to plot
    for idx, country in enumerate(dimensions.columns):
        make_spider(idx, country, my_palette(idx), dimensions, reference)

    fig.tight_layout(pad=RADAR_PLOTS_PADDING)
    return fig


def generate_choropleth(
        dimensions: distance_calculations.PandasDataFrame,
        dimension_name: str
) -> plt.Figure:
    transposed = dimensions.transpose()
    transposed.reset_index(inplace=True)
    transposed = transposed.rename(columns={'index': 'country'})
    print(transposed)
    fig = px.choropleth(transposed, locationmode="country names", locations="country", color=dimension_name,
                        hover_name="country", color_continuous_scale=px.colors.sequential.Plasma)
    return fig


def make_spider(
        col: int,
        title: str,
        color: str,
        dimensions: distance_calculations.PandasDataFrame,
        reference: distance_calculations.PandasDataFrame | None = None
) -> None:

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

    # Ind2
    if reference is not None:
        values = reference["distance"].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, color="red", linewidth=1, linestyle="dashed")
        ax.fill(angles, values, color="red", alpha=0.1)

    # Add a title
    plt.title(title, size=RADAR_PLOT_TITLE_FONT_SIZE, color=color, y=RADAR_PLOT_TITLE_Y_POSITION)
