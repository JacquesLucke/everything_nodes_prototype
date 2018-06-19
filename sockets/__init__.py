import bpy

from . float import FloatSocket
from . vector import VectorSocket
from . object import ObjectSocket

socket_classes = [
    FloatSocket,
    VectorSocket,
    ObjectSocket
]

def register():
    for cls in socket_classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in socket_classes:
        bpy.utils.unregister_class(cls)

def get_socket_classes():
    return socket_classes[:]