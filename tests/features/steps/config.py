"""Generate the configuration file."""

from asserts import assert_equal, assert_in
from behave import when, then


@when("the user asks for a configuration file")
def generate_config_file(context):
    """In addition to --write-config-file, also add --config so the default config file isn't read."""
    context.arguments.extend(["--write-config-file", "--config"])


@when("the user specifies the {argument}-argument with value {value}")
def cli_argument(context, argument, value):
    """Add command line argument."""
    context.arguments.extend(["--" + argument, value])


@when("the user specifies the {option}-option")
def cli_option(context, option):
    """Add command line option."""
    context.arguments.extend(["--" + option])


@when("the user specifies a {filter_type}-filter")
def cli_option(context, filter_type):
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
