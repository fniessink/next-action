""" Methods for reading, parsing, and validating Next-action configuration files. """

import os
import sys
from typing import Callable, Dict, List, Union

from pygments.styles import get_all_styles
import yaml
import cerberus


def read_config_file(filename: str, default_filename: str, error: Callable[[str], None]):
    """ Read and parse the configuration file. """
    try:
        with open(os.path.expanduser(filename), "r") as config_file:
            return yaml.safe_load(config_file.read())
    except FileNotFoundError as reason:
        if filename == default_filename:
            return dict()  # Don't complain if there's no configuration file at the default location
        else:
            error("can't open file: {0}".format(reason))
    except OSError as reason:
        error("can't open file: {0}".format(reason))
    except yaml.YAMLError as reason:
        error("can't parse {0}: {1}".format(filename, reason))


def write_config_file() -> None:
    """ Generate a configuration file on standard out. """
    intro = "# Configuration file for Next-action. Edit the settings below as you like.\n"
    config = yaml.dump(dict(file="~/todo.txt", number=1, style="default"), default_flow_style=False)
    sys.stdout.write(intro + config)


def validate_config_file(config, config_filename: str, error: Callable[[str], None]) -> None:
    """ Validate the configuration file contents. """
    schema = {
        "file": {
            "type": ["string", "list"],
            "schema": {
                "type": "string"}},
        "number": {
            "type": "integer",
            "min": 1,
            "excludes": "all"
        },
        "all": {
            "type": "boolean",
            "allowed": [True]
        },
        "style": {
            "type": "string",
            "allowed": sorted(list(get_all_styles()))
        }
    }
    validator = cerberus.Validator(schema)
    try:
        valid = validator.validate(config)
    except cerberus.validator.DocumentError as reason:
        error("{0} is invalid: {1}".format(config_filename, reason))
    if not valid:
        error("{0} is invalid: {1}".format(config_filename, flatten_errors(validator.errors)))


def flatten_errors(error_message: Union[Dict, List, str]) -> str:
    """ Flatten Cerberus' error messages. """

    def flatten_dict(error_dict: Dict) -> str:
        """ Return a string version of the dict. """
        return ", ".join(["{0}: {1}".format(key, flatten_errors(value)) for key, value in error_dict.items()])

    def flatten_list(error_list: List) -> str:
        """ Return a string version of the list. """
        return ", ".join([flatten_errors(item) for item in error_list])

    if isinstance(error_message, dict):
        return flatten_dict(error_message)
    elif isinstance(error_message, list):
        return flatten_list(error_message)
    return error_message
