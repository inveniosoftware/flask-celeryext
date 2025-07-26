# -*- coding: utf-8 -*-
#
# This file is part of Flask-CeleryExt
# Copyright (C) 2015-2019 CERN.
# Copyright (C) 2018-2019 infarm - Indoor Urban Farming GmbH.
# Copyright (C) 2022-2025 Graz University of Technology.
#
# Flask-CeleryExt is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for more
# details.

"""Flask extension for Celery integration."""

import importlib.metadata as m
from sys import version_info

from celery import Task
from celery import current_app as current_celery_app
from celery import signals
from flask import has_app_context

from ._mapping import FLASK_TO_CELERY_MAPPING


def entry_points(group):
    """Entry points."""
    if version_info < (3, 10):
        eps = m.entry_points()
        # the only reason to add this check is to simplify the tests! the tests
        # are implemented against python >=3.10 which uses the group keyword.
        # since we drop python3.9 soon, this should work!
        # in the tests there is a line which patches the return value of
        # importlib.metadata.entry_points with a list. this works for
        # python>=3.10 but not for 3.9
        # the return value of .get can contain duplicates. the simplest way to
        # remove is the set() call, to still return a list, list() is called on
        # set()
        if isinstance(eps, dict):
            eps = list(set(eps.get(group, [])))
    else:
        eps = m.entry_points(group=group)

    return eps


def map_invenio_to_celery(config, mapping):
    """Translate Invenio Celery configuration to Celery Configuration."""

    def map_key(key):
        return mapping[key] if key in mapping else key

    return {map_key(key): value for key, value in config.items()}


def setup_task_logger(logger=None, **kwargs):
    """Make celery.task logger propagate exceptions.

    Ensures that handlers in the RootLogger such as Sentry will be run.
    """
    logger.propagate = 1


def create_celery_app(flask_app):
    """Create a Celery application."""
    celery = current_celery_app

    config = map_invenio_to_celery(flask_app.config, FLASK_TO_CELERY_MAPPING)
    celery.config_from_object(config)

    celery.Task = AppContextTask

    # Set Flask application object on the Celery application.
    if not hasattr(celery, "flask_app"):
        celery.flask_app = flask_app

    signals.after_setup_task_logger.connect(setup_task_logger)
    return celery


class AppContextTask(Task):
    """Celery task running within a Flask application context.

    Expects the associated Flask application to be set on the bound
    Celery application.
    """

    abstract = True

    def __init__(self, *args, **kwargs):
        """Construct."""
        super().__init__(*args, **kwargs)
        self.entry_points = entry_points("flask_celeryext.app_context_task")

    def __call__(self, *args, **kwargs):
        """Execute task."""
        # If an "app_context" has already been loaded, just pass through
        for ep in self.entry_points:
            ep.load()()

        if has_app_context():
            return Task.__call__(self, *args, **kwargs)
        with self.app.flask_app.app_context():
            return Task.__call__(self, *args, **kwargs)


class RequestContextTask(Task):
    """Celery task running within Flask test request context.

    Expects the associated Flask application to be set on the bound
    Celery application.
    """

    abstract = True

    def __call__(self, *args, **kwargs):
        """Execute task."""
        with self.app.flask_app.test_request_context():
            self.app.flask_app.preprocess_request()
            res = Task.__call__(self, *args, **kwargs)
            self.app.flask_app.process_response(self.app.flask_app.response_class())
            return res
