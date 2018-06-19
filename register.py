import bpy
from . import ui
from . import menu
from . import trees
from . import nodes
from . import sockets
from . import operators

def register():
    operators.register()
    sockets.register()
    trees.register()
    nodes.register()
    menu.register()
    ui.register()

def unregister():
    ui.register()
    menu.unregister()
    nodes.unregister()
    trees.unregister()
    sockets.unregister()
    operators.unregister()
    bpy.utils.unregister_class(EverythingNodesTree)