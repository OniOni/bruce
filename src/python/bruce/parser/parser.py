from typing import List

from ..task import BaseTask
from . import ini

try:
    from . import toml_
except Exception:
    toml_ = None  # type: ignore


def parse(configfile: str) -> List[BaseTask]:
    if configfile.endswith(".toml"):
        if toml_:
            return toml_.parse(configfile)
        else:
            raise Exception
    elif configfile.endswith(".ini"):
        return ini.parse(configfile)
    else:
        raise Exception
