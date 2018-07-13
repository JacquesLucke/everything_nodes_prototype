import bpy

def draw_menu(self, context):
    tree = context.space_data.node_tree
    if True:
        return

    layout = self.layout
    layout.operator_context = "INVOKE_DEFAULT"

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