def init_variables(data_type, variables):
    if str(data_type) == "string":
        return tuple("" for _ in range(int(variables)))
    elif str(data_type) == "true":
        return tuple(True for _ in range(variables))
    elif str(data_type) == "false":
        return tuple(False for _ in range(variables))
    elif str(data_type) == "set":
        return tuple(set() for _ in range(variables))
    else:
        return tuple("" for _ in range(int(variables)))