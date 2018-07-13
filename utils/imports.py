def collect_new_vars(locals_before, locals_after):
    new_objects = list()
    for name in locals_after.keys():
        if name not in locals_before.keys():
            object = locals_after[name]
            if object is not locals_before:
                new_objects.append(object)

    return new_objects
