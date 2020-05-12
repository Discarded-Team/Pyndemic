import inspect
import logging

from .context import get_context, ContextError
from .. import api

class GameEntityCreationMeta(type):
    """This class builder ensures that the object created as an instance of
    that class will get access to the context kept by the object that caused
    the creation of this instance.
    If caller object context is not present, the instance contest will also be
    undefined.
    """
    def __call__(cls, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)

        upper_stack_frame = inspect.stack()[1].frame
        try:
            calling_object = upper_stack_frame.f_locals['self']
            ctx = calling_object._ctx
        except (KeyError, AttributeError):
            logging.warning(
                f'Creating game object "{obj}" with no context attached.')
            ctx = None
        finally:
            del upper_stack_frame

        obj._ctx = ctx

        return obj


class GameEntity(metaclass=GameEntityCreationMeta):
    """Base class for every game object."""
    def emit_signal(self, message):
        if not hasattr(self, '_context_id'):
            raise ContextError(
                (f'Object {self} cannot emit signals because it is created '
                 'outside any game context.'))

        controller = self._ctx['controller_weakref']()

        if controller is None:
            raise ContextError(
                (f'The context for this object ({self}) was destroyed and is '
                 'no longer available'))

        if isinstance(message, str):
            signal = api.message_response(message)
        else:
            signal = message

        controller.signals.put(signal)
