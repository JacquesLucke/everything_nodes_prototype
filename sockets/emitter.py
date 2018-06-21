import bpy
from .. base_socket_types import RelationalSocket

class EmitterSocket(RelationalSocket, bpy.types.NodeSocket):
    bl_idname = "en_EmitterSocket"
    color = (1, 1, 1, 1)

    def draw(self, context, layout, node, text):
        layout.label(text)