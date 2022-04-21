# -*- coding: utf-8 -*-
#
# This file is part of Flask-CeleryExt
# Copyright (C) 2015 CERN.
#
# Flask-CeleryExt is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for more
# details.

"""Tests for extension."""

from __future__ import absolute_import, print_function

from celery import Celery
from flask import Flask

from flask_celeryext import FlaskCeleryExt


def test_ext_init():
    """Test of find_best_app."""
    app = Flask("testapp")
    ext = FlaskCeleryExt(app=app)
    assert ext.celery

    app = Flask("testapp")
    ext = FlaskCeleryExt()
    assert ext.celery is None
    ext.init_app(app)
    assert ext.celery

    def factory(flask_app):
        celery = Celery("myname")
        celery.flask_app = flask_app
        return celery

    app = Flask("testapp")
    ext = FlaskCeleryExt(app=app, create_celery_app=factory)
    ext.init_app(app)
    assert ext.celery
