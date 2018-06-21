import bpy
from .. trees import ParticleSystemTree

class ParticlesPanel(bpy.types.Panel):
    bl_idname = "en_ParticlesPanel"
    bl_label = "Info"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "Everything Nodes"

    @classmethod
    def poll(cls, context):
        return isinstance(context.space_data.node_tree, ParticleSystemTree)

    def draw(self, context):
        layout = self.layout
        tree = context.space_data.node_tree

        layout.label("Test")

        layout.operator("en.simulate_particle_system")