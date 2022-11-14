from typing import Optional

from faker import Faker
import hypothesis.strategies as st

from code.people import Person, People


fake = Faker()


an_adult = st.builds(
    Person,
    first_name=st.builds(fake.first_name),
    last_name=st.builds(fake.last_name),
    age=st.integers(min_value=18, max_value=120),
)


a_kid = st.builds(
    Person,
    first_name=st.builds(fake.first_name),
    last_name=st.builds(fake.last_name),
    age=st.integers(min_value=0, max_value=10),
)


def create_family(data, last_name: Optional[str] = None, n_kids: Optional[int] = None) -> People:
    family_name = last_name or fake.last_name()
    parents = [data.draw(an_adult) for _ in range(2)]
    total_kids: int = n_kids or data.draw(st.integers(min_value=0, max_value=5))
    kids = [data.draw(a_kid) for _ in range(total_kids)]

    return People(*parents, *kids).map(lambda person: person.with_last_name(family_name))


some_people = st.builds(People.from_list, st.lists(an_adult, min_size=0))
