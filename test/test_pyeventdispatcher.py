import pytest
import pyeventdispatcher

from pyeventdispatcher import (
    EventDispatcher,
    Event,
    EventDispatcherException,
    EventSubscriber,
    listen,
)
from pyeventdispatcher.event_dispatcher import (
    MemoryRegistry,
    register_global_listener,
    register_event_subscribers,
)


class TestRegister:
    class MyListener:
        def call_on_event(self, event):
            print(event.data)

    @pytest.mark.parametrize(
        "registered", [MyListener().call_on_event, lambda event: print(event.data)]
    )
    def test_it_allows_to_register(self, registered, capsys):
        py_event_dispatcher = EventDispatcher()
        py_event_dispatcher.register("foo.bar", registered)
        py_event_dispatcher.dispatch(Event("foo.bar", {"a": "b"}))

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
        py_event_dispatcher = EventDispatcher()
        for register in to_register:
            py_event_dispatcher.register(
                "foo.bar", register["lambda"], register["priority"]
            )
        py_event_dispatcher.dispatch(Event("foo.bar", {"a": "b"}))

        captured = capsys.readouterr()

        assert captured.out == output

    def test_it_raises_an_exception_when_non_callable_is_trying_to_be_registered(self):
        py_event_dispatcher = EventDispatcher()
        with pytest.raises(EventDispatcherException):
            py_event_dispatcher.register("foo.bar", "")

    @pytest.mark.parametrize("priority", [None, ""])
    def test_it_raises_an_exception_when_priority_is_not_integer(self, priority):
        py_event_dispatcher = EventDispatcher()
        with pytest.raises(EventDispatcherException):
            py_event_dispatcher.register(
                "foo.bar", lambda event: print(event), priority
            )


class TestRegisterGlobal:
    def setup_method(self):
        pyeventdispatcher.event_dispatcher.global_registry = MemoryRegistry()

    def test_it_allows_to_register_listener_globally(self, capsys):
        def my_listener(event):
            print("my_listener")

        def global_listener(event):
            print("global")

        register_global_listener("foo.bar", global_listener)

        py_event_dispatcher_1 = EventDispatcher()
        py_event_dispatcher_1.register("foo.bar", my_listener)
        py_event_dispatcher_2 = EventDispatcher()
        py_event_dispatcher_2.register("foo.bar", my_listener)

        py_event_dispatcher_1.dispatch(Event("foo.bar", None))
        captured = capsys.readouterr()

        assert captured.out == "my_listener\nglobal\n"


class TestRegisterSubscribers:
    def setup_method(self):
        pyeventdispatcher.event_dispatcher.global_registry = MemoryRegistry()

    class MySubscriber1(EventSubscriber):
        EVENTS = {"foo.bar": "execute_one", "bar.foo": ("execute_two", -10)}

        @staticmethod
        def execute_one(event):
            print("MySubscriber1::execute_one")

        @staticmethod
        def execute_two(event):
            print("MySubscriber1::execute_two")

    def test_register_global_listeners_by_subscriber(self, capsys):
        register_event_subscribers()
        py_event_dispatcher = EventDispatcher()
        py_event_dispatcher.dispatch(Event("foo.bar", None))

        captured = capsys.readouterr()
        assert captured.out == "MySubscriber1::execute_one\n"


class TestRegisterThroughDecorator:
    def setup_method(self):
        pyeventdispatcher.event_dispatcher.global_registry = MemoryRegistry()

    def test_register_global_listener_by_decorator(self, capsys):
        @listen("foo.bar")
        def my_test_function(event):
            print(event.name)

        py_event_dispatcher = EventDispatcher()
        py_event_dispatcher.dispatch(Event("foo.bar", None))

        captured = capsys.readouterr()
        assert captured.out == "foo.bar\n"


class TestStopPropagation:
    def setup_method(self):
        pyeventdispatcher.event_dispatcher.global_registry = MemoryRegistry()

    def test_it_stops_propagation(self, capsys):
        def first_listener(event):
            event.stop = True
            print("first_listener")

        def second_listener(event):
            print("first_listener")

        py_event_dispatcher = EventDispatcher()
        py_event_dispatcher.register("foo.bar", first_listener)
        py_event_dispatcher.register("foo.bar", second_listener)
        py_event_dispatcher.dispatch(Event("foo.bar", {}))

        captured = capsys.readouterr()

        assert captured.out == "first_listener\n"
