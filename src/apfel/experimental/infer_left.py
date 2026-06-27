import ast
import inspect
import sys
import textwrap
from dataclasses import dataclass, field
from itertools import chain


@dataclass(slots=True)
class CallNodeVisitor(ast.NodeVisitor):
    lineno: int
    end_lineno: int
    col_offset: int
    end_col_offset: int

    targets: list[dict] = field(default_factory=list)

    def _is_this_assign(
        self, node: ast.Assign | ast.AnnAssign | ast.AugAssign | ast.NamedExpr
    ) -> bool:
        value = node.value
        return (
            isinstance(value, ast.Call)
            and value.lineno == self.lineno
            and value.col_offset == self.col_offset
            and value.end_col_offset == self.end_col_offset
            and value.end_lineno == self.end_lineno
        )

    def parse_target(self, target: ast.expr):
        if isinstance(target, ast.Tuple):
            return [
                {"__class__": element.__class__, **vars(element)}
                for element in target.elts
            ]
        else:
            return ({"__class__": target.__class__, **vars(target)},)

    def visit_Assign(self, node: ast.Assign):
        if not self._is_this_assign(node):
            return

        self.targets.extend(chain.from_iterable(map(self.parse_target, node.targets)))

    def visit_AnnAssign(self, node: ast.AnnAssign):
        if not self._is_this_assign(node):
            return

        (target, ) = self.parse_target(node.target)
        target["annotation"] = node.annotation

        self.targets.append(target)

    def visit_AugAssign(self, node: ast.AugAssign):
        if not self._is_this_assign(node):
            return

        (target, ) = self.parse_target(node.target)
        target["op"] = node.op

        self.targets.append(target)

    def visit_NamedExpr(self, node: ast.NamedExpr):
        if not self._is_this_assign(node):
            return

        self.targets.extend(self.parse_target(node.target))


def infer_left():
    caller_frame_raw = sys._getframe(2)
    caller_frame = inspect.getframeinfo(caller_frame_raw)

    assert caller_frame.positions is not None, "The caller frame must have positions"
    assert caller_frame.positions.lineno is not None, (
        "The caller frame must have a starting line number"
    )
    assert caller_frame.positions.end_lineno is not None, (
        "The caller frame must have an ending line number"
    )
    assert caller_frame.positions.col_offset is not None, (
        "The caller frame must have a starting column offset"
    )

    caller_lines, starting_lineno = inspect.getsourcelines(caller_frame_raw)

    # if the caller frame is a module, the starting_lineno is set to 0
    # see https://github.com/python/cpython/pull/103226
    # which will never be fixed
    if starting_lineno == 0:
        starting_lineno = 1

    absolute_lineno = caller_frame.positions.lineno
    absolute_end_lineno = caller_frame.positions.end_lineno
    col_offset = caller_frame.positions.col_offset
    end_col_offset = caller_frame.positions.end_col_offset
    assert end_col_offset is not None

    line_start, line_end = (
        absolute_lineno - starting_lineno,
        absolute_end_lineno - starting_lineno,
    )

    context_str = "".join(caller_lines)
    non_empty = [l for l in context_str.splitlines() if l.strip()]
    dedent_amount = min((len(l) - len(l.lstrip()) for l in non_empty), default=0)
    context_str = textwrap.dedent(context_str)
    ast_context = ast.parse(context_str, "<ast>", mode="single")

    visitor = CallNodeVisitor(
        lineno=line_start + 1,
        end_lineno=line_end + 1,
        col_offset=col_offset - dedent_amount,
        end_col_offset=end_col_offset - dedent_amount,
    )
    visitor.visit(ast_context)

    match len(visitor.targets):
        case 0:
            return None
        case 1:
            return visitor.targets[0]
        case _:
            return visitor.targets
