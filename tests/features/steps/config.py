"""Generate the configuration file."""

import os
import stat
import tempfile

from asserts import assert_equal, assert_in
from behave import given, when, then


@given("a configuration file with")
def config_file(context):
    """Add the contents to the temporary configuration file."""
    context.config_file = tempfile.NamedTemporaryFile(mode="w")
    text = []
    in_file_list = False
    for line in context.text.split("\n"):
        if line.startswith("file: "):
            filename = line[len("file: "):]
            text.append("file: " + temporary_filename(context, filename))
        elif in_file_list and line.startswith("- "):
            filename = line[len("- "):]
            text.append("- " + temporary_filename(context, filename))
        else:
            text.append(line)
        in_file_list = line.startswith("file:") or in_file_list and line.startswith("- ")
    context.config_file.write("\n".join(text))
    context.config_file.seek(0)
    context.arguments.extend(["--config-file", context.config_file.name])


def temporary_filename(context, filename):
    """Match the filenames in the config file to the temporary files' names."""
    for file in context.files:
        if file.given_filename == filename:
            return file.name


@when("the user asks for a configuration file")
def generate_config_file(context):
    """In addition to --write-config-file, also add --config so the default config file isn't read."""
    context.arguments.extend(["--write-config-file", "--config"])


@when("the user specifies a configuration file that doesn't exist")
def non_existing_config_file(context):
    """Specify a non-existing configuration file."""
    context.arguments.extend(["--config", "non-existing-next-action-configuration-file.cfg"])


@when("the user specifies a configuration file that can't be read")
def unreadable_config_file(context):
    """Specify an unreadable configuration file."""
    context.config_file = tempfile.NamedTemporaryFile(mode="w")
    os.chmod(context.config_file.name, ~stat.S_IREAD)
    context.arguments.extend(["--config", context.config_file.name])


@when("the user specifies a configuration file that is empty")
def empty_config_file(context):
    """Specify an empty configuration file."""
    context.config_file = tempfile.NamedTemporaryFile(mode="w")
    context.arguments.extend(["--config", context.config_file.name])


@when("the user specifies the {argument}-argument with value {value}")
def cli_argument(context, argument, value):
    """Add command line argument."""
    context.arguments.extend(["--" + argument, value])


@when("the user specifies the {option}-option")
def cli_option(context, option):
    """Add command line option."""
    context.arguments.extend(["--" + option])


@when("the user specifies a {filter_type}-filter")
def cli_filter_option(context, filter_type):
    """Add command line filter."""
    filter_option = "@home" if filter_type == "context" else "+Project"
    context.arguments.extend(["--", filter_option])


@then("Next-action shows the default configuration file")
def check_default_config(context):
    """Check that Next-action returns the default YAML configuration file."""
    assert_equal(f"""# Configuration file for Next-action. Edit the settings below as you like.
file: ~/todo.txt
number: 1
reference: multiple
style: default
""", context.next_action())


@then("Next-action includes the {argument}-argument with value {value} in the configuration file")
def check_config_argument(context, argument, value):
    """Check that Next-action includes the argument in the configuration file."""
    assert_in(argument + ": " + value, context.next_action())


@then("Next-action includes the {option}-option in the configuration file")
def check_config_option(context, option):
    """Check that Next-action includes the option in the configuration file."""
    assert_in(option + ": true", context.next_action())


@then("Next-action includes the {filter_type}-filter in the configuration file")
def check_config_filter(context, filter_type):
    """Check that Next-action includes the filter in the configuration file."""
    filter_option = "'@home'" if filter_type == "context" else "+Project"
    assert_in("filters:\n- " + filter_option, context.next_action())


@then("Next-action tells the user it can't read the configuration file")
def non_existing_config_file_error(context):
    """Check that Nect-action gives the correct error message."""
    assert_in("next-action: error: can't open file:", context.next_action())


@then("Next-action tells the user it can't parse the configuration file")
def parse_config_file_error(context):
    """Check that Nect-action gives the correct error message."""
    assert_in(f"next-action: error: can't parse {context.config_file.name}:", context.next_action())


@then("Next-action tells the user the configuration file is invalid")
def invalid_config_file_error(context):
    """Check that Nect-action gives the correct error message."""
    assert_in(f"next-action: error: {context.config_file.name} is invalid:", context.next_action())
