"""An easy, light-weight lib for posting to multiple chat channels. Does nothing more than using webhooks to post to
channels that you give it the information to post to. Additionally, decorators are included in the event that you want
to post to channels whenever a certain method finishes executing. Additionally, all services are capable of being
run from the command line.
"""


# import built-in modules
import json

# import 3rd party modules
import requests

__all__ = [
    'Discord',
    'HipChat',
    'Messenger',
    'Slack',
    'RocketChat',
    'Mattermost',
    'post_to_discord',
    'post_to_hipchat',
    'post_to_slack',
    'post_to_rocketchat',
    'post_to_mattermost',
    'discord',
    'hipchat',
    'slack',
    'rocketchat',
    'mattermost'
]


class Messenger(object):

    url_template = ''
    room_url = ''

    def __init__(self, room_id, token, **kwargs):
        self.room_id = room_id
        self.token = token

        if kwargs.get('url_template'):
            self.url_template = kwargs.get('url_template')

        self.headers = {
            'Authorization': 'Bearer {0}'.format(self.token),
            'Content-type': 'application/json'
        }

    def _process_data(self, *args, **kwargs):
        raise NotImplementedError

    def post(self, *args, **kwargs):
        data = self._process_data(*args, **kwargs)
        result = requests.post(
            url=self.room_url,
            data=data,
            headers=self.headers
        )
        return result


class Slack(Messenger):

    url_template = 'https://hooks.slack.com/services/{channel}/{room_id}/{token}'

    def __init__(self, room_id, token, channel, **kwargs):
        super(Slack, self).__init__(room_id=None, token=token, **kwargs)
        self.room_id = room_id
        self.token = token
        self.channel = channel
        self.room_url = self.url_template.format(
            room_id=self.room_id,
            token=self.token,
            channel=self.channel)

    def _process_data(self, *args, **kwargs):
        data = {
            'text': args[0],
            'channel': kwargs.get('channel', '#general'),
            'username': kwargs.get('user_name', 'David Bowie'),
            'icon_emoji': kwargs.get('icon_emoji', ':ghost:')
        }

        return json.dumps(data.update(**kwargs) if kwargs else data)


class HipChat(Messenger):

    url_template = ''

    def _process_data(self, *args, **kwargs):
        data = {
            'message': args[0],
            'notify': kwargs.get('notify', True),
            'color': kwargs.get('color', 'blue'),
            'message_format': kwargs.get('message_format', 'text')
        }

        return json.dumps(data.update(**kwargs) if kwargs else data)


class Mattermost(Messenger):

    url_template = 'http://{base_url}/hooks/{token}'

    def __init__(self, token, base_url, **kwargs):
        super(Mattermost, self).__init__(room_id=None, token=token, **kwargs)
        self.token = token
        self.base_url = base_url
        self.room_url = self.url_template.format(token=self.token, base_url=self.base_url)

    def _process_data(self, *args, **kwargs):
        data = {
            'text': args[0],
            'username': kwargs.get('user_name', 'David Bowie'),
            'channel': kwargs.get('channel', 'town-square')
        }

        return json.dumps(data.update(**kwargs) if kwargs else data)


class RocketChat(Messenger):
    url_template = 'http://{base_url}/hooks/{token}'

    def __init__(self, base_url, token, **kwargs):
        super(RocketChat, self).__init__(room_id=None, token=token, **kwargs)
        self.base_url = base_url
        self.token = token
        self.room_url = self.url_template.format(
            base_url=self.base_url,
            token=self.token)

    def _process_data(self, *args, **kwargs):
        data = {
            'text': args[0],
            "channel": kwargs.get('channel', "#general"),
            "username": kwargs.get('user_name', 'monkey-bot'),
            "icon_emoji": kwargs.get('icon_emoji', ':monkey_face:')
        }

        return json.dumps(data.update(**kwargs) if kwargs else data)


class Discord(Messenger):
    url_template = 'https://discordapp.com/api/webhooks/{room_id}/{token}'

    def _process_data(self, *args, **kwargs):
        data = {
            'content': args[0],
            'username': kwargs.get('user_name', 'David Bowie'),
        }
        return json.dumps(data.update(**kwargs) if kwargs else data)


def post_to_mattermost(message, token, base_url='localhost:8065', data=None):
    """Decorator for posting to Mattermost.

    Args:
        message (str): The message to post.
        token (str): The authorization token to use.
        base_url (str): The base URL to use, default is 'localhost:8065'.
        data (dict): Any extra data to include in the payload.

    Returns:

    """
    def process(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            instance = Mattermost(
                token=token,
                base_url=base_url)
            instance.post(message, kwargs.update(data) if data else kwargs)
        return wrapper
    return process


def mattermost(message, instance, data=None):
    """Decorator for posting to a Mattermost instance.

    Args:
        message (str): The message to post.
        instance (Mattermost): The Mattermost instance to use.
        data (dict): Any extra data to include in the payload.

    Returns:
        callable:
    """
    return messenger(message, instance, data)


def post_to_discord(message, room_id, token, data=None):
    """Decorator for posting to Discord.

    Args:
        message (str): The message to post.
        room_id (str):
        token (str): The authorization token to use.
        data (dict): Any extra data to include in the payload.

    Returns:

    """
    def process(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            instance = Discord(
                room_id=room_id,
                token=token)
            instance.post(message, kwargs.update(data) if data else kwargs)
        return wrapper
    return process


def messenger(message, instance, data):
    """Generic method called by

    Args:
        message (str): The message to post.
        instance (Messenger): The Messenger instance to use.
        data (dict): Any extra data to include in the payload.

    Returns:

    """
    def process(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            instance.post(message, kwargs.update(data) if data else kwargs)
        return wrapper
    return process


def discord(message, instance, data=None):
    """Decorator for posting to a Discord instance.

    Args:
        message (str): The message to post.
        instance (Messenger): The Discord instance to use.
        data (dict): Any extra data to include in the payload.

    Returns:

    """
    return messenger(message, instance, data)


def post_to_hipchat(message, room_id, token, data=None):
    """Decorator for posting to Hipchat.

    Args:
        message (str): The message to post.
        room_id (str): The ID of the group to post to.
        token (str): The authorization token to use.
        data (dict): Any extra data to include in the payload.

    Returns:
        callable:
    """
    def process(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            instance = HipChat(room_id=room_id, token=token)
            instance.post(message, kwargs.update(data) if data else kwargs)
        return wrapper
    return process


def hipchat(message, instance, data=None):
    """Decorator to post a message to a Hipchat instance.

    Args:
        message (str): The message to post.
        instance (HipChat): The Hipchat instance to use.
        data (dict): Any extra data to include in the payload.

    Returns:

    """
    return messenger(message, instance, data)


def post_to_slack(message, room_id, channel, token, data=None):
    """Decorator for posting to Slack.

    Args:
        message (str): The message to post.
        room_id (str): The id of the group.
        channel (str): The channel to post to.
        token (str): The authorization token to use.
        data (dict): Any extra data to include in the payload.

    Returns:

    """
    def process(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            instance = Slack(
                room_id=room_id,
                channel=channel,
                token=token)
            instance.post(message, kwargs.update(data) if data else kwargs)
        return wrapper
    return process


def slack(message, instance, data=None):
    """Decorator for posting a Slack instance.

    Args:
        message (str): The message to post.
        instance (Slack): The Slack instance to use.
        data (dict): Any overriding information for the payload.

    Returns:

    """
    return messenger(message, instance, data)


def post_to_rocketchat(message, base_url, token, data=None):
    """Decorator for posting to Rocketchat.

    Args:
        message (str): The message to post.
        base_url (str): The base url to post to.
        token (str): The token to use.
        data (dict): Any overriding information for the payload.

    Returns:

    """
    def process(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            instance = RocketChat(
                base_url=base_url,
                token=token)
            instance.post(message, kwargs.update(data) if data else kwargs)
        return wrapper
    return process


def rocketchat(message, instance, data=None):
    """Decorator for posting to Rocketchat.

    Args:
        message (str): The message to post.
        instance (Messenger):
        data (dict): Any overriding information for the payload.

    Returns:

    """
    return messenger(message, instance, data)
