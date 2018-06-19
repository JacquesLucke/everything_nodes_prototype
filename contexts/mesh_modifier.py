import bpy
from bpy.props import *
from .. trees import DataFlowGroupTree

class NodeMeshModifier(bpy.types.PropertyGroup):
    def is_function(self, tree):
        return isinstance(tree, DataFloatGroupTree) and tree.is_valid_function

    enabled = BoolProperty(name = "Enabled", default = False)
    data_flow_group = PointerProperty(type = bpy.types.NodeTree, poll = is_function)

property_groups = [
    NodeMeshModifier
]

def register():
    for cls in property_groups:
        bpy.utils.register_class(cls)
    bpy.types.Mesh.node_modifier = PointerProperty(type = NodeMeshModifier)

def unregister():
    del bpy.types.Mesh.node_modifier
    for cls in property_groups:
        bpy.utils.unregister_class(cls)