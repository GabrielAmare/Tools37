import unittest

from tools37.events.direct import *


class TestEvents(unittest.TestCase):
    def test_001(self):
        emitter1 = Emitter()
        emitter2 = Emitter()
        observer1 = Observer()
        observer2 = Observer()
        name1 = 'abc'
        name2 = 'xyz'

        reference = EventModel(name=name1, emitter=emitter1, observer=observer1)

        self.assertIs(
            reference,
            EventModel(name=name1, emitter=emitter1, observer=observer1),
            msg="event models should be identical "
                "if name1 == name2 & emitter1 == emitter2 & observer1 == observer2."
        )
        self.assertIsNot(
            reference,
            EventModel(name=name2, emitter=emitter1, observer=observer1),
            msg="event models should not be identical "
                "if name1 != name2 & emitter1 == emitter2 & observer1 == observer2."
        )
        self.assertIsNot(
            reference,
            EventModel(name=name1, emitter=emitter2, observer=observer1),
            msg="event models should not be identical "
                "if name1 == name2 & emitter1 != emitter2 & observer1 == observer2."
        )
        self.assertIsNot(
            reference,
            EventModel(name=name1, emitter=emitter1, observer=observer2),
            msg="event models should not be identical "
                "if name1 == name2 & emitter1 == emitter2 & observer1 != observer2."
        )

    def test_002(self):
        emitter1 = Emitter()
        emitter2 = Emitter()
        observer = Observer()
        name1 = 'abc'
        name2 = 'xyz'

        reference = EventModel(name=name1, emitter=emitter1, observer=observer)

        self.assertTrue(
            reference.match(Event(emitter=emitter1, name=name1)),
            msg="event models should match events if emitter1 == emitter2 & name1 == name2"
        )
        self.assertFalse(
            reference.match(Event(emitter=emitter2, name=name1)),
            msg="event models should not match events if emitter1 != emitter2 & name1 == name2"
        )
        self.assertFalse(
            reference.match(Event(emitter=emitter1, name=name2)),
            msg="event models should not match events if emitter1 == emitter2 & name1 != name2"
        )

        reference = EventModel(name='*', emitter=emitter1, observer=observer)

        self.assertTrue(
            reference.match(Event(emitter=emitter1, name=name1)),
            msg="event models with name '*' should match any events if emitter1 == emitter2"
        )

    def test_003(self):
        emitter = Emitter()
        transmitter = Transmitter()
        observer = Observer()

        prefix = 'xyz'
        suffix = 'abc'

        transmitter.transmit(name='*', emitter=emitter, prefix=prefix)

        observer.test_passed = False

        def function(event: Event) -> None:
            if event.name == prefix + suffix and event.emitter is transmitter:
                observer.test_passed = True

        observer.on(emitter=transmitter, name='*', function=function)

        emitter.emit(suffix, *'xyz', some_kwarg='...')
        self.assertTrue(
            observer.test_passed,
            msg="Transmitters shall be able to re-emit events they receive with an additional prefix to the event name."
        )


if __name__ == '__main__':
    unittest.main()
