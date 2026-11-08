docs:
    docker run --rm -v "$PWD/docs/site:/app/docs/site:ro" -v "$PWD/docs/content:/app/src/content/docs:ro" -v "$PWD:/app/source:ro" ghcr.io/yixuan-wang/astro-docs-python:latest

test:
    uv run tox
