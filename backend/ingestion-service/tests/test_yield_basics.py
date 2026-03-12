import pytest


def number_steps():
    yield 1
    yield 2


def test_generator_yields_values_in_order():
    generator = number_steps()

    assert next(generator) == 1
    assert next(generator) == 2


def test_generator_stops_after_last_value():
    generator = number_steps()

    next(generator)
    next(generator)

    with pytest.raises(StopIteration):
        next(generator)
