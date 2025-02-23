"""Parses an nginx.conf file and handle the errors"""

import io

import crossplane


class ParseError(BaseException):
    pass


def _format_error(error: dict):
    msg = io.StringIO()
    msg.write(error["file"])
    if error["line"] is not None:
        msg.write(f"({error['line']})")
    msg.write(f": {error['error'] or 'unknown error'}")
    return msg.getvalue()


def _handle_errors(errors: list):
    if not errors:
        return

    raise ParseError("\n".join(_format_error(error) for error in errors))


def parse(path: str) -> dict:
    root = crossplane.parse(path)
    _handle_errors(root["errors"])

    config = root["config"][0]
    _handle_errors(config["errors"])

    parsed = config["parsed"]
    return parsed
