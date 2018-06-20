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
    def get_code(self):
        """
        Similar to the FunctionalNode.get_code function.
        But here the generated code is allowed to have side effects.
        """
        raise NotImplementedError()

class FunctionalNode(Node):
    def get_code(self, required):
        """
        Yields lines of Python code that execute the node.
        The identifiers of input and output sockets can be used.
        Also "self" is allowed to reference the node.
        """
        raise NotImplementedError()

    def get_external_dependencies(self, external_values_per_socket, required):
        """
        Given the possible input values for external sockets (e.g. objects),
        output the necessary dependencies to calculate the outputs
        """
        return
        yield

    def execute_external(self, possible_values_per_socket):
        """
        Given the possible input values for external sockets,
        output the possible values for external output sockets.
        """
        return {}

    def get_required_inputs(self, outputs):
        """
        Output a (sub)set of the input nodes, that are required to
        calculate the outputs.
        """
        return set(self.inputs)

    def code_changed(self, context = None):
        self.id_data.update()

class DeclarativeNode(Node):
    pass