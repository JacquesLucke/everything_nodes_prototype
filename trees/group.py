import bpy
from . base import NodeTree

class GroupNodeTree(NodeTree, bpy.types.NodeTree):
    bl_idname = "en_GroupNodeTree"
    bl_icon = "OUTLINER_DATA_EMPTY"
    bl_label = "Group"

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

        return GroupSignature(inputs, outputs)

class GroupSignature:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

    def __repr__(self):
        in_names = [socket.data_type for socket in self.inputs]
        out_names = [socket.data_type for socket in self.outputs]
        return "<In: ({}), Out: ({})>".format(
            ", ".join(in_names), ", ".join(out_names)
        )

