from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from lib.lib_agent import agent_name, polkadot_version
from lib.lib_fmt import fmt_thousands


def plot_agents_classification(agents):
    fig, axs = plt.subplots(2, 2, figsize=[15, 8], dpi=150)

    for idx, node_class in enumerate(sorted(agents.keys())):
        ax = fig.axes[idx]

        df = agents[node_class]

        def get_client(agent_version: str) -> Optional[str]:
            a = polkadot_version(agent_version)
            if a is None:
                return None
            return a.client

        df["client"] = df.apply(lambda row: get_client(row.agent_version), axis=1)

        agent_names_df = df \
            .groupby(by=["client"], as_index=False) \
            .sum(numeric_only=True) \
            .sort_values('count', ascending=False)
        agent_names_total = agent_names_df["count"].sum()

        result = agent_names_df.nlargest(10, columns="count")
        other_count = agent_names_df.loc[~agent_names_df["client"].isin(result["client"]), "count"].sum()

        if other_count > 0:
            result.loc[len(result)] = ['Rest', 0, other_count]

        agent_names_df = result

        bar = ax.barh(agent_names_df["client"], agent_names_df["count"])
        ax.bar_label(bar, padding=4,
                     labels=["%.1f%%" % (100 * val / agent_names_total) for val in agent_names_df["count"]])

        ax.set_xlabel("Count")
        ax.set_title(f"{node_class.lower()} (Total Peers {fmt_thousands(agent_names_total)})")
        ax.invert_yaxis()

    fig.suptitle(f"Agent Type By Classification")

    fig.set_tight_layout(True)

    if len(agents.keys()) < len(fig.axes):
        for ax in fig.axes[len(agents.keys()):]:
            fig.delaxes(ax)

    return fig
