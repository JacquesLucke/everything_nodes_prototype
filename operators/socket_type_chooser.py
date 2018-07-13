import bpy
from bpy.props import *
from .. callback import execute_callback

class ChooseSocketTypeOperator(bpy.types.Operator):
    bl_idname = "en.choose_socket_type"
    bl_label = "Choose Socket Type"
    bl_property = "selected_data_type"

    def get_items(self, context):
        items = []
        return items

    selected_data_type = EnumProperty(items = get_items)
    callback = StringProperty()

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"CANCELLED"}

    def execute(self, context):
        execute_callback(self.callback, self.selected_data_type)
        return {"FINISHED"}