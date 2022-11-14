from __future__ import annotations
from operator import attrgetter

from hypothesis import given, note
import hypothesis.strategies as st

from code.people import People
from tests.people.conftest import an_adult, a_kid, some_people, create_family


@given(an_adult)
def test_that_a_person_will_not_live_more_than_200_years_yet(person):
    assert person.age <= 200


@given(an_adult)
def test_that_a_persons_full_name_contains_first_and_last_name(person):
    assert person.full_name.startswith(person.first_name)
    assert person.full_name.endswith(person.last_name)


@given(an_adult.filter(lambda p: p.age > 18))
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


@given(st.data())
def test_that_a_family_has_two_adults_and_may_have_no_kids(data):
    family = create_family(data)
    note(f"Family {family.map(lambda p: (p.full_name, p.age))}")

    assert len(family.grown_ups()) == 2
    assert len(family.kids()) >= 0
