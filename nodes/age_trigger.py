import bpy
from . particle_event_trigger_base import ParticleEventTriggerNode

class ParticleAgeTriggerNode(ParticleEventTriggerNode, bpy.types.Node):
    bl_idname = "en_ParticleAgeTriggerNode"
    bl_label = "Age Trigger"

    def create(self):
        self.new_input("en_ParticleTypeSocket", "Particle Type")
        self.new_input("en_FloatSocket", "Age", "trigger_age")
        self.new_output("en_ControlFlowSocket", "Next")

    def get_trigger_code(self):
        yield "_age = CURRENT_TIME - PARTICLE.born_time"
        yield "TRIGGERED = _age >= trigger_age and _age - TIME_STEP < trigger_age"