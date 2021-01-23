# This runs the test notebooks in test folder and
# verifies they complete without exceptions.
# Also collects code coverage.
# Notebooks should still be verified manually to
# enusre things are drawn correctly.
py.test --nbval-lax --cov=schemdraw --cov-report=html test