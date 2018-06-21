import bpy
import time
import traceback
from bgl import *
from bpy.props import *
from .. trees import ParticleSystemTree
from .. trees.particle_system import ParticleSystemState, simulate_step


class SimulateParticleSystemOperator(bpy.types.Operator):
    bl_idname = "en.simulate_particle_system"
    bl_label = "Simulate Particle System"

    @classmethod
    def poll(cls, context):
        return isinstance(context.space_data.node_tree, ParticleSystemTree)

    def invoke(self, context, event):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.016, context.window)
        wm.modal_handler_add(self)

        self.draw_handler = bpy.types.SpaceView3D.draw_handler_add(
                self.draw_callback, tuple(), "WINDOW", "POST_VIEW")

        tree = context.space_data.node_tree
        self.state = ParticleSystemState()
        self.particle_system = tree.get_particle_system()
        self.last_time = time.perf_counter()

        self.is_pause = False

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if not self.is_pause:
            if event.type == "TIMER":
                current_time = time.perf_counter()
                time_step = current_time - self.last_time
                try:
                    simulate_step(self.particle_system, self.state, current_time, time_step)
                except Exception as e:
                    self.finish()
                    traceback.print_exc()
                    return {"CANCELLED"}
                self.last_time = current_time

            for area in context.screen.areas:
                area.tag_redraw()

        if event.type == "SPACE" and event.value == "PRESS":
            self.is_pause = not self.is_pause
            self.last_time = time.perf_counter()
            return {"RUNNING_MODAL"}

        if event.type == "ESC":
            self.finish(context)
            return {"CANCELLED"}

        return {"PASS_THROUGH"}

    def finish(self, context):
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, "WINDOW")
        context.window_manager.event_timer_remove(self._timer)

    def draw_callback(self):
        glPointSize(2)
        glEnable(GL_POINT_SMOOTH)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)

        glBegin(GL_POINTS)
        for particle_type, particles in self.state.particles_by_type.items():
            for particle in particles:
                glColor3f(*particle.color)
                glVertex3f(*particle.location)
        glEnd()

        glDisable(GL_POINT_SMOOTH)