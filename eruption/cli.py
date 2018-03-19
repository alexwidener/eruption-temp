import click
import eruption


# Configuration key will be base for everything, unless given an explicit argument which will be treated as an
# override
CONFIGURATION_KEY = __name__ + '.configuration'

# Configuration keys
CONFIGURATION_BASE_URL = 'base_url'
CONFIGURATION_TOKEN = 'token'
CONFIGURATION_ROOM_ID = 'room_id'
CONFIGURATION_CHANNEL = 'channel'
CONFIGURATION_ICON = 'icon'
CONFIGURATION_USER_NAME = 'user_name'


MESSAGE_KEY = __name__ + '.message'
BASE_URL_KEY = __name__ + '.base_url'
ROOM_ID_KEY = __name__ + '.room_id'
TOKEN_KEY = __name__ + '.token'
CHANNEL_KEY = __name__ + '.channel'
ICON_KEY = __name__ + '.icon'
USER_NAME_KEY = __name__ + '.user_name'

# TODO (Alex): Needed?
OVERRIDES_KEY = __name__ + '.overrides'


@click.group(
    name='eruption',
    invoke_without_command=False)
@click.pass_context
def cli(context):
    print('Going to load the configuration information here')
    # context.meta['GET_ME'] = 'information'
    print('running cli')


def set_message(context, parameters, value):
    """Set the message on the Click Context.

    Args:
        context (click.Context): The Click Context to use.
        parameters (click.ParamType): The Parameter being inspected (ignored).
        value (str): The value to set for the message on the context.
    """
    if value:
        context.meta[MESSAGE_KEY] = value


def set_base_url(context, parameters, value):
    """Set the server's base url on the Click Context.

    Args:
        context (click.Context): The Click Context to use.
        parameters (click.ParamType): The Parameter being inspected (ignored).
        value (str): The value to set for the message on the context.
    """
    if value:
        context.meta[BASE_URL_KEY] = value


def set_room_id(context, parameters, value):
    """Set the server's room id on the Click Context.

    Args:
        context (click.Context): The Click Context to use.
        parameters (click.ParamType): The Parameter being inspected (ignored).
        value (str): The value to set for the message on the context.
    """
    if value:
        context.meta[ROOM_ID_KEY] = value


def set_token(context, parameters, value):
    """Set the token on the Click Context.

    Args:
        context (click.Context): The Click Context to use.
        parameters (click.ParamType): The Parameter being inspected (ignored).
        value (str): The value to set for the message on the context.
    """
    if value:
        context.meta[TOKEN_KEY] = value


def set_icon(context, parameters, value):
    """Set the icon on the Click context.

    Args:
        context (click.Context): The Click Context to use.
        parameters (click.ParamType): The Parameter being inspected (ignored).
        value (str): The value to set for the message on the context.
    """
    if value:
        context.meta[ICON_KEY] = value


def set_channel(context, parameters, value):
    """Set the token on the Click Context.

    Args:
        context (click.Context): The Click Context to use.
        parameters (click.ParamType): The Parameter being inspected (ignored).
        value (str): The value to set for the message on the context.
    """
    if value:
        context.meta[CHANNEL_KEY] = value


def set_user_name(context, parameters, value):
    """Set the user name on the Click Context.

    Args:
        context (click.Context): The Click Context to use.
        parameters (click.ParamType): The Parameter being inspected (ignored).
        value (str): The value to set for the message on the context.
    """
    if value:
        context.meta[USER_NAME_KEY] = value


# def set_overrides(context, parameters, value):
#     """Set the message overrides on the Click Context.
#
#     Args:
#         context (click.Context): The Click Context to use.
#         parameters (click.ParamType): The Parameter being inspected (ignored).
#         value (str): The value to set for the message on the context.
#     """
#     if value:


@cli.command(
    name='discord',
    short_help='Post the given message to Discord')
@click.option(
    '-m', '--message',
    expose_value=False,
    callback=set_message)
@click.pass_context
def discord(context):
    print('ran discord')
    print('Received {}'.format(context))
    print('And it contains {}'.format(context.meta.get('GET_ME')))
    print('Obviously still need to finish this.')


@cli.command(
    name='rocketchat',
    short_help='Post the given message to Rocketchat')
@click.option(
    '-m', '--message',
    expose_value=False,
    callback=set_message)
@click.option(
    '-b', '--base-url',
    expose_value=False,
    callback=set_base_url,
    required=False)
@click.option(
    '-t', '--token',
    expose_value=False,
    callback=set_token,
    required=False)
@click.option(
    '-c', '--channel',
    expose_value=False,
    callback=set_channel,
    required=False)
@click.option(
    '-u', '--user_name',
    expose_value=False,
    callback=set_user_name,
    required=False)
@click.option(
    '-i', '--icon-emoji',
    expose_value=False,
    callback=set_icon,
    required=False)
@click.pass_context
def rocketchat(context):
    message = context.meta.get(MESSAGE_KEY)
    configuration = context.meta.get(CONFIGURATION_KEY)
    base_url = context.meta.get(BASE_URL_KEY) or configuration.get('base_url')




if __name__ == '__main__':
    cli()
