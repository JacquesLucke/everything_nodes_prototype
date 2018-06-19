import bpy
from .. execution_code import generate_function_code, get_new_socket_name
from .. contexts.driver import evaluate_drivers

class AnalyseTreeOperator(bpy.types.Operator):
    bl_idname = "en.analyse_tree"
    bl_label = "Analyse Tree"

    def execute(self, context):
        tree = context.space_data.node_tree
        evaluate_drivers()

        return {"FINISHED"}

