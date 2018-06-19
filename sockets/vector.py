import bpy
from bpy.props import *
from .. base_socket_types import DataFlowSocket

class VectorSocket(DataFlowSocket, bpy.types.NodeSocket):
    bl_idname = "en_VectorSocket"
    data_type = "Vector"
    color = (0, 0, 0, 1)

    value = FloatVectorProperty(name = "Value", default = [0.0, 0.0, 0.0], subtype = "XYZ")

    def draw_property(self, layout, text, node):
        layout.column(align = True).prop(self, "value", text = text)

    def get_value(self):
        return self.value