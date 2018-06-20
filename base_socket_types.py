class Socket:
    def draw_color(self, context, node):
        return self.color

    def draw(self, context, layout, node, text):
        raise NotImplementedError()

    def get_index(self, node):
        if self.is_output:
            return list(node.outputs).index(self)
        else:
            return list(node.inputs).index(self)

class DataFlowSocket(Socket):
    data_type = NotImplemented

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text)
        else:
            self.draw_property(layout, text, node)

    def draw_property(self, layout, text, node):
        layout.label(text)

    def get_value(self):
        raise NotImplementedError()

    def internal_data_changed(self, context = None):
        self.id_data.internal_data_socket_changed()

    def external_data_changed(self, context = None):
        self.id_data.external_data_socket_changed()

    def get_dependencies(self):
        return
        yield

class InternalDataFlowSocket(DataFlowSocket):
    pass

class ExternalDataFlowSocket(DataFlowSocket):
    pass

# There is only one of this type
# class ControlFlowSocket(Socket):
#     pass

class RelationalSocket(Socket):
    pass