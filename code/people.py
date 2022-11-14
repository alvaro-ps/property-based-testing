from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Sequence, Iterator


@dataclass
class Person:
    first_name: str
    last_name: str
    age: int

    def __repr__(self):
        return f"{self.__class__.__name__}({self.first_name.title()}, {self.age})"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def is_of_age(self) -> bool:
        return self.age >= 18

    def with_age(self, new_age: int) -> Person:
        return replace(self, age=new_age)

    def with_last_name(self, new_last_name: str) -> Person:
        return replace(self, last_name=new_last_name)


class People(Sequence[Person]):
    def __init__(self, *people):
        self.people = people

    def __iter__(self) -> Iterator[Person]:
        return iter(self.people)

    def __getitem__(self, index) -> Person:
        return self.people[index]

    def __len__(self) -> int:
        return len(self.people)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.people == other.people

    def __repr__(self):
        info = ", ".join([repr(p) for p in self])
        return f"{self.__class__.__name__}({info})"

    def map(self, f):
        return People(*[f(person) for person in self])

    def filter(self, f):
        return People(*[person for person in self if f(person)])

    def new_year(self) -> People:
        return self.map(lambda person: person.with_age(person.age + 1))

    def kids(self) -> People:
        return self.filter(lambda person: person.age <= 10)

    def grown_ups(self) -> People:
        return self.filter(lambda person: person.age >= 18)

    @classmethod
    def from_list(cls, people):
        return cls(*people)
