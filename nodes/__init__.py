import bpy

node_classes = []

def register():
    for cls in node_classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in node_classes:
        bpy.utils.unregister_class(cls)