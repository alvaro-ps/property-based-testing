# Property-based testing with Hypothesis

This repo contains a number of examples that allow using property-based testing against
a "domain business logic".

The code is structured in the following way:

    - domain: core business logic implemented in memory
    - data generation strategies: based on the entities defined in domain
    - tests: use generated data to test the domain
    - stateful tests [optional]: generate not only data but sequences of calls on the same
        entities

# Running the code

Run `pip install -r requirements.txt` with any fairly recent python version. Then, in orden
to run the tests, type:
```
pytest *.py --hypothesis-show-statistics --verbose
```
Notice that `conftest.py` allows us to specify a profile for hypothesis to know how many
tests to run and how much info to display. In order to modify that, you can use an
environmental variable:
```
CI_ROLE=ci pytest *.py --hypothesis-show-statistics --verbose
```
