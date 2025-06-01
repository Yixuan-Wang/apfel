"""
A set of helper functions that inspect contextual information during runtime.

See [non-standard evaluation](http://adv-r.had.co.nz/Computing-on-the-language.html){ .ref .rl } for more inspiration.
"""

import ast
import sys
import inspect

def call_expr():
    """
    Get the call expression that invoked the callee.
    """
    try:
        # 0 is the current frame, 1 is the callee and caller to `call_expr`, 2 is the caller.
        caller_frame_raw = sys._getframe(2)

        caller_frame = inspect.getframeinfo(caller_frame_raw)

        assert caller_frame.positions is not None, (
            "The caller frame must have positions"
        )
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

        line_start, line_end = (
            absolute_lineno - starting_lineno,
            absolute_end_lineno - starting_lineno,
        )

        if line_start == line_end:
            segment = caller_lines[line_start][col_offset:end_col_offset]
        else:
            segment = "".join(
                (
                    caller_lines[line_start][col_offset:],
                    *caller_lines[line_start + 1 : line_end],
                    caller_lines[line_end][:end_col_offset],
                )
            )

        ast_node = ast.parse(segment, filename="<ast>", mode="eval")
        assert isinstance(ast_node.body, ast.Call), "The line must be a function call"

        for node in ast.walk(ast_node):
            if hasattr(node, "lineno") and node.lineno is not None:  # pyright: ignore[reportAttributeAccessIssue]
                if node.lineno == 1:  # pyright: ignore[reportAttributeAccessIssue]
                    node.col_offset += col_offset  # pyright: ignore[reportAttributeAccessIssue]
                    node.end_col_offset += col_offset  # pyright: ignore[reportAttributeAccessIssue]
                node.lineno += absolute_lineno - 1  # pyright: ignore[reportAttributeAccessIssue]
            if hasattr(node, "end_lineno") and node.end_lineno is not None:  # pyright: ignore[reportAttributeAccessIssue]
                node.end_lineno += absolute_lineno - 1  # pyright: ignore[reportAttributeAccessIssue]

        args = ast_node.body.args
        return args

    except Exception:
        return None


if sys.version_info < (3, 11):

    def get_real_arg():
        return None
