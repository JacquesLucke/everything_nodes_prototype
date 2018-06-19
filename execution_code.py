import re
from functools import lru_cache

def generate_function_code(graph, output_sockets, variables,
        generate_unlinked_input, generate_self_expression):
    def calculate_socket(socket):
        if socket in variables:
            return

        if socket.is_output:
            node = graph.get_node_by_socket(socket)

            for input_socket in node.inputs:
                yield from calculate_socket(input_socket)

            for output_socket in node.outputs:
                variables[output_socket] = get_new_socket_name(graph, output_socket)

            for line in node.get_code():
                for socket in node.sockets:
                    line = replace_variable_name(line, socket.identifier, variables[socket])
                line = replace_variable_name(line, "self", generate_self_expression(graph, node))
                yield line
        else:
            linked_sockets = graph.get_linked_sockets(socket)
            if len(linked_sockets) == 0:
                yield from generate_unlinked_input(graph, socket, variables)
            elif len(linked_sockets) == 1:
                source_socket = next(iter(linked_sockets))
                yield from calculate_socket(source_socket)
                variables[socket] = variables[source_socket]

    for socket in output_sockets:
        yield from calculate_socket(socket)

counter = 0

def get_new_socket_name(graph, socket):
    global counter
    counter += 1
    return "_" + str(counter)

@lru_cache(maxsize = 2**15)
def replace_variable_name(code, oldName, newName):
    pattern = r"([^\.\"']|^)\b{}\b".format(oldName)
    return re.sub(pattern, r"\1{}".format(newName), code)