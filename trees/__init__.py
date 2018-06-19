import bpy
from . group import GroupNodeTree

tree_types = [
    GroupNodeTree
]

def register():
    for cls in tree_types:
        bpy.utils.register_class(cls)

def unregister():
    for cls in tree_types:
        bpy.utils.unregister_class(cls)