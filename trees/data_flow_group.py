import bpy
from . base import NodeTree
from .. execution_code import generate_function_code, get_new_socket_name

function_by_tree = {}

class DataFlowGroupTree(NodeTree, bpy.types.NodeTree):
    bl_idname = "en_DataFlowGroupTree"
    bl_icon = "MOD_DATA_TRANSFER"
    bl_label = "Data Flow Group"

    def update(self):
        super().update()
        self.update_function()

    @property
    def is_valid_function(self):
        if self.graph.count_idname("en_GroupInputNode") > 1:
            return False
        if self.graph.count_idname("en_GroupOutputNode") != 1:
            return False
        return True

    @property
    def input_node(self):
        nodes = self.graph.get_nodes_by_idname("en_GroupInputNode")
        if len(nodes) == 0:
            return None
        elif len(nodes) == 1:
            return nodes[0]
        else:
            raise Exception("there is more than one input node")

    @property
    def output_node(self):
        nodes = self.graph.get_nodes_by_idname("en_GroupOutputNode")
        if len(nodes) == 0:
            return None
        elif len(nodes) == 1:
            return nodes[0]
        else:
            raise Exception("there is more than one output node")

    @property
    def signature(self):
        input_node = self.input_node
        if input_node is None:
            inputs = []
        else:
            inputs = list(input_node.outputs)

        outputs = list(self.output_node.inputs)

        return FunctionSignature(inputs, outputs)

    @property
    def function(self):
        if not self.is_valid_function:
            raise Exception("the node tree is in an invalid state")
        if self not in function_by_tree:
            self.update_function()
        return function_by_tree[self]

    def update_function(self):
        function_by_tree[self] = generate_function(self)

class FunctionSignature:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

    def __repr__(self):
        in_names = [socket.data_type for socket in self.inputs]
        out_names = [socket.data_type for socket in self.outputs]
        return "<In: ({}), Out: ({})>".format(
            ", ".join(in_names), ", ".join(out_names)
        )

    def match_input(self, pattern):
        if len(pattern) != len(self.inputs):
            return False
        return all(s.data_type == t for s, t in zip(self.inputs, pattern))

    def match_output(self, pattern):
        if len(pattern) != len(self.outputs):
            return False
        return all(s.data_type == t for s, t in zip(self.outputs, pattern))

def generate_function(tree):
    code = "\n".join(iter_function_lines(tree))
    container = {}
    exec(code, container, container)
    return container["main"]

def iter_function_lines(tree):
    yield "import bpy, mathutils"
    signature = tree.signature

    variables = {}
    for i, socket in enumerate(signature.inputs):
        variables[socket] = "input_" + str(i)

    input_string = ", ".join(variables[socket] for socket in signature.inputs)
    yield f"def main({input_string}):"

    for line in generate_function_code(tree.graph, signature.outputs, variables, generate_code_for_unlinked_input):
        yield "    " + line

    output_string = ", ".join(variables[socket] for socket in signature.outputs)
    yield "    return " + output_string

def generate_code_for_unlinked_input(graph, socket, variables):
    name = get_new_socket_name(graph, socket)
    node = graph.get_node_by_socket(socket)
    variables[socket] = name
    yield "{} = bpy.data.node_groups['{}'].nodes['{}'].inputs[{}].get_value()".format(
        name, socket.id_data.name, node.name, socket.get_index(node)
    )
