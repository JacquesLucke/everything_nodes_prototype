import bpy
from . group_info_panel import GroupInfoPanel

panels = [
    GroupInfoPanel
]

def register():
    for cls in panels:
        bpy.utils.register_class(cls)

def unregister():
    for cls in panels:
        bpy.utils.unregister_class(cls)