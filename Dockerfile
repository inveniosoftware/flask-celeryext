# This file is part of Flask-CeleryExt
# Copyright (C) 2015, 2016 CERN.
#
# Flask-CeleryExt is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for more
# details.

# Use Python-2.7:
FROM python:2.7

# Install some prerequisites ahead of `setup.py` in order to profit
# from the docker build cache:
RUN pip install coveralls \
                ipython \
                pydocstyle \
                pytest \
                pytest-cache \
                pytest-cov \
                Sphinx

# Add sources to `code` and work there:
WORKDIR /code
ADD . /code

# Install flask-cli:
RUN pip install -e .

# Run container as user `flask-celeryext` with UID `1000`, which should match
# current host user in most situations:
RUN adduser --uid 1000 --disabled-password --gecos '' flaskceleryext && \
    chown -R flaskceleryext:flaskceleryext /code

# Run test suite instead of starting the application:
USER flaskceleryext
CMD ["python", "setup.py", "test"]
