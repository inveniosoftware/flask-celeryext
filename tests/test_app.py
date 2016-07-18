# -*- coding: utf-8 -*-
#
# This file is part of Flask-CeleryExt
# Copyright (C) 2015, 2016 CERN.
#
# Flask-CeleryExt is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for more
# details.

"""Tests for Celery application factory."""

from __future__ import absolute_import, print_function

import pytest
from celery import Celery
from flask import Flask, current_app, request

from flask_celeryext import AppContextTask, RequestContextTask, \
    create_celery_app


class eager_conf:
    """Configuration for testing Celery tasks."""

    CELERY_ALWAYS_EAGER = True
    CELERY_RESULT_BACKEND = "cache"
    CELERY_CACHE_BACKEND = "memory"
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True


def test_factory():
    """Test of factory method."""
    # Set the current Celery application
    c = Celery('mycurrent')
    c.set_current()

    app = Flask("myapp")
    celery = create_celery_app(app)
    assert celery
    assert celery.flask_app == app


def test_appctx_task():
    """Test execution of Celery task with application context."""
    app = Flask("myapp")
    app.config.from_object(eager_conf)

    # Set the current Celery application
    c = Celery('mycurrent')
    c.set_current()

    celery = create_celery_app(app)

    @celery.task
    def appctx():
        return current_app.name

    r = appctx.delay()
    assert r.result == "myapp"


def test_reqctx_task():
    """Test execution of Celery task with request context."""
    app = Flask("myapp")
    app.config.from_object(eager_conf)
    celery = create_celery_app(app)

    @celery.task(base=RequestContextTask)
    def reqctx():
        return request.method

    @celery.task(base=AppContextTask)
    def reqctx2():
        return request.method

    r = reqctx.delay()
    assert r.result == "GET"

    assert pytest.raises(RuntimeError, reqctx2.delay)
