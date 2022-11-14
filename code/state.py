from __future__ import annotations
from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar
import heapq


T = TypeVar("T")


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
