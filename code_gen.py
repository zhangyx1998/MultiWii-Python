from lib import MSP, Command

print("#include <stdint.h>")
print("""
#ifndef __MSP_SEND__
#define __MSP_SEND__(NAME, CODE) \\
void MSP_##NAME##(MSP_##NAME##_t *data) {}
#endif

#ifndef __MSP_RECV__
#define __MSP_RECV__(NAME, CODE) \\
void MSP_##NAME##(MSP_##NAME##_t *data) {}
#endif
""")

INDENT = "  "

MSP_COMMANDS = {}

for key in dir(MSP):
    item = getattr(MSP, key)
    try:
        if issubclass(item, Command.MSP_Command):
            MSP_COMMANDS[item.code] = {
                "key": key,
                "struct": item.struct,
                "direction": "MSP_RECV" if issubclass(item, Command.ReadCMD) else "MSP_SEND"
            }
    except Exception:
        pass

for code in sorted(MSP_COMMANDS.keys()):
    key = MSP_COMMANDS[code]["key"]
    struct = MSP_COMMANDS[code]["struct"]
    direction = MSP_COMMANDS[code]["direction"]
    name = "MSP_" + key
    struct_content = [INDENT + f"{t.ctype()} {key};" for key, t in struct.items()]
    print("\ntypedef struct " + name + "_s {", *struct_content, "} " + name + "_t;", sep='\n', end='\n\n')
    print(f"__{direction}__({key}, {code});")
