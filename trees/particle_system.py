import bpy
from . base import NodeTree
from mathutils import Vector, Color
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
            find_trigger_function = get_find_next_trigger_function(self, event_triggers)
            event_handlers = get_event_handlers(self, event_triggers)

            particle_type = ParticleType(
                emitter_function, forces_function,
                find_trigger_function, event_handlers)
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
    yield "def main(START_TIME, TIME_STEP):"

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
def get_find_next_trigger_function(tree, event_triggers):
    graph = tree.graph
    yield from iter_import_lines(tree)
    yield "def main(PARTICLE, START_TIME, MAX_TIME_STEP):"
    yield "    EARLIEST_TRIGGER_TIME = MAX_TIME_STEP"
    yield "    EARLIEST_TRIGGER = None"

    sockets_to_calculate = get_data_flow_inputs(event_triggers)
    variables = {}
    for line in generate_function_code(graph, sockets_to_calculate, variables):
        yield "    " + line

    for trigger in event_triggers:
        inputs = get_data_flow_inputs(trigger)
        for line in trigger.get_trigger_code():
            yield "    " + replace_local_identifiers(line, trigger, inputs, variables)
        yield "    if 0 < TRIGGER_TIME <= EARLIEST_TRIGGER_TIME:"
        yield "        EARLIEST_TRIGGER_TIME = TRIGGER_TIME"
        yield "        EARLIEST_TRIGGER = " + repr(trigger.name)

    yield "    return EARLIEST_TRIGGER_TIME, EARLIEST_TRIGGER"

def get_event_handlers(tree, event_triggers):
    return {node.name : get_event_handler(tree, node) for node in event_triggers}

@code_to_function()
def get_event_handler(tree, event_trigger):
    graph = tree.graph
    yield from iter_import_lines(tree)
    yield "def main(PARTICLE, CURRENT_TIME):"

    for line in generate_action_code(graph, event_trigger.outputs[0]):
        if "KILL" in line:
            yield " " * (4 + line.index("KILL")) + "return False"
        else:
            yield "    " + line

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

def simulate_step(particle_system, state, start_time, time_step):
    for particle_type in particle_system.particle_types:
        killed_particles = set()
        for particle in state.particles_by_type[particle_type]:
            time_to_simulate = time_step
            current_time = start_time
            while time_to_simulate > 0:
                elapsed_time, event_handler_name = particle_type.find_trigger_function(particle, current_time, time_to_simulate)

                run_modifiers(particle_type, particle, current_time, elapsed_time)
                current_time += elapsed_time
                time_to_simulate -= elapsed_time

                if event_handler_name is not None:
                    still_alive = particle_type.event_handlers[event_handler_name](particle, current_time)
                    if not still_alive:
                        killed_particles.add(particle)
                        break

        state.particles_by_type[particle_type] -= killed_particles

        new_particles = particle_type.emitter_function(start_time, time_step)
        state.particles_by_type[particle_type].update(new_particles)

def run_modifiers(particle_type, particle, start_time, time_step):
    particle.location += particle.velocity * time_step
    particle.velocity += particle_type.forces_function(particle.location) * time_step

class ParticleSystemState:
    def __init__(self):
        self.particles_by_type = defaultdict(set)

class ParticleSystem:
    def __init__(self, particle_types):
        self.particle_types = particle_types

class ParticleType:
    def __init__(self, emitter_function, forces_function,
            find_trigger_function, event_handlers):
        self.emitter_function = emitter_function
        self.forces_function = forces_function
        self.find_trigger_function = find_trigger_function
        self.event_handlers = event_handlers

class Particle:
    def __init__(self):
        self.location = Vector((0, 0, 0))
        self.velocity = Vector((0, 0, 0))
        self.born_time = 0
        self.color = Color((1, 1, 1))