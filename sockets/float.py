import bpy
from bpy.props import *
from .. base_socket_types import InternalDataFlowSocket

class FloatSocket(InternalDataFlowSocket, bpy.types.NodeSocket):
    bl_idname = "en_FloatSocket"
    data_type = "Float"
    color = (0, 0, 0, 1)

    value = FloatProperty(name = "Value", default = 0.0)

    def draw_property(self, layout, text, node):
        layout.prop(self, "value", text = text)

    def get_value(self):
        return self.value