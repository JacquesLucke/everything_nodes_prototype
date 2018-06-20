import bpy
from . execute_callback import ExecuteCallbackOperator
from . socket_type_chooser import ChooseSocketTypeOperator
from . analyse_tree import AnalyseTreeOperator
from . add_driver import AddDriverOperator
from . modal_runner import ModalRunnerOperator
from . print_driver_dependencies import PrintDriverDependenciesOperator
from . start_interactive_mode import StartInteractiveModeOperator

operators = [
    AnalyseTreeOperator,
    ExecuteCallbackOperator,
    ChooseSocketTypeOperator,
    AddDriverOperator,
    ModalRunnerOperator,
    PrintDriverDependenciesOperator,
    StartInteractiveModeOperator
]

def register():
    for cls in operators:
        bpy.utils.register_class(cls)

def unregister():
    for cls in operators:
        bpy.utils.unregister_class(cls)