import bpy
from bpy.props import *
from . particle_event_trigger_base import ParticleEventTriggerNode

mode_items = [
    ("AGE_REACHED", "Age Reached", ""),
    ("INTERVAL", "Interval", "")
]

class ParticleAgeTriggerNode(ParticleEventTriggerNode, bpy.types.Node):
    bl_idname = "en_ParticleAgeTriggerNode"
    bl_label = "Age Trigger"

    def mode_changed(self, context = None):
        if len(self.inputs) == 2:
            self.inputs.remove(self.inputs[1])

        if self.mode == "AGE_REACHED":
            self.new_input("en_FloatSocket", "Age", "trigger_age")
        elif self.mode == "INTERVAL":
            self.new_input("en_FloatSocket", "Interval", "interval")

    mode = EnumProperty(name = "Mode", default = "AGE_REACHED",
        update = mode_changed,
        items = mode_items)

    def create(self):
        self.new_input("en_ParticleTypeSocket", "Particle Type")
        self.new_output("en_ControlFlowSocket", "Next")
        self.mode_changed()

    def draw(self, layout):
        layout.prop(self, "mode", text = "")

    def get_trigger_code(self):
        yield "_age = CURRENT_TIME - PARTICLE.born_time"
        if self.mode == "AGE_REACHED":
            yield "TRIGGERED = _age >= trigger_age and _age - TIME_STEP < trigger_age"
        elif self.mode == "INTERVAL":
            yield "TRIGGERED = _age // interval > (_age - TIME_STEP) // interval"