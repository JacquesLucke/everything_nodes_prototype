import bpy

class GroupInfoPanel(bpy.types.Panel):
    bl_idname = "en_InfoPanel"
    bl_label = "Info"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "Everything Nodes"

    @classmethod
    def poll(cls, context):
        try: return context.space_data.tree_type == "en_GroupNodeTree"
        except: return False

    def draw(self, context):
        layout = self.layout
        tree = context.space_data.node_tree

        layout.label(str(tree.is_valid_function))
        if tree.is_valid_function:
            layout.label(str(tree.signature))

        layout.operator("en.analyse_tree")