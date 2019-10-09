from shutil import which


def is_tool_accessible(tool):
    """Check whether `tool` is on PATH and marked as executable."""

    return which(tool) is not None
