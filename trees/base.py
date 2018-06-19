from .. node_parser import NodeGraph

graph_by_tree = {}

class NodeTree:
    def update(self):
        self.update_graph()

    @property
    def graph(self):
        if self not in graph_by_tree:
            self.update_graph()
        return graph_by_tree[self]

    def update_graph(self):
        graph_by_tree[self] = NodeGraph.from_node_tree(self)