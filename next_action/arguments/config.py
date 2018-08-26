"""Methods for reading, parsing, and validating Next-action configuration files."""

import argparse
import os
import string
import sys
from typing import Callable, Dict, List, Union

from pygments.styles import get_all_styles
import yaml
import cerberus


def read_config_file(filename: str, default_filename: str, error: Callable[[str], None]):
    """Read and parse the configuration file."""
    try:
        with open(os.path.expanduser(filename), "r") as config_file:
            return yaml.safe_load(config_file.read())
    except FileNotFoundError as reason:
        if filename == default_filename:
            # Don't complain if there's no configuration file at the default location
            return dict()  # pragma: no cover-behave
        error(f"can't open file: {reason}")
    except OSError as reason:
        error(f"can't open file: {reason}")
    except yaml.YAMLError as reason:
        error(f"can't parse {filename}: {reason}")


def write_config_file(namespace: argparse.Namespace) -> None:
    """Generate a configuration file on standard out."""
    intro = "# Configuration file for Next-action. Edit the settings below as you like.\n"
    options = dict(file=namespace.file[0] if len(namespace.file) == 1 else namespace.file,
                   reference=namespace.reference, style=namespace.style or "default")
    prefixed_filters = []
    for prefix, filters in (("@", namespace.contexts), ("+", namespace.projects),
                            ("-@", namespace.excluded_contexts), ("-+", namespace.excluded_projects)):
        prefixed_filters.extend([prefix + filter_name for filter_name in filters])
    if prefixed_filters:
        options["filters"] = prefixed_filters
    if namespace.number == sys.maxsize:
        options["all"] = True
    else:
        options["number"] = namespace.number
    if namespace.priority:
        options["priority"] = namespace.priority
    if namespace.blocked:
        options["blocked"] = True
    config = yaml.dump(options, default_flow_style=False)
    sys.stdout.write(intro + config)


def validate_config_file(config, config_filename: str, error: Callable[[str], None]) -> None:
    """Validate the configuration file contents."""
    schema = {
        "file": {
            "type": ["string", "list"],
            "schema": {"type": "string"}
        },
        "number": {
            "type": "integer",
            "min": 1,
            "excludes": "all"
        },
        "all": {
            "type": "boolean",
            "allowed": [True]
        },
        "priority": {
            "type": "string",
            "allowed": [letter for letter in string.ascii_uppercase]
        },
        "filters": {
            "type": ["string", "list"],
            "regex": r"^\-?[@|\+]\S+(\s+\-?[@|\+]\S+)*",
            "schema": {"type": "string", "regex": r"^\-?[@|\+]\S+"}
        },
        "reference": {
            "type": "string",
            "allowed": ["always", "never", "multiple"]
        },
        "style": {
            "type": "string",
            "allowed": sorted(list(get_all_styles()))
        },
        "blocked": {
            "type": "boolean",
            "allowed": [True]
        }
    }
    validator = cerberus.Validator(schema)
    try:
        valid = validator.validate(config)
    except cerberus.validator.DocumentError as reason:
        error(f"{config_filename} is invalid: {reason}")
    if not valid:
        error(f"{config_filename} is invalid: {flatten_errors(validator.errors)}")


def flatten_errors(error_message: Union[Dict, List, str]) -> str:
    """Flatten Cerberus' error messages."""
    def flatten_dict(error_dict: Dict) -> str:
        """Return a string version of the dict."""
        return ", ".join([f"{key}: {flatten_errors(value)}" for key, value in error_dict.items()])

    def flatten_list(error_list: List) -> str:
        """Return a string version of the list."""
        return ", ".join([flatten_errors(item) for item in error_list])

    if isinstance(error_message, dict):
        return flatten_dict(error_message)
    if isinstance(error_message, list):
        return flatten_list(error_message)
    return error_message
