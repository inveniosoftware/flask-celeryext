# -*- coding: utf-8 -*-
#
# This file is part of Flask-CeleryExt
# Copyright (C) 2015-2019 CERN.
# Copyright (C) 2018-2019 infarm - Indoor Urban Farming GmbH.
#
# Flask-CeleryExt is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for more
# details.

"""Flask extension for Celery integration."""

from __future__ import absolute_import, print_function

import warnings
from distutils.version import LooseVersion

import flask
from celery import Task
from celery import __version__ as celery_version
from celery import current_app as current_celery_app
from celery import signals

from ._mapping import V3TOV4MAPPING

CELERY_4_OR_GREATER = LooseVersion(celery_version) >= LooseVersion('4.0')


def v3tov4config(config, mapping):
    """Translate Celery v3 configuration to v4."""
    for new, old in mapping.items():
        if new not in config and old in config:
            warnings.warn(
                'Celery v4 installed, but detected Celery v3 '
                'configuration %s (use %s instead).' % (old, new),
                UserWarning
            )
            config[new] = config[old]


def setup_task_logger(logger=None, **kwargs):
    """Make celery.task logger propagate exceptions.

    Ensures that handlers in the RootLogger such as Sentry will be run.
    """
    logger.propagate = 1


def create_celery_app(flask_app):
    """Create a Celery application."""
    celery = current_celery_app

    if CELERY_4_OR_GREATER:
        v3tov4config(flask_app.config, V3TOV4MAPPING)
        celery.config_from_object(flask_app.config, namespace='CELERY')  # pragma: no cover
    else:
        celery.config_from_object(flask_app.config)  # pragma: no cover

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
            self.app.flask_app.process_response(
                self.app.flask_app.response_class())
            return res
