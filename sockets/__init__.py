import bpy

socket_classes = []

def register():
    for cls in socket_classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in socket_classes:
        bpy.utils.unregister_class(cls)