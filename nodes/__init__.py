import bpy
from . group_input import GroupInputNode
from . group_output import GroupOutputNode
from . float_math import FloatMathNode
from . combine_vector import CombineVectorNode
from . separate_vector import SeparateVectorNode
from . object_transforms import ObjectTransformsNode
from . offset_vector_with_object import OffsetVectorWithObjectNode
from . get_parent_object import GetObjectParentNode
from . vector_math import VectorMathNode
from . key_press_event import KeyPressEventNode
from . move_object import MoveObjectNode
from . condition import ConditionNode

node_classes = [
    GroupInputNode,
    GroupOutputNode,
    FloatMathNode,
    CombineVectorNode,
    SeparateVectorNode,
    ObjectTransformsNode,
    OffsetVectorWithObjectNode,
    GetObjectParentNode,
    VectorMathNode,
    KeyPressEventNode,
    MoveObjectNode,
    ConditionNode
]

def register():
    for cls in node_classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in node_classes:
        bpy.utils.unregister_class(cls)