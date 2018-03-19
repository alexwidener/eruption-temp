"""Integration tests for Eruption. """
# import built-in modules
import inspect
import os
import unittest

# import local modules
from eruption import eruption


def get_caller_name():
    current_frame = inspect.currentframe()
    caller_frame = inspect.getouterframes(current_frame, 2)
    return caller_frame[1][3]


class TestRocketchat(unittest.TestCase):
    """Test for the Rocketchat related classes and decorators."""

    @classmethod
    def setUpClass(cls):
        cls.base_url = os.environ.get('ROCKETCHAT_BASE_URL')
        cls.token = os.environ.get('ROCKETCHAT_TOKEN')

    def setUp(self):
        """Reusable setup method between tests."""
        self.rocket_chat = eruption.RocketChat(base_url=self.base_url, token=self.token)

    def ensure_result_is_good(self, result):
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.reason, 'OK')
        self.assertEqual(result.text, '{"success":true}')

    def test_instantiation_post(self):
        """Ensure that instantiating the class and posting performs as expected."""
        caller_name = get_caller_name()
        result = self.rocket_chat.post('Integration test for {}'.format(caller_name))
        self.ensure_result_is_good(result)

    def test_decorator_instance_post(self):
        """Ensure that the decorator that takes an instance and posts performs as expected."""
        caller_name = get_caller_name()
        message = 'Integration test for {}'.format(caller_name)

        @eruption.rocketchat(message=message, instance=self.rocket_chat)
        def adder():
            return 1 + 1

        adder()
        # There is no assertion here on purpose.

    def test_decorator_new_instance_post(self):
        """Ensure that the decorator that creates a new instance and posts performs as expected."""
        caller_name = get_caller_name()
        message = 'Integration test for {}'.format(caller_name)

        @eruption.post_to_rocketchat(message=message, base_url=self.base_url, token=self.token)
        def adder():
            return 1 + 1

        adder()
        # There is no assertion here on purpose.


class TestDiscord(unittest.TestCase):
    """Tests for the Discord related classes and decorators."""

    @classmethod
    def setUpClass(cls):
        cls.room_id = os.environ.get('DISCORD_ROOM_ID')
        cls.token = os.environ.get('DISCORD_TOKEN')

    def setUp(self):
        """Reusable setup method between tests."""
        self.discord = eruption.Discord(room_id=self.room_id, token=self.token)

    def ensure_result_is_good(self, result):
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.reason, 'OK')
        self.assertEqual(result.text, '{"success":true}')

    def test_instantiation_post(self):
        """Ensure that instantiating the class and posting performs as expected."""
        caller_name = get_caller_name()
        result = self.discord.post('Integration test for {}'.format(caller_name))
        self.ensure_result_is_good(result)

    def test_decorator_instance_post(self):
        """Ensure that the decorator that takes an instance and posts performs as expected."""
        caller_name = get_caller_name()
        message = 'Integration test for {}'.format(caller_name)

        @eruption.discord(message=message, instance=self.discord)
        def adder():
            return 1 + 1

        adder()
        # There is no assertion here on purpose.

    def test_decorator_new_instance_post(self):
        """Ensure that the decorator that creates a new instance and posts performs as expected."""
        caller_name = get_caller_name()
        message = 'Integration test for {}'.format(caller_name)

        @eruption.post_to_discord(message=message, room_id=self.room_id, token=self.token)
        def adder():
            return 1 + 1

        adder()
        # There is no assertion here on purpose.


class TestHipchat(unittest.TestCase):
    def test_instantiation_post(self):
        """Ensure that instantiating the class and posting performs as expected."""
        self.fail()

    def test_decorator_instance_post(self):
        """Ensure that the decorator that takes an instance and posts performs as expected."""
        self.fail()

    def test_decorator_new_instance_post(self):
        """Ensure that the decorator that creates a new instance and posts performs as expected."""
        self.fail()


class TestSlack(unittest.TestCase):
    def test_instantiation_post(self):
        """Ensure that instantiating the class and posting performs as expected."""
        self.fail()

    def test_decorator_instance_post(self):
        """Ensure that the decorator that takes an instance and posts performs as expected."""
        self.fail()

    def test_decorator_new_instance_post(self):
        """Ensure that the decorator that creates a new instance and posts performs as expected."""
        self.fail()


class TestMattermost(unittest.TestCase):
    def test_instantiation_post(self):
        """Ensure that instantiating the class and posting performs as expected."""
        self.fail()

    def test_decorator_instance_post(self):
        """Ensure that the decorator that takes an instance and posts performs as expected."""
        self.fail()

    def test_decorator_new_instance_post(self):
        """Ensure that the decorator that creates a new instance and posts performs as expected."""
        self.fail()


if __name__ == '__main__':
    unittest.main()
