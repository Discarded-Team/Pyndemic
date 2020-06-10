from unittest import TestCase

from pyndemic.core.context import (ContextError, ContextNotFoundError,
                                   register_context, unregister_context,
                                   get_context, generate_id, search_context,
                                   ContextRegistrationMeta, _ContextManager)


class ContextManagerTestCase(TestCase):
    mock_context = 'mock_string_instead_of_an_object'

    def setUp(self):
        self.contexts = _ContextManager._contexts

    def tearDown(self):
        self.contexts.clear()

    def test_register_context(self):
        """A comprehensive test for registering, getting and unregistering
        contexts.
        """
        register_context(42, self.mock_context)
        self.assertIn(42, self.contexts)
        self.assertEqual(self.mock_context, self.contexts[42])

        another_context = 'another_mock_string_instead_of_an_object'
        with self.assertRaises(ContextError):
            register_context(42, another_context)

    def test_get_context(self):
        self.contexts[42] = self.mock_context
        ctx = get_context(42)
        self.assertEqual(ctx, self.mock_context)

        with self.assertRaises(ContextNotFoundError):
            get_context(43)

    def test_unregister_context(self):
        self.contexts[42] = self.mock_context
        unregister_context(42)
        self.assertNotIn(42, self.contexts)

        with self.assertRaises(ContextNotFoundError):
            unregister_context(42)

    def test_generate_id(self):
        ctx_id_1 = generate_id()
        self.assertIsNotNone(ctx_id_1)
        self.assertIsInstance(ctx_id_1, str)

        ctx_id_2 = generate_id()
        self.assertNotEqual(ctx_id_1, ctx_id_2)

    def test_search_context(self):
        self._ctx = self.mock_context
        ctx = search_context()
        self.assertEqual(self._ctx, ctx)

        del self._ctx
        ctx = search_context()
        self.assertIsNone(ctx)


class ContextRegistrationMetaTestCase(TestCase):
    def construct_context_creator_mock_class(self, ctx_name=None):
        if ctx_name is None:
            class MockContextCreator(metaclass=ContextRegistrationMeta):
                pass
        else:
            class MockContextCreator(metaclass=ContextRegistrationMeta,
                                     ctx_name=ctx_name):
                pass

        return MockContextCreator

    def setUp(self):
        self.contexts = _ContextManager._contexts

    def tearDown(self):
        self.contexts.clear()

    def test_init(self):
        test_class = self.construct_context_creator_mock_class()
        default_ctx_name = test_class.__name__.lower()
        self.assertTrue(hasattr(test_class, '_ctx_name'))
        self.assertEqual(default_ctx_name, test_class._ctx_name)

        test_class = self.construct_context_creator_mock_class(ctx_name='mock')
        self.assertTrue(hasattr(test_class, '_ctx_name'))
        self.assertEqual('mock', test_class._ctx_name)

    def test_call(self):
        test_class = self.construct_context_creator_mock_class(
            ctx_name='test_context')

        instance = test_class()
        self.assertTrue(hasattr(instance, '_ctx'))

        ctx = instance._ctx
        self.assertIn('id', ctx)
        context_id = ctx['id']
        self.assertIn(context_id, self.contexts)
        self.assertIs(self.contexts[context_id], ctx)

        ctx_registered_instance = ctx['test_context']
        self.assertIs(ctx_registered_instance, instance)
