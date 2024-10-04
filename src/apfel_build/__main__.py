"""
Script used to build the apfel library.
"""

import logging
from pathlib import Path
import importlib
import importlib.util
import argparse

BUILD_PKG_ROOT = Path(__file__).parent
PKG_ROOT = BUILD_PKG_ROOT.parent / "apfel"

ARGPARSER = argparse.ArgumentParser(description="Build the apfel library.")
ARGPARSER.add_argument("--verbose", action="store_true", help="Enable verbose logging.")
ARGS: argparse.Namespace = argparse.Namespace()

logging.basicConfig(level=logging.WARNING, format="%(levelname)s | %(message)s")

def gen():
    """\
    Generate all type stubs for the apfel library.
    """

    iter_gen_path = (
        p
        for (dir, _, list_file) in Path(__file__).parent.walk()
        for file in list_file if (p := dir / file).name.endswith(".gen.py")
    )

    for path in iter_gen_path:
        qualname = ".".join(path.relative_to(BUILD_PKG_ROOT).with_name(path.name.replace(".gen.py", "")).parts)
        logging.info(f"Generating type stub for {qualname}")

        target_path = (PKG_ROOT / path.relative_to(BUILD_PKG_ROOT)).with_name(path.name.replace(".gen.py", ".pyi"))
        spec = importlib.util.spec_from_file_location(qualname, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with ( 
            target_path.open("w") as pyi,
        ):
            pyi.write(module.pyi.content.getvalue())


if __name__ == "__main__":
    ARGS = ARGPARSER.parse_args()
    importlib.util.spec_from_file_location("apfel_build", Path(__file__).parent / "__init__.py")

    if ARGS.verbose:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    gen()
