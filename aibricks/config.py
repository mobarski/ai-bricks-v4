import os
from yamja import lookup, load_config, load_configs

_this_dir = os.path.dirname(__file__)
providers = load_config(os.path.join(_this_dir, 'providers.yaml'))
