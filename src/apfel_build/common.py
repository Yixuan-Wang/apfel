from dataclasses import dataclass, field
from functools import partial
from contextlib import contextmanager
import io

@dataclass
class PYI:
    content: io.StringIO = field(default_factory=io.StringIO)
    indent_level: int = field(default=0, init=False)

    def emit(self, *lines):
        indent_spaces = "    " * self.indent_level
        for line in lines:
            self.content.write(indent_spaces)
            self.content.write(line)
            self.content.write("\n")

    @contextmanager
    def indent(self, *, is_item: bool = True):
        try:
            self.indent_level += 1
            yield self.indent_level
        finally:
            self.indent_level -= 1
            if is_item: self.emit("")
