import importlib
import os.path

from ._foundation import *

log = Log(
    "dependency",
    log_output_to_file_path=f"{log_path}dependency.log",
)

json = Json()
modules = json.load("dependency_load_modules")
"""
{
    "name": {
        "name": str
        "load": T/F,
    }
}
"""
if modules is False:
    modules = {
        "tkinter": {
            "load": False,
            "name": "tkinter"
        }
    }
    json.dump(modules, "dependency_load_modules")

_t = {}
for name in modules.keys():
    try:
        log.info(f"load {name}")
        if modules[name]["load"]:
            _t[name] = importlib.import_module(
                os.path.join(
                    "modules",
                    f'_{modules[name]["name"]}'
                ),
                package=__package__,
            )
    except Exception as e:
        log.error(e)
        print(f"load {name} error:{e}")
        _t[name] = False

modules = _t
