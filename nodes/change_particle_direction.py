import bpy
from bpy.props import *
from .. base_node_types import ImperativeNode

mode_items = [
    ("SET", "Set", ""),
    ("RANDOMIZE", "Randomize", "")
]

class ChangeParticleDirectionNode(ImperativeNode, bpy.types.Node):
    bl_idname = "en_ChangeParticleDirectionNode"
    bl_label = "Change Direction"

    mode = EnumProperty(name = "Mode", default = "RANDOMIZE",
        items = mode_items, update = ImperativeNode.code_changed)

    keep_velocity = BoolProperty(name = "Keep Velocity")

    def create(self):
        self.new_input("en_ControlFlowSocket", "Previous")
        self.new_input("en_VectorSocket", "Direction", "direction")
        self.new_output("en_ControlFlowSocket", "Next")

    def draw(self, layout):
        layout.prop(self, "mode", text = "")
        if self.mode == "SET":
            layout.prop(self, "keep_velocity")

    def get_code(self):
        if self.mode == "SET":
            if self.keep_velocity:
                yield "PARTICLE.velocity = direction.normalized() * PARTICLE.velocity.length"
            else:
                yield "PARTICLE.velocity = direction"
        elif self.mode == "RANDOMIZE":
            yield "PARTICLE.velocity.x += (random.random() - 0.5) * direction.x"
            yield "PARTICLE.velocity.y += (random.random() - 0.5) * direction.y"
            yield "PARTICLE.velocity.z += (random.random() - 0.5) * direction.z"