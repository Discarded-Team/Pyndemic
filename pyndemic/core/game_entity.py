import inspect
import logging

from .context import ContextError
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

        try:
            frame = inspect.currentframe()
            while frame is not None:
                frame = frame.f_back
                if 'self' in frame.f_locals:
                    break
            calling_object = frame.f_locals['self']
            ctx = calling_object._ctx
        except (KeyError, AttributeError):
            logging.warning(
                f'Creating game object "{obj}" with no context attached.')
            ctx = {}
        finally:
            del frame

        obj._ctx = ctx

        return obj


class GameEntity(metaclass=GameEntityCreationMeta):
    """Base class for every game object."""
    signals_enabled = True

    def emit_signal(self, message, log_level=logging.INFO):
        if not self.signals_enabled:
            return

        if not hasattr(self, '_ctx'):
            raise ContextError(
                (f'Object {self} cannot emit signals because it is created '
                 'outside any game context.'))

        if 'controller_weakref' not in self._ctx:
            raise ContextError(
                (f'Cannot find signal receiver for this object {self} - '
                 'game context is empty.'))

        controller = self._ctx['controller_weakref']()

        if controller is None:
            raise ContextError(
                (f'The context for this object ({self}) was destroyed and is '
                 'no longer available'))

        if isinstance(message, str):
            signal = api.message_response(message)
        else:
            signal = message

        if log_level is not None:
            logging.log(log_level, signal)

        controller.signals.put(signal)
