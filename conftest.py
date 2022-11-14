import os

from hypothesis import settings, Verbosity

CI_ROLE = os.environ.get("CI_ROLE", "local")

settings.register_profile("local", max_examples=50, verbosity=Verbosity.verbose)
settings.register_profile("ci", max_examples=500)
settings.load_profile(CI_ROLE)
