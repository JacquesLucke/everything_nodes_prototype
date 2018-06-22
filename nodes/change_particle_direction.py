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
        items = mode_items, update = ImperativeNode.refresh)

    keep_velocity = BoolProperty(name = "Keep Velocity", default = True)

    def create(self):
        self.new_input("en_ControlFlowSocket", "Previous")
        if self.mode == "SET":
            self.new_input("en_VectorSocket", "Direction", "direction")
        elif self.mode == "RANDOMIZE":
            self.new_input("en_FloatSocket", "Strength", "strength")
        self.new_output("en_ControlFlowSocket", "Next", "NEXT")

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
            yield "_rotation = mathutils.Euler([(random.random() - 0.5) * strength * math.pi * 2 for _ in range(3)])"
            yield "PARTICLE.velocity = _rotation.to_matrix() * PARTICLE.velocity"
        yield "NEXT"