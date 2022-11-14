from __future__ import annotations
from operator import attrgetter
from dataclasses import dataclass, replace
from typing import Sequence, Iterator

from faker import Faker
from hypothesis import given
import hypothesis.strategies as st


fake = Faker()


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

    def grown_ups(self) -> People:
        return self.filter(lambda person: person.age > 18)

    @classmethod
    def from_list(cls, people):
        return cls(*people)


a_person = st.builds(
    Person,
    first_name=st.builds(fake.first_name),
    last_name=st.builds(fake.last_name),
    age=st.integers(min_value=0, max_value=120),
)

a_kid = a_person.filter(lambda person: person.age <= 10)

@st.composite
def create_family(draw, family_name: str) -> People:
    parent1 = draw(a_person, last_name=family_name)
    parent2 = draw(a_person, last_name=family_name)
    n_kids = draw(st.integers(min_value=0, max_value=5))
    kids = [draw(a_kid, last_name=family_name) for _ in n_kids] 

    return People(parent1, parent2, *kids)
    

some_people = st.builds(People.from_list, st.lists(a_person, min_size=0))
a_family = st.builds(create_family, family_name=st.builds(fake.last_name))


@given(a_person)
def test_that_a_person_will_not_live_more_than_200_years_yet(person):
    assert person.age <= 200


@given(a_person)
def test_that_a_persons_full_name_contains_first_and_last_name(person):
    assert person.full_name.startswith(person.first_name)
    assert person.full_name.endswith(person.last_name)


@given(a_person.filter(lambda p: p.age > 18))
def test_that_a_grownup_is_of_age(person):
    assert person.is_of_age


@given(some_people)
def test_that_a_new_year_adds_n_total_years_across_people(people):
    total_years_before = sum(people.map(attrgetter("age")))
    older_people = people.new_year()
    total_years_after = sum(older_people.map(attrgetter("age")))

    assert (total_years_after - total_years_before) == len(people)

@given(st.builds(People.from_list, st.lists(a_kid)))
def test_that_no_kid_is_a_grownup(kids):
    assert kids.grown_ups() == People()
