from openhound.core.models.entries_dataclass import (
    Node as BaseNode,
    NodeProperties as BaseProperties,
    Edge,
    EdgePath,
    ConditionalEdgePath
)


from dataclasses import dataclass, field


@dataclass
class FakeNodeProperties(BaseProperties):
    tenant: str


@dataclass
class Node(BaseNode):
    properties: FakeNodeProperties
    kinds: list[str]
    id: str = field(init=False)

    @staticmethod
    def guid(name: str, node_type: str) -> str:
        return BaseNode.guid(name, node_type)


    def __post_init__(self):
        self.id = self.guid(self.properties.name, self.kinds[0])
