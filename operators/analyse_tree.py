import bpy
from .. execution_code import generate_function_code, get_new_socket_name

class AnalyseTreeOperator(bpy.types.Operator):
    bl_idname = "en.analyse_tree"
    bl_label = "Analyse Tree"

    def execute(self, context):
        tree = context.space_data.node_tree
        graph =  tree.graph

        input_node = tree.input_node
        output_node = tree.output_node

        variables = {}

        if input_node is not None:
            for i, socket in enumerate(input_node.outputs):
                variables[socket] = "input_" + str(i)

        for line in generate_function_code(graph, list(output_node.inputs), variables, generate_code_for_unlinked_input):
            print("    " + line)

        return {"FINISHED"}

def generate_code_for_unlinked_input(graph, socket, variables):
    name = get_new_socket_name(graph, socket)
    node = graph.get_node_by_socket(socket)
    variables[socket] = name
    yield "{} = bpy.data.node_groups['{}'].nodes['{}'].inputs[{}].get_value()".format(
        name, socket.id_data.name, node.name, socket.get_index(node)
    )
