import bpy
from bpy.props import *
from .. base_node_types import ImperativeNode

mode_items = [
    ("SET", "Set", ""),
    ("RANDOMIZE", "Randomize", "")
]

class ChangeParticleColorNode(ImperativeNode, bpy.types.Node):
    bl_idname = "en_ChangeParticleColorNode"
    bl_label = "Change Color"

    mode = EnumProperty(name = "Mode", default = "SET",
        items = mode_items, update = ImperativeNode.code_changed)

    def create(self):
        self.new_input("en_ControlFlowSocket", "Previous")
        self.new_input("en_ColorSocket", "Color", "color")
        self.new_output("en_ControlFlowSocket", "Next", "NEXT")

    def draw(self, layout):
        layout.prop(self, "mode", text = "")

    def get_code(self):
        if self.mode == "SET":
            yield "PARTICLE.color = color"
        elif self.mode == "RANDOMIZE":
            yield "PARTICLE.color.r += (random.random() - 0.5) * color.r"
            yield "PARTICLE.color.g += (random.random() - 0.5) * color.g"
            yield "PARTICLE.color.b += (random.random() - 0.5) * color.b"
        yield "NEXT"