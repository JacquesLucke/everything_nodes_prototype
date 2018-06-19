import bpy
from bpy.props import *
from .. base_socket_types import ExternalDataFlowSocket

class ObjectSocket(ExternalDataFlowSocket, bpy.types.NodeSocket):
    bl_idname = "en_ObjectSocket"
    data_type = "Object"
    color = (0, 0, 0, 1)

    value = PointerProperty(type = bpy.types.Object)

    def draw_property(self, layout, text, node):
        layout.prop(self, "value", text = text)

    def get_value(self):
        return self.value