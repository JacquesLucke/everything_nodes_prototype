import bpy
from bpy.props import *
from .. trees import DataFlowGroupTree

class FunctionalPropertyDriver(bpy.types.PropertyGroup):
    def is_function(self, tree):
        return isinstance(tree, DataFlowGroupTree) and tree.is_valid_function

    path = StringProperty()
    data_flow_group = PointerProperty(type = bpy.types.NodeTree, poll = is_function)

class FunctionalObjectDrivers(bpy.types.PropertyGroup):
    property_drivers = CollectionProperty(type = FunctionalPropertyDriver)



def evaluate_drivers():
    for object in bpy.context.scene.objects:
        evaluate_drivers_on_object(object)

def evaluate_drivers_on_object(object):
    for driver in object.drivers.property_drivers:
        group = driver.data_flow_group
        if group is None:
            continue
        if not group.is_valid_function:
            continue

        signature = group.signature
        if not signature.match_output([get_data_type(driver.path)]):
            raise Exception("output type of function does not match the property")
        if signature.match_input([]):
            value = group.function()
        elif signature.match_input(["Object"]):
            value = group.function(object)
        exec(f"object.{driver.path} = value", {"object" : object, "value" : value})

def get_data_type(path):
    if path in {"location", "scale"}:
        return "Vector"
    elif path in {"location.x", "location.y", "location.z"}:
        return "Float"
    else:
        raise Exception(f"type of property '{path}' is unknown")



property_groups = [
    FunctionalPropertyDriver,
    FunctionalObjectDrivers
]

def register():
    for cls in property_groups:
        bpy.utils.register_class(cls)
    bpy.types.Object.drivers = PointerProperty(type = FunctionalObjectDrivers)

def unregister():
    del bpy.types.Object.drivers
    for cls in reversed(property_groups):
        bpy.utils.unregister_class(cls)