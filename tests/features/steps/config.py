"""Generate the configuration file."""

@when("the user asks for a configuration file")
def generate_config_file(context):
    context.arguments.append("--write-config-file")

@then("Next-action shows the default configuration file")
def check_config_file(context):
    assert "number: 1" in context.next_action()
