class Dependency:
    def __init__(self, object, attribute):
        self.object = object
        self.attribute = attribute

    def __hash__(self):
        return hash((self.object, self.attribute))

    def __eq__(self, other):
        return self.object == other.object and self.attribute == other.attribute

    def __repr__(self):
        return f"<Object: {repr(self.object)}, {repr(self.attribute)}>"