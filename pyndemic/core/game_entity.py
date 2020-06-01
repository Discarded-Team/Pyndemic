import logging

from .context import ContextError, search_context
from . import api


class GameEntityCreationMeta(type):
    """This class builder ensures that the object created as an instance of
    that class will get access to the context kept by the object that caused
    the creation of this instance.
    If caller object context is not present, the instance contest will also be
    undefined.
    """
    def __call__(cls, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)

        ctx = search_context()
        if not ctx:
            logging.warning(
                f'Creating game object "{obj}" with no context attached.')
            ctx = {}

        obj._ctx = ctx

        return obj


class GameEntity(metaclass=GameEntityCreationMeta):
    """Base class for every game object."""
    signals_enabled = True

    def assert_has_context(self):
        try:
            self._ctx['id']
        except (LookupError, AttributeError):
            raise ContextError(
                (f'Object {self} attempts to perform context-dependent '
                 'procedure but is outside any game context or has invalid '
                 'context.'))

    def emit_signal(self, message, log_level=logging.INFO):
        if not self.signals_enabled:
            logging.debug(
                (f'Attempting to send a message ({message}) from {self}, '
                 'however, signal emitting is disabled.'))
            return

        self.assert_has_context()

        if 'controller' not in self._ctx:
            raise ContextError(
                (f'Cannot find signal receiver for this object {self} - '
                 'game context is empty.'))

        controller = self._ctx['controller']

        if isinstance(message, str):
            signal = api.message_response(message)
        else:
            signal = message

        if log_level is not None:
            logging.log(log_level, signal)

        controller.signals.put(signal)
