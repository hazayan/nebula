from typing import Optional, List

import pandas as pd
import matplotlib.dates as md
from matplotlib import pyplot as plt, ticker

from lib.lib_agent import agent_name, kubo_version, polkadot_version
from lib.lib_fmt import thousands_ticker_formatter


def plot_crawl_properties(df: pd.DataFrame, polkadot_clients: List[str]) -> plt.Figure:
    def get_client(agent_version: str) -> Optional[str]:
        a = polkadot_version(agent_version)
        if a is None:
            return None
        return a.client

    def get_version(agent_version: str) -> Optional[str]:
        a = polkadot_version(agent_version)
        if a is None:
            return None
        return a.version()

    df["client"] = df.apply(lambda row: get_client(row["agent_version"]), axis=1)
    df["version"] = df.apply(lambda row: get_version(row["agent_version"]), axis=1)

    group = df[df["client"].isin(polkadot_clients)] \
        .groupby(by=['crawl_id', 'started_at', 'client'], as_index=False) \
        .sum(numeric_only=True) \
        .sort_values(['started_at', 'count'], ascending=False)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=[15, 5], dpi=150)

    for name in sorted(group["client"].unique()):
        data = group[group["client"] == name]
        ax1.plot(data["started_at"], data["count"], label=name)

    ax1.set_ylim(0)
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Count")
    ax1.xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
    for tick in ax1.get_xticklabels():
        tick.set_rotation(20)
        tick.set_ha('right')
    ax1.legend(title="Agent Name")
    ax1.set_title("General Agent Versions")

    group = df[df["client"] == polkadot_clients[0]] \
        .groupby(by=['crawl_id', 'started_at', 'version'], as_index=False) \
        .sum(numeric_only=True) \
        .sort_values(['started_at', 'count'], ascending=False)

    # Find 10 most widely used agent versions
    filter_group = group \
        .groupby(by="version", as_index=False) \
        .mean(numeric_only=True) \
        .sort_values('count', ascending=False)
    filter_group = filter_group.head(10)

    for version in reversed(sorted(group["version"].unique())):
        if version not in set(filter_group["version"]):
            continue
        data = group[group["version"] == version].sort_values('started_at', ascending=False)
        ax2.plot(data["started_at"], data["count"], label=version)

    ax2.set_ylim(0)
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Count")
    ax2.xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
    for tick in ax2.get_xticklabels():
        tick.set_rotation(20)
        tick.set_ha('right')
    ax2.legend()
    # ax2.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: "%.1fk" % (x / 1000)))
    #
    ax2.set_title(f"Top 10 \"{polkadot_clients[0]}\" Versions")
    ax2.legend(handlelength=1.0, ncols=5)
    fig.set_tight_layout(True)

    return fig
