import bpy
from .. base_node_types import ImperativeNode

class MoveObjectNode(ImperativeNode, bpy.types.Node):
    bl_idname = "en_MoveObjectNode"
    bl_label = "Move Object"

    def create(self):
        self.new_input("en_ControlFlowSocket", "Previous")
        self.new_input("en_ObjectSocket", "Object", "object")
        self.new_input("en_VectorSocket", "Offset", "offset")

        self.new_output("en_ControlFlowSocket", "Next", "NEXT")

    def get_code(self):
        yield "if object is not None:"
        yield "    object.location += offset"
        yield "NEXT"