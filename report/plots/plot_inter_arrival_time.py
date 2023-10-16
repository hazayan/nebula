from typing import Optional

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt, ticker

from lib.lib_agent import polkadot_version
from lib.lib_fmt import fmt_thousands
from lib.lib_plot import cdf


def configure_axis(ax):
    ax.set_xlim(0, 48)
    ax.set_xticks(np.arange(0, 50, step=2))
    ax.set_xlabel("Inter-Arrival Time in Hours")


def plot_inter_arrival_time(df: pd.DataFrame) -> plt.Figure:
    df = df.assign(inter_arrival_time_in_h=df.inter_arrival_time.apply(lambda x: x.total_seconds() / 3600))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), sharey=True)

    # First plot
    data = cdf(df["inter_arrival_time_in_h"])
    ax1.plot(data["inter_arrival_time_in_h"], data["cdf"])
    ax1.legend(loc='lower right', labels=[f"all ({fmt_thousands(len(df))})"])
    ax1.set_title("Overall")
    ax1.set_ylabel("Online Peers in %")
    ax2.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: "%d" % int(x * 100)))
    configure_axis(ax1)

    df = df.dropna()

    def get_client(agent_version: str) -> Optional[str]:
        agent = polkadot_version(agent_version)
        if agent is None:
            return None
        return agent.client

    df["client"] = df.apply(lambda row: get_client(row["agent_version"]), axis=1)

    # Second plot
    for agent in list(df["client"].unique()) + ['other']:
        data = df[df['client'] == agent]
        data = cdf(data["inter_arrival_time_in_h"])
        ax2.plot(data["inter_arrival_time_in_h"], data["cdf"], label=f"{agent} ({fmt_thousands(len(data))})")

    ax2.legend(loc='lower right')
    ax2.set_title("By Agent")
    configure_axis(ax2)

    fig.set_tight_layout(True)

    return fig
