import unittest
from unittest.mock import patch
from pyndemic.core.context import ContextRegistrationMeta, ContextError
from pyndemic.core import api
from queue import Queue


from pyndemic.core.game_entity import GameEntity


class DumbQueue:
    def __init__(self):
        self.queue = list()

    def put(self, something):
        self.queue.append(something)

    def get(self):
        return self.queue.pop(0)


class GameEntityTestCase(unittest.TestCase):
    def construct_controller_mock_class(self):
        class MockController(metaclass=ContextRegistrationMeta,
                             ctx_name='controller'):
            def __init__(self):
                self.signals = DumbQueue()

            def create_entity(self):
                return GameEntity()

        return MockController

    def setUp(self):
        controller_class = self.construct_controller_mock_class()
        self.controller = controller_class()

    def test_assert_has_context(self):
        with self.assertRaises(ContextError):
            self.entity = GameEntity()
            self.entity.assert_has_context()

    def test_emit_signal(self):
        self.entity = self.controller.create_entity()
        self.entity.signals_enabled = True
        self.entity.emit_signal("message")
        received = self.controller.signals.get()
        required = api.message_response("message")
        self.assertEqual(required, received)
