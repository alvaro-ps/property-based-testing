# Property-based testing with Hypothesis

This repo contains a number of examples that allow using property-based testing against
a "domain business logic".

The code is structured in the following way:

    - domain: core business logic implemented in memory
    - data generation strategies: based on the entities defined in domain
    - tests: use generated data to test the domain
    - stateful tests [optional]: generate not only data but sequences of calls on the same
        entities
