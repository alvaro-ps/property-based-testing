from hypothesis import given
from hypothesis.stateful import RuleBasedStateMachine, rule, precondition, invariant

from code.state import Heap
from tests.state.conftest import a_nonempty_heap, a_number


# Tests

@given(a_nonempty_heap)
def test_that_a_heap_peeks_its_min_value(heap):
    assert heap.min() == min(heap.elements)

@given(a_nonempty_heap)
def test_that_a_heap_that_inserts_a_min_value_can_then_find_it(heap):
    original_min = heap.min()
    match original_min:
        case int(original_min) | float(original_min):
            new_min = original_min - 1
        case _:
            new_min = ""

    new_heap = heap.insert(new_min)
    assert new_heap.min() == new_min

@given(a_nonempty_heap)
def test_that_a_heap_that_deletes_its_top_value_can_then_not_find_it(heap):
    original_min = heap.min()
    match original_min:
        case int(original_min) | float(original_min):
            new_min = original_min - 1
        case _:
            new_min = ""

    new_heap = heap.insert(new_min)
    final_heap = new_heap.delete_top()
    final_min = final_heap.min()

    assert final_min == original_min


# Stateful tests

class HeapStateMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()

        self.heap = Heap()

    @rule(element=a_number)
    def insert_element(self, element):
        return self.heap.insert(element)

    @rule()
    def find_min(self):
        return self.heap.min()

    @precondition(lambda self: self.find_min() is not None)
    @rule()
    def delete_top_element(self):
        return self.heap.delete_top()

    @precondition(lambda self: self.find_min() is not None)
    @invariant()
    def min_value_should_be_always_correct(self):
        assert self.heap.min() == min(self.heap.elements)


TestHeapStateMachine = HeapStateMachine.TestCase
