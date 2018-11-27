from collections import defaultdict

import pytest

from pyeventdispatcher import (
    PyEventDispatcher,
    PyEvent,
    PyEventDispatcherException,
    PyEventSubscriber,
)


class TestRegister:
    class MyListener:
        def call_on_event(self, event):
            print(event.data)

    @pytest.mark.parametrize(
        "registered", [MyListener().call_on_event, lambda event: print(event.data)]
    )
    def test_it_allows_to_register(self, registered, capsys):
        py_event_dispatcher = PyEventDispatcher()
        py_event_dispatcher.register("foo.bar", registered)
        py_event_dispatcher.dispatch(PyEvent("foo.bar", {"a": "b"}))

        captured = capsys.readouterr()

        assert captured.out == "{'a': 'b'}\n"

    @pytest.mark.parametrize(
        "to_register, output",
        [
            # With default "priority" - in order they were added
            (
                (
                    {"lambda": lambda event: print("First"), "priority": 0},
                    {"lambda": lambda event: print("Second"), "priority": 0},
                ),
                "First\nSecond\n",
            ),
            # Based on priority
            (
                (
                    {"lambda": lambda event: print("First"), "priority": 0},
                    {"lambda": lambda event: print("Second"), "priority": -100},
                ),
                "Second\nFirst\n",
            ),
        ],
    )
    def test_listeners_executed_in_order(self, to_register, output, capsys):
        py_event_dispatcher = PyEventDispatcher()
        for register in to_register:
            py_event_dispatcher.register(
                "foo.bar", register["lambda"], register["priority"]
            )
        py_event_dispatcher.dispatch(PyEvent("foo.bar", {"a": "b"}))

        captured = capsys.readouterr()

        assert captured.out == output

    def test_it_raises_an_exception_when_non_callable_is_trying_to_be_registered(self):
        py_event_dispatcher = PyEventDispatcher()
        with pytest.raises(PyEventDispatcherException):
            py_event_dispatcher.register("foo.bar", "")

    @pytest.mark.parametrize("priority", [None, ""])
    def test_it_raises_an_exception_when_priority_is_not_integer(self, priority):
        py_event_dispatcher = PyEventDispatcher()
        with pytest.raises(PyEventDispatcherException):
            py_event_dispatcher.register(
                "foo.bar", lambda event: print(event), priority
            )


class TestRegisterGlobal:
    def setup_method(self):
        PyEventDispatcher._GLOBAL_LISTENERS = defaultdict(list)

    def test_it_allows_to_register_listener_globally(self, capsys):
        def my_listener(event):
            print("my_listener")

        def global_listener(event):
            print("global")

        PyEventDispatcher.register_global("foo.bar", global_listener)

        py_event_dispatcher_1 = PyEventDispatcher()
        py_event_dispatcher_1.register("foo.bar", my_listener)
        py_event_dispatcher_2 = PyEventDispatcher()
        py_event_dispatcher_2.register("foo.bar", my_listener)

        py_event_dispatcher_1.dispatch(PyEvent("foo.bar", None))
        captured = capsys.readouterr()

        assert captured.out == "my_listener\nglobal\n"


class TestRegisterSubscribers:
    def setup_method(self):
        PyEventDispatcher._GLOBAL_LISTENERS = defaultdict(list)

    class MySubscriber1(PyEventSubscriber):
        EVENTS = {"foo.bar": "execute_one", "bar.foo": ("execute_two", -10)}

        @staticmethod
        def execute_one(event):
            print("MySubscriber1::execute_one")

        @staticmethod
        def execute_two(event):
            print("MySubscriber1::execute_two")

    def test_register_global_listeners_by_subscriber(self, capsys):
        py_event_dispatcher = PyEventDispatcher()
        py_event_dispatcher.register_subscribers()
        py_event_dispatcher.dispatch(PyEvent("foo.bar", None))

        captured = capsys.readouterr()
        assert captured.out == "MySubscriber1::execute_one\n"


class TestStopPropagation:
    def setup_method(self):
        PyEventDispatcher._GLOBAL_LISTENERS = defaultdict(list)

    def test_it_stops_propagation(self, capsys):
        def first_listener(event):
            event.stop = True
            print("first_listener")

        def second_listener(event):
            print("first_listener")

        py_event_dispatcher = PyEventDispatcher()
        py_event_dispatcher.register("foo.bar", first_listener)
        py_event_dispatcher.register("foo.bar", second_listener)
        py_event_dispatcher.dispatch(PyEvent("foo.bar", {}))

        captured = capsys.readouterr()

        assert captured.out == "first_listener\n"
