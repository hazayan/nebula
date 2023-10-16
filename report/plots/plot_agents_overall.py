import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker
from lib.lib_agent import agent_name, kubo_version
from lib.lib_fmt import fmt_thousands


def plot_agents_overall(df: pd.DataFrame) -> plt.Figure:
    df = df.copy() \
        .groupby(by=["client"], as_index=False) \
        .sum(numeric_only=True) \
        .sort_values(["count"], ascending=False) \
        .reset_index(drop=True)

    result = df.nlargest(10, columns="count")
    other_count = df.loc[~df["client"].isin(result["client"]), "count"].sum()

    if other_count > 0:
        result.loc[len(result)] = ['Rest', 0, other_count]

    df = result

    total = df['count'].sum()

    fig, ax = plt.subplots(figsize=[10, 5], dpi=150)

    p1 = ax.barh(df["client"], df["count"])
    ax.set_yticks(df["client"], labels=[client for client in df["client"]])
    ax.set_xlabel("Count")
    ax.set_ylabel("Client")

    ax.bar_label(p1, padding=6, labels=["%.1f%%" % (100 * val / total) for val in df["count"]])

    ax.set_title(f"Clients (Total Peers {fmt_thousands(total)})")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.invert_yaxis()
    fig.set_tight_layout(True)

    return fig
