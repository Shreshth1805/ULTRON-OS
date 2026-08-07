from dataclasses import dataclass, field
from typing import Dict, List, Set
from collections import defaultdict


@dataclass
class Node:

    id: str

    type: str

    properties: Dict = field(default_factory=dict)


@dataclass
class Edge:

    source: str

    relation: str

    target: str


class KnowledgeGraph:
    """
    ULTRON Knowledge Graph

    Stores relationships between:

    • Projects
    • Files
    • Agents
    • Technologies
    • Users
    • Libraries
    • APIs
    • Models
    • Bugs
    • Fixes
    """

    def __init__(self):

        self.nodes: Dict[str, Node] = {}

        self.edges: List[Edge] = []

        self.graph = defaultdict(set)

    # =====================================================
    # Add Node
    # =====================================================

    def add_node(

        self,

        node_id: str,

        node_type: str,

        **properties

    ):

        if node_id not in self.nodes:

            self.nodes[node_id] = Node(

                id=node_id,

                type=node_type,

                properties=properties

            )

        else:

            self.nodes[node_id].properties.update(

                properties

            )

        return self.nodes[node_id]

    # =====================================================
    # Add Edge
    # =====================================================

    def add_edge(

        self,

        source: str,

        relation: str,

        target: str

    ):

        self.edges.append(

            Edge(

                source,

                relation,

                target

            )

        )

        self.graph[source].add(target)

    # =====================================================
    # Get Node
    # =====================================================

    def get_node(

        self,

        node_id: str

    ):

        return self.nodes.get(node_id)

    # =====================================================
    # Neighbors
    # =====================================================

    def neighbors(

        self,

        node_id: str

    ):

        return [

            self.nodes[n]

            for n in self.graph.get(

                node_id,

                []

            )

            if n in self.nodes

        ]

    # =====================================================
    # Incoming Edges
    # =====================================================

    def incoming(

        self,

        node_id: str

    ):

        return [

            edge

            for edge in self.edges

            if edge.target == node_id

        ]

    # =====================================================
    # Outgoing Edges
    # =====================================================

    def outgoing(

        self,

        node_id: str

    ):

        return [

            edge

            for edge in self.edges

            if edge.source == node_id

        ]

    # =====================================================
    # Find by Type
    # =====================================================

    def find_type(

        self,

        node_type: str

    ):

        return [

            node

            for node in self.nodes.values()

            if node.type == node_type

        ]

    # =====================================================
    # Search
    # =====================================================

    def search(

        self,

        keyword: str

    ):

        keyword = keyword.lower()

        results = []

        for node in self.nodes.values():

            if keyword in node.id.lower():

                results.append(node)

                continue

            for value in node.properties.values():

                if keyword in str(value).lower():

                    results.append(node)

                    break

        return results

    # =====================================================
    # Connected Components
    # =====================================================

    def connected(

        self,

        node_id: str

    ) -> Set[str]:

        visited = set()

        stack = [node_id]

        while stack:

            current = stack.pop()

            if current in visited:

                continue

            visited.add(current)

            stack.extend(

                self.graph.get(

                    current,

                    []

                )

            )

        return visited

    # =====================================================
    # Statistics
    # =====================================================

    def stats(self):

        return {

            "nodes": len(self.nodes),

            "edges": len(self.edges)

        }

    # =====================================================
    # Clear
    # =====================================================

    def clear(self):

        self.nodes.clear()

        self.edges.clear()

        self.graph.clear()


knowledge_graph = KnowledgeGraph()