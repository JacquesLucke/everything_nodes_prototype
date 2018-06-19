import bpy
from pprint import pprint
from .. execution_code import generate_function_code, get_new_socket_name
from .. contexts.driver import evaluate_drivers
from .. trees.data_flow_group import find_possible_external_values, find_dependencies

class AnalyseTreeOperator(bpy.types.Operator):
    bl_idname = "en.analyse_tree"
    bl_label = "Analyse Tree"

    def execute(self, context):
        tree = context.space_data.node_tree
        evaluate_drivers()

        values = {}
        values[tree.signature.inputs[0]] = {context.active_object}
        find_possible_external_values(tree.graph, values)

        print()
        pprint(values)

        deps = find_dependencies(tree.graph, values, tree.signature.inputs, tree.signature.outputs)
        pprint(deps)
        return {"FINISHED"}

