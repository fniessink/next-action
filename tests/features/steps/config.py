"""Generate the configuration file."""

from asserts import assert_equal
from behave import when, then


@when("the user asks for a configuration file")
def generate_config_file(context):
    """In addition to --write-config-file, also add --config so the default config file isn't read."""
    context.arguments.extend(["--write-config-file", "--config"])

@when("the user specifies a file argument")
def file_argument(context):
    """Add file argument."""
    context.arguments.extend(["--file", "my_todo.txt"])


@then("Next-action shows the default configuration file")
def check_default_config(context):
    """Check that Next-action returns the default YAML configuration file."""
    assert_equal(f"""# Configuration file for Next-action. Edit the settings below as you like.
file: ~/todo.txt
number: 1
reference: multiple
style: default
""", context.next_action())


@then("Next-action shows the default configuration file with the file argument")
def check_config_file(context):
    """Check that Next-action returns the default YAML configuration file."""
    assert_equal("""# Configuration file for Next-action. Edit the settings below as you like.
file: my_todo.txt
number: 1
reference: multiple
style: default
""", context.next_action())
