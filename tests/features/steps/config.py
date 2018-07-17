"""Generate the configuration file."""

from asserts import assert_equal


@when("the user asks for a configuration file")
def generate_config_file(context):
    # In addition to --write-config-file, also add --config to the default config file isn't read.
    context.arguments.extend(["--write-config-file", "--config"])

@then("Next-action shows the default configuration file")
def check_config_file(context):
    assert_equal("""# Configuration file for Next-action. Edit the settings below as you like.
file: ~/todo.txt
number: 1
reference: multiple
style: default
""", context.next_action())
