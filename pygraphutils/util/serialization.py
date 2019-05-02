import numpy as np
import json
from enum import Enum

# See https://stackoverflow.com/a/27050186
class GenericJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, Enum):
            return str(obj)
        else:
            return super(GenericJSONEncoder, self).default(obj)

