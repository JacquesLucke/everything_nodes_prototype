import bpy
from . base import NodeTree
from mathutils import Vector
from collections import defaultdict
from .. base_socket_types import DataFlowSocket
from .. nodes.particle_emitter_base import ParticleEmitterNode

from . data_flow_group import (
    iter_import_lines,
    generate_function_code,
    replace_local_identifiers,
    main_function_from_code_lines
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
            particle_type = ParticleType(emitter_function)
            particle_types.append(particle_type)
        return ParticleSystem(particle_types)


def get_emitter_nodes_for_particle_node(graph, node):
    emitters = set()
    for socket in graph.get_linked_sockets(node.inputs["Emitter"]):
        linked_node = graph.get_node_by_socket(socket)
        if isinstance(linked_node, ParticleEmitterNode):
            emitters.add(linked_node)
    return emitters

def get_emitter_function(tree, emitters):
    return main_function_from_code_lines(iter_emitter_function_code(tree, emitters))

def iter_emitter_function_code(tree, emitters):
    graph = tree.graph
    yield from iter_import_lines(tree)
    yield "from everything_nodes_prototype.trees.particle_system import Particle as NEW_PARTICLE"
    yield "def main(CURRENT_TIME, TIME_STEP):"

    sockets_to_calculate = set()
    for emitter in emitters:
        for socket in emitter.inputs:
            if isinstance(socket, DataFlowSocket):
                sockets_to_calculate.add(socket)

    variables = {}
    for line in generate_function_code(graph, sockets_to_calculate, variables):
        yield "    " + line

    yield "    ALL_NEW_PARTICLES = []"
    for emitter in emitters:
        inputs = {s for s in emitter.inputs if isinstance(s, DataFlowSocket)}
        for line in emitter.get_emit_code():
            yield "    " + replace_local_identifiers(line, emitter, inputs, variables)

        yield "    ALL_NEW_PARTICLES.extend(EMITTED)"
    yield "    return ALL_NEW_PARTICLES"



def simulate_step(particle_system, state, current_time, time_step):
    for particle_type in particle_system.particle_types:
        for particle in state.particles_by_type[particle_type]:
            particle.location += particle.velocity * time_step

        new_particles = particle_type.emitter_function(current_time, time_step)
        state.particles_by_type[particle_type].update(new_particles)

class ParticleSystemState:
    def __init__(self):
        self.particles_by_type = defaultdict(set)

class ParticleSystem:
    def __init__(self, particle_types):
        self.particle_types = particle_types

class ParticleType:
    def __init__(self, emitter_function):
        self.emitter_function = emitter_function

class Particle:
    def __init__(self):
        self.location = Vector((0, 0, 0))
        self.velocity = Vector((0, 0, 0))