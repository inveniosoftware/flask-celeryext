# -*- coding: utf-8 -*-
#
# This file is part of Flask-CeleryExt
# Copyright (C) 2015-2019 CERN.
# Copyright (C) 2018-2019 infarm - Indoor Urban Farming GmbH.
# Copyright (C) 2022 Graz University of Technology.
#
# Flask-CeleryExt is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for more
# details.

"""Flask extension for Celery integration."""

import flask
from celery import Task
from celery import current_app as current_celery_app
from celery import signals

from ._mapping import FLASK_TO_CELERY_MAPPING


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

    def __call__(self, *args, **kwargs):
        """Execute task."""
        # If an "app_context" has already been loaded, just pass through
        if flask._app_ctx_stack.top is not None:
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
            self.app.flask_app.try_trigger_before_first_request_functions()
            self.app.flask_app.preprocess_request()
            res = Task.__call__(self, *args, **kwargs)
            self.app.flask_app.process_response(self.app.flask_app.response_class())
            return res
