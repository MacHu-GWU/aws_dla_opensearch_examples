# -*- coding: utf-8 -*-

__version__ = "0.0.1"

try:
    from .connection import oss
    from . import helpers
except ImportError:
    pass
except:
    pass
