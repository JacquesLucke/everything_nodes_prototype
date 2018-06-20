import bpy
from . base import NodeTree
from .. base_socket_types import DataFlowSocket, ControlFlowBaseSocket

class ActionsTree(NodeTree, bpy.types.NodeTree):
    bl_idname = "en_ActionsTree"
    bl_icon = "PMARKER_ACT"
    bl_label = "Actions"

    def internal_data_socket_changed(self):
        pass

    def external_data_socket_changed(self):
        pass

    def print_event_code(self):
        for node in self.get_event_nodes():
            generate_action(self, node.outputs[0])

    def handle_event(self, event):
        if event.value == "PRESS":
            for node in self.graph.get_nodes_by_idname("en_KeyPressEventNode"):
                if event.type == node.key_type.upper():
                    generate_action(self, node.outputs[0])()

            for node in self.graph.get_nodes_by_idname("en_MouseClickEventNode"):
                if event.type == node.mouse_button:
                    generate_action(self, node.outputs[0])()

        if event.type == "TIMER":
            for node in self.graph.get_nodes_by_idname("en_OnUpdateEventNode"):
                generate_action(self, node.outputs[0])()


def generate_action(tree, start_socket):
    code = "\n".join(iter_action_lines(tree, start_socket))
    container = {}
    exec(code, container, container)
    return container["main"]

def iter_action_lines(tree, start_socket):
    yield "import bpy, mathutils"
    yield f"nodes = bpy.data.node_groups[{repr(tree.name)}].nodes"

    yield "def main():"
    yield "    pass"
    for line in generate_action_code(tree.graph, start_socket):
        yield "    " + line

from . data_flow_group import (
    generate_function_code,
    generate_code_for_unlinked_input,
    generate_self_expression,
    find_required_sockets,
    replace_variable_name
)

def generate_action_code(graph, socket):
    if socket.is_output:
        linked_sockets = graph.get_linked_sockets(socket)
        if len(linked_sockets) == 1:
            yield from generate_action_code(graph, next(iter(linked_sockets)))
    else:
        node = graph.get_node_by_socket(socket)

        yield ""
        yield "#"
        yield "# " + repr(node.name)
        yield "#"

        sockets_to_calculate = {s for s in node.inputs if isinstance(s, DataFlowSocket)}
        required_sockets = find_required_sockets(graph, set(), sockets_to_calculate)
        variables = dict()
        yield from generate_function_code(graph, sockets_to_calculate, required_sockets, variables,
                generate_code_for_unlinked_input, generate_self_expression)

        yield ""
        yield "# Execute actual node"

        control_outputs = {s.identifier : s for s in node.outputs if isinstance(s, ControlFlowBaseSocket)}

        for line in node.get_code():
            for identifer, out_socket in control_outputs.items():
                if identifer in line:
                    indentation = " " * line.index(identifer)
                    yield indentation + "pass"
                    for next_line in generate_action_code(graph, out_socket):
                        yield indentation + next_line
                    break
            else:
                for socket in node.sockets:
                    if isinstance(socket, DataFlowSocket):
                        line = replace_variable_name(line, socket.identifier, variables[socket])
                line = replace_variable_name(line, "self", generate_self_expression(graph, node))
                yield line
