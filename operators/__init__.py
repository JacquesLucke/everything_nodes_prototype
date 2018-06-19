import bpy
from . execute_callback import ExecuteCallbackOperator
from . socket_type_chooser import ChooseSocketTypeOperator
from . analyse_tree import AnalyseTreeOperator

operators = [
    AnalyseTreeOperator,
    ExecuteCallbackOperator,
    ChooseSocketTypeOperator
]

def register():
    for cls in operators:
        bpy.utils.register_class(cls)

def unregister():
    for cls in operators:
        bpy.utils.unregister_class(cls)