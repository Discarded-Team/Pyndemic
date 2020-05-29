import unittest
from pyndemic.core.context import ContextError, ContextNotFoundError, \
    ContextRegistrationMeta, register_context, unregister_context, \
    get_context, generate_id


class ContextManagerTestCase(unittest.TestCase):
    def test_register_unregister(self):
        """A comprehensive test for registring, getting and unregistering
        the context"""
        mock_context = "mock_string_instead_of_an_object"
        register_context(42, mock_context)

        # register a conflicting context
        with self.assertRaises(ContextError):
            register_context(42, "mock_string_instead_of_an_object")

        # get the existing context
        ctx = get_context(42)
        self.assertEqual(ctx, mock_context)

        unregister_context(42)

        # get a non-existing context
        with self.assertRaises(ContextNotFoundError):
            get_context(42)

        # unregister a non-existing context
        with self.assertRaises(ContextNotFoundError):
            unregister_context(42)

    def test_generate_id(self):
        ctx_id_1 = generate_id()
        self.assertIsNotNone(ctx_id_1)
        self.assertIsInstance(ctx_id_1, str)
        self.assertEqual(8, len(ctx_id_1))

        ctx_id_2 = generate_id()
        self.assertNotEqual(ctx_id_1, ctx_id_2)


class MockController(metaclass=ContextRegistrationMeta,
                     ctx_name='mock_controller'):
    pass


class ContextMetaClassTestCase(unittest.TestCase):
    def test_context(self):
        mock = MockController()
        self.assertIsNotNone(mock._ctx)

