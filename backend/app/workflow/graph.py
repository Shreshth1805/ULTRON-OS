class WorkflowGraph:

    def __init__(self):

        self.nodes = {}

    def add(self, node):

        self.nodes[node.id] = node

    def get(self, node_id):

        return self.nodes[node_id]

    def ready_nodes(self):

        ready = []

        for node in self.nodes.values():

            if node.completed:

                continue

            ok = True

            for dep in node.depends_on:

                if not self.nodes[dep].completed:

                    ok = False

                    break

            if ok:

                ready.append(node)

        return ready