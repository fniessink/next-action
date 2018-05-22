""" Methods for reading, parsing, and validating Next-action configuration files. """

import os
from typing import Callable

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


def validate_config_file(config, config_filename: str, error: Callable[[str], None]) -> None:
    """ Validate the configuration file contents. """
    schema = {
        "file": {
            "type": ["string", "list"],
            "schema": {
                "type": "string"}},
        "number": {
            "type": ["integer"],
            "min": 1,
            "excludes": "all"
        },
        "all": {
            "type": "boolean",
            "allowed": [True]
        }
    }
    validator = cerberus.Validator(schema)
    try:
        valid = validator.validate(config)
    except cerberus.validator.DocumentError as reason:
        error("{0} is invalid: {1}".format(config_filename, reason))
    if not valid:
        error("{0} is invalid: {1}".format(config_filename, validator.errors))
