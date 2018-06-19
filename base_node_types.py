from . callback import get_node_callback

class Node:
    def init(self, context):
        self.create()

    def create(self):
        pass

    def new_input(self, idname, name, identifier = None):
        if identifier is None: identifier = name
        self.inputs.new(idname, name, identifier)

    def new_output(self, idname, name, identifier = None):
        if identifier is None: identifier = name
        self.outputs.new(idname, name, identifier)

    def draw_buttons(self, context, layout):
        self.draw(layout)

    def draw(self, layout):
        pass

    def invoke_function(self, layout, function_name, text):
        props = layout.operator("en.execute_callback", text = text)
        props.callback = get_node_callback(self, function_name)

    def invoke_socket_type_chooser(self, layout, function_name, text):
        props = layout.operator("en.choose_socket_type", text = text)
        props.callback = get_node_callback(self, function_name)

    @property
    def sockets(self):
        return list(self.inputs) + list(self.outputs)

class ImperativeNode(Node):
    pass

class FunctionalNode(Node):
    def get_code(self):
        raise NotImplementedError()

    def get_external_dependencies(self, external_values_per_socket):
        return
        yield

class DeclarativeNode(Node):
    pass