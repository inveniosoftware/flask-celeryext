# SPDX-FileCopyrightText: 2015 CERN.
# SPDX-License-Identifier: BSD-3-Clause

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
