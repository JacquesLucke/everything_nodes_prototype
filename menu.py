import bpy
from . trees import DataFlowGroupTree

def draw_menu(self, context):
    if not isinstance(context.space_data.node_tree, DataFlowGroupTree):
        return

    layout = self.layout
    layout.operator_context = "INVOKE_DEFAULT"
    insertNode(layout, "en_GroupInputNode", "Group Input")
    insertNode(layout, "en_GroupOutputNode", "Group Output")
    layout.separator()
    insertNode(layout, "en_FloatMathNode", "Float Math")
    insertNode(layout, "en_CombineVectorNode", "Combine Vector")
    insertNode(layout, "en_SeparateVectorNode", "Separate Vector")
    insertNode(layout, "en_ObjectTransformsNode", "Object Transforms")
    insertNode(layout, "en_OffsetVectorWithObjectNode", "Offset Vector with Object")
    insertNode(layout, "en_GetObjectParentNode", "Get Object Parent")

def insertNode(layout, type, text, settings = {}, icon = "NONE"):
    operator = layout.operator("node.add_node", text = text, icon = icon)
    operator.type = type
    operator.use_transform = True
    for name, value in settings.items():
        item = operator.settings.add()
        item.name = name
        item.value = value
    return operator

def register():
    bpy.types.NODE_MT_add.append(draw_menu)

def unregister():
    bpy.types.NODE_MT_add.remove(draw_menu)