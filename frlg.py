import scripting
import json
import sys

scripting.install_commands(sys.modules[__name__],json.load(open("frlg.json")))