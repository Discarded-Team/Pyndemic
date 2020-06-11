import random
import string
import inspect


class ContextError(Exception):
    pass


class ContextNotFoundError(ContextError):
    pass


class _ContextManager:
    _contexts = {}


def register_context(context_id, context):
    if context_id in _ContextManager._contexts:
        raise ContextError(
            f'Such context is already present: {context_id}')
    _ContextManager._contexts[context_id] = context


def unregister_context(context_id):
    if context_id not in _ContextManager._contexts:
        raise ContextNotFoundError(
            f'Such context is not registered: {context_id}')

    _ContextManager._contexts.pop(context_id)


def get_context(context_id):
    try:
        context = _ContextManager._contexts[context_id]
    except KeyError:
        raise ContextNotFoundError(
            f'Such context is not registered: {context_id}')

    return context


# TODO: regenerate when conflict occures
def generate_id():
    context_id = ''.join(
        random.choice(string.ascii_lowercase) for _ in range(8))
    return context_id


def search_context():
    """Find the nearest caller object posed as "self" with game context
    (if exists) and return its context.
    Otherwise, return None.
    """
    frame = inspect.currentframe()
    try:
        while frame is not None:
            if 'self' not in frame.f_locals:
                frame = frame.f_back
                continue

            calling_object = frame.f_locals['self']
            if hasattr(calling_object, '_ctx'):
                ctx = calling_object._ctx
                return ctx

            frame = frame.f_back
    finally:
        del frame

    return None


class ContextRegistrationMeta(type):
    """When a class instance is created with this class builder, it creates a
    new game context attached to it.
    """
    def __new__(mcs, name, bases, attrs, **options):
        return super().__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs, **options):
        if hasattr(cls, '_ctx_name'):
            return
        cls._ctx_name = options.get('ctx_name') or cls.__name__.lower()

    def __call__(cls, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)

        context_id = generate_id()
        ctx = {
            cls._ctx_name: obj,
            'id': context_id,
        }

        register_context(context_id, ctx)
        obj._ctx = ctx

        return obj
