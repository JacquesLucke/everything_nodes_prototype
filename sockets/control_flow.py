import bpy
from .. base_socket_types import Socket

class ControlFlowSocket(Socket, bpy.types.NodeSocket):
    bl_idname = "en_ControlFlowSocket"
    color = (0, 1, 0, 1)

    def draw(self, context, layout, node, text):
        layout.label(text)