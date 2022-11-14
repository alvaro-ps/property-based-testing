from __future__ import annotations
from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar
import heapq

from faker import Faker
from hypothesis import given
import hypothesis.strategies as st
from hypothesis.stateful import Bundle, RuleBasedStateMachine, rule, precondition, invariant

T = TypeVar("T")

fake = Faker()

"""
Domain
"""

@dataclass
class Heap(Generic[T]):
    elements: list[T] = field(default_factory=list)

    def __post_init__(self):
        heapq.heapify(self.elements)

    def insert(self, element: T) -> Heap:
        heapq.heappush(self.elements, element)
        return self

    def delete_top(self) -> Heap:
        heapq.heappop(self.elements)
        return self

    def min(self) -> Optional[T]:
        """Smallest"""
        try:
            return self.elements[0]
        except IndexError:
            return None

"""
Data generation strategies
"""
a_number = st.integers() | st.floats(allow_nan=False)
a_heap = st.builds(Heap, elements=st.lists(a_number))
a_nonempty_heap = st.builds(Heap, elements=st.lists(a_number, min_size=1))

"""
Tests
"""

@given(a_nonempty_heap)
def test_that_a_heap_peeks_its_min_value(heap):
    assert heap.min() == min(heap.elements)

@given(a_nonempty_heap)
def test_that_a_heap_that_inserts_a_min_value_can_then_find_it(heap):
    original_min = heap.min()
    new_min = original_min - 1
    new_heap = heap.insert(new_min)
    assert new_heap.min() == new_min

@given(a_nonempty_heap)
def test_that_a_heap_that_deletes_its_top_value_can_then_not_find_it(heap):
    original_min = heap.min()
    new_min = original_min - 1

    new_heap = heap.insert(new_min)
    final_heap = new_heap.delete_top()
    final_min = final_heap.min()

    assert final_min == original_min

"""
Stateful tests
"""

class HeapStateMachine(RuleBasedStateMachine):
    #elements = Bundle("elements")

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
