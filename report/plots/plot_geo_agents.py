from typing import Optional, List

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from lib.lib_agent import polkadot_version
from lib.lib_fmt import fmt_thousands, fmt_barplot


def plot_geo_agents(df: pd.DataFrame, countries: pd.DataFrame, polkadot_clients: List[str]) -> plt.Figure:
    def get_client(agent_version: str) -> Optional[str]:
        agent = polkadot_version(agent_version)
        if agent is None:
            return None
        return agent.client

    df["client"] = df.apply(lambda row: get_client(row["agent_version"]), axis=1)

    fig, axs = plt.subplots((len(polkadot_clients) + 2) // 3, 3, figsize=(15, 9))
    for idx, client in enumerate(polkadot_clients):
        ax = fig.axes[idx]

        data = countries[countries["peer_id"].isin(df[df['client'] == client]["peer_id"])]
        data = data.groupby(by="country", as_index=False).count().sort_values('peer_id', ascending=False)
        data = data.rename(columns={'peer_id': 'count'})

        result = data.nlargest(8, columns="count")
        other_count = data.loc[~data["country"].isin(result["country"]), "count"].sum()

        if other_count > 0:
            result.loc[len(result)] = ['Rest', other_count]

        sns.barplot(ax=ax, x="country", y="count", data=result)
        fmt_barplot(ax, result["count"], result["count"].sum())
        ax.set_xlabel("")
        ax.title.set_text(f"{client} (Total {fmt_thousands(data['count'].sum())})")

    fig.suptitle(f"Country Distributions of all Resolved Peer IDs by Agent Version")
    fig.set_tight_layout(True)

    if len(polkadot_clients) < len(fig.axes):
        for ax in fig.axes[len(polkadot_clients):]:
            fig.delaxes(ax)

    return fig
