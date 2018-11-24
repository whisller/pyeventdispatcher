from pyeventdispatcher import PyEventDispatcher, PyEvent


class TestExecutionOrder:
    def test_listeners_executed_in_order_they_were_added(self, capsys):
        def first_function(event):
            print("First")
            print(event.data)

        def second_function(event):
            print("Second")
            print(event.data)

        py_event_dispatcher = PyEventDispatcher()
        py_event_dispatcher.register("foo.bar", first_function)
        py_event_dispatcher.register("foo.bar", second_function)
        py_event_dispatcher.dispatch(PyEvent("foo.bar", {"a": "b"}))

        captured = capsys.readouterr()

        assert captured.out == "First\n{'a': 'b'}\nSecond\n{'a': 'b'}\n"
