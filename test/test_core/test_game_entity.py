from unittest import TestCase
from collections import deque

from pyndemic.core.context import ContextError
from pyndemic.core import api

from pyndemic.core.game_entity import GameEntity, GameEntityCreationMeta


class GameEntityCreationMetaTestCase(TestCase):
    def setUp(self):
        class DumbEntity(metaclass=GameEntityCreationMeta):
            pass

        self._ctx = {'id': 'foo', 'content': 'Funny content!'}
        self.test_class = DumbEntity

    def test_call(self):
        """Testing that every class created through GameEntityCreationMeta will
        perform context search for the instance. Here we use TestCase instance
        as a context holder and caller.
        """
        test_class = self.test_class
        instance = test_class()
        self.assertTrue(hasattr(instance, '_ctx'))
        self.assertIs(instance._ctx, self._ctx)

        del self._ctx
        instance = test_class()
        self.assertTrue(hasattr(instance, '_ctx'))
        self.assertEqual(instance._ctx, {})


class GameEntityTestCase(TestCase):
    def construct_controller_mock_class(self):
        """Help method for providing Controller-like class with "signals"
        attribute.
        """
        class MockController:
            def __init__(self):
                self.signals = deque()

        return MockController

    def setUp(self):
        controller_class = self.construct_controller_mock_class()
        self.controller = controller_class()
        self._ctx = {'id': 'mock_context', 'controller': self.controller}

    def test_assert_has_context(self):
        entity = GameEntity()
        entity.assert_has_context()

        del self._ctx
        with self.assertRaises(ContextError):
            entity = GameEntity()
            entity.assert_has_context()

    def test_emit_signal(self):
        entity = GameEntity()

        entity.signals_enabled = False
        entity.emit_signal("message")
        self.assertFalse(self.controller.signals)

        entity.signals_enabled = True
        entity.emit_signal("message")
        received = self.controller.signals.popleft()
        required = api.message_response("message")
        self.assertEqual(required, received)

    def test_emit_signal_without_context(self):
        del self._ctx
        entity = GameEntity()
        entity.signals_enabled = True

        with self.assertRaises(ContextError):
            entity.emit_signal("message")
