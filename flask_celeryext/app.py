# -*- coding: utf-8 -*-
#
# This file is part of Flask-CeleryExt
# Copyright (C) 2015, 2016 CERN.
#
# Flask-CeleryExt is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for more
# details.

"""Flask extension for Celery integration."""

from __future__ import absolute_import, print_function

from celery import current_app as current_celery_app
from celery import Task, signals


def setup_task_logger(logger=None, **kwargs):
    """Make celery.task logger propagate exceptions.

    Ensures that handlers in the RootLogger such as Sentry will be run.
    """
    logger.propagate = 1


def create_celery_app(flask_app):
    """Create a Celery application."""
    celery = current_celery_app
    celery.conf.update(flask_app.config)
    celery.Task = AppContextTask

    # Set Flask application object on the Celery application.
    if not hasattr(celery, 'flask_app'):
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
            self.app.flask_app.process_response(
                self.app.flask_app.response_class())
            return res
