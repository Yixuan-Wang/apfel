def test_transform():
    from apfel.impt.transform import register_transform_hook
    import importlib
    from sys import modules

    if "typing_extensions" in modules:
        del modules["typing_extensions"]

    def hook(source: str) -> str:
        return source + "\nHI = 'Hello, World!'\n"
    
    register_transform_hook("typing_extensions", hook)
    import typing_extensions

    assert hasattr(typing_extensions, "HI")
    assert typing_extensions.HI == "Hello, World!"  # type: ignore

    importlib.reload(typing_extensions)
    assert hasattr(typing_extensions, "HI")
