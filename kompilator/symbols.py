cellCounter = 3
forCounter = 1

globalIdentifierHashMap = {}
functionArgumentsHashMap = {}

functionHashMap = {
    "PROGRAM_mul": 1,
    "PROGRAM_divMod": 29,
}


def add_identifier(name, declaration):
    if name in globalIdentifierHashMap:
        raise ValueError(f"Duplicate identifier {name}")
    globalIdentifierHashMap[name] = declaration

def get_identifier(name):
    return globalIdentifierHashMap.get(name)
