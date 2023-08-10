import matplotlib
import seaborn as sns

matplotlib.use("Agg")


def plot_normalized_distplot(data, save_path=None, **kwargs):
    """Plot a distribution."""
    sns_plot = sns.histplot(data)
    sns_plot.set(xlabel=kwargs["xlabel"], title=kwargs["title"])
    if save_path:
        sns_plot.figure.savefig(save_path)
