import bpy
from bpy.props import *

class PrintDriverDependenciesOperator(bpy.types.Operator):
    bl_idname = "en.print_driver_dependencies"
    bl_label = "Print Driver Dependencies"

    index = IntProperty()

    def execute(self, context):
        object = context.active_object
        driver = object.drivers[self.index]
        print(f"Driver: {repr(driver.path)} on {repr(object.name)}")

        for dependency in driver.get_dependencies():
            print(f"  {repr(dependency.attribute)} of {repr(dependency.object.name)}")

        return {"FINISHED"}
