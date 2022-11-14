import hypothesis.strategies as st

from code.state import Heap


a_number = st.integers() | st.floats(allow_nan=False)
a_heap = st.builds(
    Heap,
    elements=st.one_of(
        st.lists(a_number),
        st.lists(st.text()),
    )
)
a_nonempty_heap = st.builds(
    Heap,
    elements=st.one_of(
        st.lists(a_number, min_size=1),
        st.lists(st.text(), min_size=1),
    )
)
