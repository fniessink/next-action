"""Unit tests for the warning module in the output package."""

from next_action import todotxt
from next_action.output.warning import invalid_arguments

from .. import fixtures


class InvalidArgumentsTest(fixtures.TestCaseWithNamespace):
    """Unit tests for the invalid argument warning method."""

    def setUp(self):
        """Set up the namespace with default arguments for all unit tests."""
        super().setUp()
        self.tasks = todotxt.Tasks()

    def test_no_args_and_no_tasks(self):
        """Test that the warning is empty if there are no tasks and no arguments."""
        self.assertEqual("", invalid_arguments(self.namespace, self.tasks))

    def test_missing_context(self):
        """Test the message with one missing context."""
        self.namespace.contexts = set(["home"])
        self.assertEqual(" (warning: unknown context: home)", invalid_arguments(self.namespace, self.tasks))

    def test_missing_contexts(self):
        """Test the message with two missing contexts."""
        self.namespace.contexts = set(["home", "work"])
        self.assertEqual(" (warning: unknown contexts: home, work)", invalid_arguments(self.namespace, self.tasks))

    def test_missing_project(self):
        """Test the message with one missing project."""
        self.namespace.projects = set(["DogHouse"])
        self.assertEqual(" (warning: unknown project: DogHouse)", invalid_arguments(self.namespace, self.tasks))

    def test_missing_projects(self):
        """Test the message with two missing projects."""
        self.namespace.projects = set(["DogHouse", "BigTrip"])
        self.assertEqual(" (warning: unknown projects: BigTrip, DogHouse)",
                         invalid_arguments(self.namespace, self.tasks))

    def test_missing_excluded_context(self):
        """Test the message with one missing excluded context."""
        self.namespace.excluded_contexts = set(["home"])
        self.assertEqual(" (warning: unknown context: home)", invalid_arguments(self.namespace, self.tasks))

    def test_missing_excluded_project(self):
        """Test the message with one missing excluded project."""
        self.namespace.excluded_projects = set(["DogHouse"])
        self.assertEqual(" (warning: unknown project: DogHouse)", invalid_arguments(self.namespace, self.tasks))

    def test_missing_context_project(self):
        """Test the message with one missing context and one missing project."""
        self.namespace.contexts = set(["home"])
        self.namespace.projects = set(["DogHouse"])
        self.assertEqual(" (warning: unknown context: home; unknown project: DogHouse)",
                         invalid_arguments(self.namespace, self.tasks))

    def test_present_context(self):
        """Test the message with one present context."""
        self.namespace.contexts = set(["home"])
        self.tasks.append(todotxt.Task("A task @home"))  # pylint: disable=no-member
        self.assertEqual("", invalid_arguments(self.namespace, self.tasks))
