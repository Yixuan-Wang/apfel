from __future__ import annotations
import sys
from types import FrameType, TracebackType
from annotated_types import T
from typing_extensions import Never
import traceback
import functools

def cover_up(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        caller = sys._getframe(1)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            e.__traceback__ = TracebackType(None, caller, caller.f_lasti, caller.f_lineno)

            traceback.print_exception(e)

            raise e

    return wrapper
