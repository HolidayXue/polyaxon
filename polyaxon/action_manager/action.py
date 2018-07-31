import logging

import auditor

from action_manager.exception import PolyaxonActionException

logger = logging.getLogger("polyaxon.actions")


class Action(object):
    action_key = None
    name = None
    description = ''
    event_type = None
    raise_empty_context = True

    @classmethod
    def _validate_config(cls, config):
        """Validate that a given config is valid for the current config."""
        raise NotImplementedError

    @classmethod
    def _get_config(cls):
        """Getting config to execute an action.

        Currently we get config from env vars.
        """
        raise NotImplementedError

    @classmethod
    def get_config(cls, config=None):
        config = config or cls._get_config()
        config = cls._validate_config(config)
        return config

    @classmethod
    def _prepare(cls, context):
        """This is where you should alter the context to fit the action.

        Default behaviour will leave the context as it is.
        """
        if not context and cls.raise_empty_context:
            raise PolyaxonActionException('{} received invalid payload context.'.format(cls.name))

        return context

    @classmethod
    def _execute(cls, data, config):
        raise NotImplementedError

    @classmethod
    def execute(cls, context, config=None, from_user=None):
        config = cls.get_config(config=config)
        data = cls._prepare(context)
        result = cls._execute(data=data, config=config)
        auditor.record(event_type=cls.event_type,
                       automatic=from_user is None,
                       user=from_user)
        return result