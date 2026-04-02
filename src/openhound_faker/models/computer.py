from openhound_faker.main import app
from openhound_faker.graph import (
    Node,
    FakeNodeProperties,
    EdgePath,
    ConditionalEdgePath,
    Edge,
)
from openhound_faker.kinds import nodes as nk, edges as ek
from openhound.core.models.entries_dataclass import PropertyMatch, Operator
from openhound.core.asset import BaseAsset, EdgeDef, NodeDef
from dataclasses import dataclass, field


@dataclass
class ComputerProperties(FakeNodeProperties):
    hostname: str
    ip_address: str
    mac_address: str


@app.asset(
    description="Randomly generated computer resources, returns node and edges",
    node=NodeDef(kind=nk.COMPUTER, icon="computer", description="Computer", properties=ComputerProperties),
    edges=[
        EdgeDef(
            start=nk.COMPUTER,
            end=nk.COMPUTER,
            kind=ek.EXAMPLE,
            description="Binding DummyComputer to another DummyComputer",
        ),
    ],
)
class FakeComputer(BaseAsset):
    hostname: str
    ip_address: str
    mac_address: str

    @property
    def as_node(self):
        properties = ComputerProperties(
            name=self.hostname,
            displayname=self.hostname,
            hostname=self.hostname,
            tenant="abc",
            ip_address=self.ip_address,
            mac_address=self.mac_address,
            environmentid="sample_environment"
        )

        return Node(kinds=[nk.COMPUTER], properties=properties)

    @property
    def _example_edge(self):
        # node_id = self.as_node.id
        find_computers = self._lookup.find_computers("*")
        for computer in find_computers[:20]:
            match_property = PropertyMatch(key="hostname", value=computer[0])
            start = ConditionalEdgePath(match_by="property", kind="DummyComputer", property_matchers=[match_property])
            end = EdgePath(
                value=Node.guid(computer[0], nk.COMPUTER), match_by="id"
            )
            yield Edge(start=start, end=end, kind="ExampleReference")

    @property
    def edges(self):
        yield from self._example_edge
