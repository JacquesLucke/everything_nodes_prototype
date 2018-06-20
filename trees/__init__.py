import bpy
from . data_flow_group import DataFlowGroupTree
from . actions_tree import ActionsTree

tree_types = [
    DataFlowGroupTree,
    ActionsTree
]

def register():
    for cls in tree_types:
        bpy.utils.register_class(cls)

def unregister():
    for cls in tree_types:
        bpy.utils.unregister_class(cls)