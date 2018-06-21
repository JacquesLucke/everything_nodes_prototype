import bpy
from . base import NodeTree
from mathutils import Vector
from collections import defaultdict
from .. utils.code import code_to_function
from . actions_tree import generate_action_code
from .. base_socket_types import DataFlowSocket
from .. nodes.particle_force_base import ParticleForceNode
from .. nodes.particle_emitter_base import ParticleEmitterNode
from .. nodes.particle_event_trigger_base import ParticleEventTriggerNode

from . data_flow_group import (
    iter_import_lines,
    generate_function_code,
    replace_local_identifiers
)

class ParticleSystemTree(NodeTree, bpy.types.NodeTree):
    bl_idname = "en_ParticleSystemTree"
    bl_icon = "PARTICLES"
    bl_label = "Particle System"

    def internal_data_socket_changed(self):
        pass

    def external_data_socket_changed(self):
        pass

    def get_particle_system(self):
        particle_types = []
        for node in self.graph.get_nodes_by_idname("en_ParticleTypeNode"):
            emitters = get_emitter_nodes_for_particle_node(self.graph, node)
            emitter_function = get_emitter_function(self, emitters)

            forces = get_force_nodes_for_particle_node(self.graph, node)
            forces_function = get_forces_function(self, forces)

            event_triggers = get_event_trigger_nodes_for_particle_node(self.graph, node)
            event_function = get_events_function(self, event_triggers)

            particle_type = ParticleType(emitter_function, forces_function, event_function)
            particle_types.append(particle_type)
        return ParticleSystem(particle_types)


# Emitters
###########################################

def get_emitter_nodes_for_particle_node(graph, node):
    emitters = set()
    for socket in graph.get_linked_sockets(node.inputs["Emitter"]):
        linked_node = graph.get_node_by_socket(socket)
        if isinstance(linked_node, ParticleEmitterNode):
            emitters.add(linked_node)
    return emitters

@code_to_function()
def get_emitter_function(tree, emitters):
    graph = tree.graph
    yield from iter_import_lines(tree)
    yield "from everything_nodes_prototype.trees.particle_system import Particle as NEW_PARTICLE"
    yield "def main(CURRENT_TIME, TIME_STEP):"

    sockets_to_calculate = get_data_flow_inputs(emitters)

    variables = {}
    for line in generate_function_code(graph, sockets_to_calculate, variables):
        yield "    " + line

    yield "    ALL_NEW_PARTICLES = []"
    for emitter in emitters:
        inputs = get_data_flow_inputs(emitter)
        for line in emitter.get_emit_code():
            yield "    " + replace_local_identifiers(line, emitter, inputs, variables)

        yield "    ALL_NEW_PARTICLES.extend(EMITTED)"
    yield "    return ALL_NEW_PARTICLES"


# Forces
###########################################

def get_force_nodes_for_particle_node(graph, node):
    forces = set()
    for socket in graph.get_linked_sockets(node.inputs["Modifiers"]):
        linked_node = graph.get_node_by_socket(socket)
        if isinstance(linked_node, ParticleForceNode):
            forces.add(linked_node)
    return forces

@code_to_function()
def get_forces_function(tree, forces):
    graph = tree.graph
    yield from iter_import_lines(tree)
    yield "def main(LOCATION):"

    sockets_to_calculate = get_data_flow_inputs(forces)
    variables = {}
    for line in generate_function_code(graph, sockets_to_calculate, variables):
        yield "    " + line

    yield "    ALL_FORCES = mathutils.Vector((0, 0, 0))"
    for force in forces:
        inputs = get_data_flow_inputs(force)
        for line in force.get_force_code():
            yield "    " + replace_local_identifiers(line, force, inputs, variables)
        yield "    ALL_FORCES += FORCE"
    yield "    return ALL_FORCES"


# Events
##############################################

def get_event_trigger_nodes_for_particle_node(graph, node):
    event_triggers = set()
    for socket in graph.get_linked_sockets(node.outputs["Particle Type"]):
        linked_node = graph.get_node_by_socket(socket)
        if isinstance(linked_node, ParticleEventTriggerNode):
            event_triggers.add(linked_node)
    return event_triggers

@code_to_function()
def get_events_function(tree, event_triggers):
    graph = tree.graph
    yield from iter_import_lines(tree)
    yield "def main(PARTICLE, CURRENT_TIME, TIME_STEP):"
    yield "    pass"

    sockets_to_calculate = get_data_flow_inputs(event_triggers)
    variables = {}
    for line in generate_function_code(graph, sockets_to_calculate, variables):
        yield "    " + line

    for trigger in event_triggers:
        inputs = get_data_flow_inputs(trigger)
        for line in trigger.get_trigger_code():
            yield "    " + replace_local_identifiers(line, trigger, inputs, variables)
        yield "    if TRIGGERED:"
        yield "        pass"
        for line in generate_action_code(graph, trigger.outputs[0]):
            if "KILL" in line:
                yield " " * (8 + line.index("KILL")) + "return False"
            else:
                yield "        " + line

    yield "    return True"

def get_data_flow_inputs(nodes):
    if isinstance(nodes, bpy.types.Node):
        nodes = [nodes]

    sockets = set()
    for node in nodes:
        for socket in node.inputs:
            if isinstance(socket, DataFlowSocket):
                sockets.add(socket)
    return sockets


# Simulation
#####################################

def simulate_step(particle_system, state, current_time, time_step):
    for particle_type in particle_system.particle_types:
        killed_particles = set()
        for particle in state.particles_by_type[particle_type]:
            particle.velocity += particle_type.forces_function(particle.location) * time_step
            particle.location += particle.velocity * time_step

            still_alive = particle_type.events_function(particle, current_time, time_step)
            if not still_alive:
                killed_particles.add(particle)

        state.particles_by_type[particle_type] -= killed_particles

        new_particles = particle_type.emitter_function(current_time, time_step)
        for particle in new_particles:
            particle.born_time = current_time
        state.particles_by_type[particle_type].update(new_particles)

class ParticleSystemState:
    def __init__(self):
        self.particles_by_type = defaultdict(set)

class ParticleSystem:
    def __init__(self, particle_types):
        self.particle_types = particle_types

class ParticleType:
    def __init__(self, emitter_function, forces_function, events_function):
        self.emitter_function = emitter_function
        self.forces_function = forces_function
        self.events_function = events_function

class Particle:
    def __init__(self):
        self.location = Vector((0, 0, 0))
        self.velocity = Vector((0, 0, 0))
        self.born_time = 0