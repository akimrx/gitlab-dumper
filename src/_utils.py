import os

def bytes_to_human(data: int, granularity=1) -> str:
    """Convert bytes to human format with binary prefix."""
    _bytes = int(data)
    result = []
    # fmt: off
    sizes = (
        ("TB", 1024 ** 4),
        ("GB", 1024 ** 3),
        ("MB", 1024 ** 2),
        ("KB", 1024),
        ("B", 1)
    )
    # fmt: on
    if _bytes == 0:
        return 0
    else:
        for name, count in sizes:
            value = _bytes // count
            if value:
                _bytes -= value * count
                result.append(f"{value}{name}")
        return ", ".join(result[:granularity])


def safe_resolve_path(path: str) -> str:
    """Safe convert path to absolute."""
    if path.startswith("~"):
        return os.path.expanduser(path)

    elif path.startswith(".") or not path.startswith("/"):
        return os.path.abspath(path)

    return path


__all__ = ["bytes_to_human", "safe_resolve_path"]
