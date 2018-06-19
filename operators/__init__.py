import bpy
from . execute_callback import ExecuteCallbackOperator
from . socket_type_chooser import ChooseSocketTypeOperator
from . analyse_tree import AnalyseTreeOperator
from . add_driver import AddDriverOperator

operators = [
    AnalyseTreeOperator,
    ExecuteCallbackOperator,
    ChooseSocketTypeOperator,
    AddDriverOperator
]

def register():
    for cls in operators:
        bpy.utils.register_class(cls)

def unregister():
    for cls in operators:
        bpy.utils.unregister_class(cls)