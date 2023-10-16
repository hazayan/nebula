from distutils.version import StrictVersion
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker
from lib.lib_fmt import fmt_thousands


def plot_agents_polkadot_clients(df: pd.DataFrame, client: str):
    df = df.copy()

    df = df[df["client"] == client]

    df = df \
        .groupby(by=["version"], as_index=False) \
        .sum(numeric_only=True) \
        .reset_index(drop=True)

    df['version_sort'] = df['version'].apply(StrictVersion)
    df.sort_values(by='version_sort', ascending=False)
    total = df['count'].sum()

    fig, ax = plt.subplots(figsize=[10, 5], dpi=150)

    p1 = ax.barh(df["version"], df["count"])
    ax.set_yticks(df["version"], labels=[version for version in df["version"]])
    ax.set_xlabel("Count")
    ax.set_ylabel(f"\"{client}\" Client")

    ax.bar_label(p1, padding=6, labels=["%.1f%%" % (100 * val / total) for val in df["count"]])

    ax.set_title(f"\"{client}\" Clients (Total Peers {fmt_thousands(total)})")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    fig.set_tight_layout(True)

    return fig
