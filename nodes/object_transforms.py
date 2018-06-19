import bpy
from .. base_node_types import FunctionalNode

class ObjectTransformsNode(FunctionalNode, bpy.types.Node):
    bl_idname = "en_ObjectTransformsNode"
    bl_label = "Object Transforms"

    def create(self):
        self.new_input("en_ObjectSocket", "Object", "object")
        self.new_output("en_VectorSocket", "Location", "location")
        self.new_output("en_VectorSocket", "Scale", "scale")

    def get_code(self):
        yield "if object is None:"
        yield "    location = mathutils.Vector((0, 0, 0)"
        yield "    scale = mathutils.Vector((1, 1, 1)"
        yield "else:"
        yield "    location = object.location.copy()"
        yield "    scale = object.scale.copy()"