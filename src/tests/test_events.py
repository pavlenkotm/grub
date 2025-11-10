"""
Tests for events module
"""

import unittest
from src.core.events import EventEmitter


class TestEventEmitter(unittest.TestCase):
    """Test cases for EventEmitter class"""

    def setUp(self):
        """Set up test fixtures"""
        self.emitter = EventEmitter()
        self.callback_count = 0
        self.callback_args = None

    def test_on_and_emit(self):
        """Test registering and emitting events"""
        def callback(value):
            self.callback_count += 1
            self.callback_args = value

        self.emitter.on("test_event", callback)
        count = self.emitter.emit("test_event", "test_value")

        self.assertEqual(count, 1)
        self.assertEqual(self.callback_count, 1)
        self.assertEqual(self.callback_args, "test_value")

    def test_multiple_listeners(self):
        """Test multiple listeners for same event"""
        results = []

        self.emitter.on("test", lambda x: results.append(x + 1))
        self.emitter.on("test", lambda x: results.append(x + 2))

        self.emitter.emit("test", 10)

        self.assertEqual(len(results), 2)
        self.assertIn(11, results)
        self.assertIn(12, results)

    def test_off(self):
        """Test removing event listeners"""
        def callback():
            self.callback_count += 1

        self.emitter.on("test", callback)
        self.emitter.emit("test")
        self.assertEqual(self.callback_count, 1)

        removed = self.emitter.off("test", callback)
        self.assertTrue(removed)

        self.emitter.emit("test")
        self.assertEqual(self.callback_count, 1)  # Should not increase

    def test_once(self):
        """Test one-time event listeners"""
        def callback():
            self.callback_count += 1

        self.emitter.once("test", callback)

        self.emitter.emit("test")
        self.assertEqual(self.callback_count, 1)

        self.emitter.emit("test")
        self.assertEqual(self.callback_count, 1)  # Should not increase

    def test_remove_all_listeners(self):
        """Test removing all listeners"""
        self.emitter.on("event1", lambda: None)
        self.emitter.on("event1", lambda: None)
        self.emitter.on("event2", lambda: None)

        self.emitter.remove_all_listeners("event1")
        self.assertEqual(self.emitter.listener_count("event1"), 0)
        self.assertEqual(self.emitter.listener_count("event2"), 1)

        self.emitter.remove_all_listeners()
        self.assertEqual(len(self.emitter.event_names()), 0)

    def test_listener_count(self):
        """Test counting listeners"""
        self.assertEqual(self.emitter.listener_count("test"), 0)

        self.emitter.on("test", lambda: None)
        self.assertEqual(self.emitter.listener_count("test"), 1)

        self.emitter.on("test", lambda: None)
        self.assertEqual(self.emitter.listener_count("test"), 2)

    def test_event_names(self):
        """Test getting event names"""
        self.emitter.on("event1", lambda: None)
        self.emitter.on("event2", lambda: None)

        names = self.emitter.event_names()
        self.assertIn("event1", names)
        self.assertIn("event2", names)

    def test_emit_with_kwargs(self):
        """Test emitting events with keyword arguments"""
        def callback(name, age):
            self.callback_args = (name, age)

        self.emitter.on("test", callback)
        self.emitter.emit("test", name="John", age=30)

        self.assertEqual(self.callback_args, ("John", 30))


if __name__ == '__main__':
    unittest.main()
