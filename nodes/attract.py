import bpy
from bpy.props import *
from . particle_force_base import ParticleForceNode

class AttractNode(ParticleForceNode, bpy.types.Node):
    bl_idname = "en_AttractNode"
    bl_label = "Attract"

    attractor = PointerProperty(type = bpy.types.Object)

    def create(self):
        self.new_input("en_FloatSocket", "Strength", "strength")
        self.new_output("en_ParticleModifierSocket", "Force")

    def draw(self, layout):
        layout.prop(self, "attractor", text = "")

    def get_force_code(self):
        yield "if self.attractor is None:"
        yield "    FORCE = mathutils.Vector((0, 0, 0))"
        yield "else:"
        yield "    _difference = self.attractor.location - LOCATION"
        yield "    _distance = _difference.length"
        yield "    FORCE = _difference.normalized() / _distance ** 2 * strength if _distance > 0 else mathutils.Vector((0, 0, 0))"