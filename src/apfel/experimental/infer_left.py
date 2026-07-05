import ast
import inspect
import sys
import textwrap
from itertools import chain


def _span(node: ast.expr) -> tuple[tuple[int, int], tuple[int, int]]:
    assert node.lineno is not None, "Node must have a starting line number"
    assert node.end_lineno is not None, "Node must have an ending line number"
    assert node.col_offset is not None, "Node must have a starting column offset"
    assert node.end_col_offset is not None, "Node must have an ending column offset"
    return (node.lineno, node.col_offset), (node.end_lineno, node.end_col_offset)


def _has_span(node: ast.AST) -> bool:
    return getattr(node, "lineno", None) is not None


def _contains(
    outer: tuple[tuple[int, int], tuple[int, int]],
    inner: tuple[tuple[int, int], tuple[int, int]],
) -> bool:
    outer_start, outer_end = outer
    inner_start, inner_end = inner
    return outer_start <= inner_start and inner_end <= outer_end


def _relevant_children(node: ast.AST):
    for field_name, value in ast.iter_fields(node):
        if isinstance(value, ast.AST):
            yield field_name, value
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    yield field_name, item


def _parse_target(target: ast.expr):
    if isinstance(target, ast.Tuple):
        return [
            {"__class__": element.__class__, **vars(element)}
            for element in target.elts
        ]
    else:
        return ({"__class__": target.__class__, **vars(target)},)


def _extract_targets(
    node: ast.Assign | ast.AnnAssign | ast.AugAssign | ast.NamedExpr,
):
    if isinstance(node, ast.Assign):
        targets = list(chain.from_iterable(map(_parse_target, node.targets)))
    else:
        (target,) = _parse_target(node.target)
        if isinstance(node, ast.AnnAssign):
            target["annotation"] = node.annotation
        elif isinstance(node, ast.AugAssign):
            target["op"] = node.op
        targets = [target]

    match len(targets):
        case 1:
            return targets[0]
        case _:
            return targets


_ASSIGN_LIKE = (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.NamedExpr)


def _find(
    node: ast.AST,
    target_span: tuple[tuple[int, int], tuple[int, int]],
):
    # `path` is a cons-list (node, rest) | None, innermost-first, so the
    # nearest enclosing ancestor is found by a plain forward walk - no
    # per-descent list copy and no final reversal, unlike a plain list.
    stack: list[tuple[ast.AST, tuple | None]] = [(node, None)]

    while stack:
        current, path = stack.pop()

        if isinstance(current, ast.Call) and _span(current) == target_span:
            while path is not None:
                ancestor, path = path
                if isinstance(ancestor, _ASSIGN_LIKE):
                    return _extract_targets(ancestor)
            return None

        if _has_span(current) and not _contains(_span(current), target_span):
            continue

        for field_name, child in _relevant_children(current):
            new_path = (current, path) if field_name == "value" else path
            stack.append((child, new_path))

    return None


def infer_left():
    """Infer the left-hand side who the function call is assigned to.

    ```python
    def f():
        return infer_left()["id"]

    a = f()
    assert a == "a"
    ```
    """
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

    target_span = (
        (line_start + 1, col_offset - dedent_amount),
        (line_end + 1, end_col_offset - dedent_amount),
    )

    return _find(ast_context, target_span)
