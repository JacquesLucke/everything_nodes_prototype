import bpy

from . float import FloatSocket
from . vector import VectorSocket
from . object import ObjectSocket
from . emitter import EmitterSocket
from . boolean import BooleanSocket
from . control_flow import ControlFlowSocket

data_flow_socket_classes = [
    FloatSocket,
    VectorSocket,
    ObjectSocket,
    EmitterSocket,
    BooleanSocket
]

socket_classes = data_flow_socket_classes + [ControlFlowSocket]

def register():
    for cls in socket_classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in socket_classes:
        bpy.utils.unregister_class(cls)

def get_data_flow_socket_classes():
    return data_flow_socket_classes[:]