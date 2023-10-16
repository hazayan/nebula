import dataclasses
import re
from typing import Optional

known_agents = [
    "go-ipfs",
    "kubo",
    "hydra-booster",
    "storm",
    "ioi",
    "iroh"
]


def agent_name(agent_version) -> str:
    if agent_version == "go-ipfs/0.8.0/48f94e2":
        return "storm*"

    for agent in known_agents:
        if agent_version.startswith(agent):
            if agent == "go-ipfs":
                return "kubo"
            return agent
    return "other"


def kubo_version(agent_version) -> Optional[str]:
    if agent_version == "go-ipfs/0.8.0/48f94e2":
        return None

    match = re.match(r"(go-ipfs|kubo)\/(\d+\.+\d+\.\d+)(.*)?\/", agent_version)
    if match is None:
        return None

    return match.group(2)


@dataclasses.dataclass
class Agent:
    client: str
    major: int
    minor: int
    patch: int

    def version(self):
        return f"{self.major}.{self.minor}.{self.patch}"


def polkadot_version(agent_version) -> Optional[Agent]:
    match = re.match(r"(?P<client>.*)\/v(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*).*",
                     agent_version)
    if match is None:
        return None

    return Agent(
        match.group("client"),
        match.group("major"),
        match.group("minor"),
        match.group("patch"),
    )

