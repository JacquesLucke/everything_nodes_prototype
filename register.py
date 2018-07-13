import bpy
from . utils.imports import collect_new_vars

from . import trees

before = locals().copy()
from . import ui
from . import menu
from . import nodes
from . import sockets
from . import operators
modules = collect_new_vars(before, locals())

def register():
    trees.register()

    for module in modules:
        module.register()

def unregister():
    for module in reversed(modules):
        module.unregister()

    trees.unregister()
