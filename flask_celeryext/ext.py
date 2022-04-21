# -*- coding: utf-8 -*-
#
# This file is part of Flask-CeleryExt
# Copyright (C) 2015 CERN.
# Copyright (C) 2022 Graz University of Technology.
#
# Flask-CeleryExt is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for more
# details.

"""Flask extension for Celery integration."""

from .app import create_celery_app as pkg_create_celery_app


class FlaskCeleryExt(object):
    """Flask-Celery extension."""

    def __init__(self, app=None, create_celery_app=None):
        """Initialize the Flask-CeleryExt."""
        self.create_celery_app = create_celery_app or pkg_create_celery_app
        self.celery = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize a Flask application."""
        # Follow the Flask guidelines on usage of app.extensions
        if not hasattr(app, "extensions"):
            app.extensions = {}  # pragma: no cover
        app.extensions["flask-celeryext"] = self
        self.celery = self.create_celery_app(app)
