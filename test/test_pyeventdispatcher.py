import pytest

from pyeventdispatcher import PyEventDispatcher, PyEvent, PyEventDispatcherException


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

    @pytest.mark.parametrize(
        "priority",
        [
            None,
            ""
        ],
    )
    def test_it_raises_an_exception_when_priority_is_not_integer(self, priority):
        py_event_dispatcher = PyEventDispatcher()
        with pytest.raises(PyEventDispatcherException):
            py_event_dispatcher.register("foo.bar", lambda event: print(event), priority)
