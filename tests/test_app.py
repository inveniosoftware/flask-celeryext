# -*- coding: utf-8 -*-
#
# This file is part of Flask-CeleryExt
# Copyright (C) 2015-2019 CERN.
# Copyright (C) 2018-2019 infarm - Indoor Urban Farming GmbH.
#
# Flask-CeleryExt is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for more
# details.

"""Tests for Celery application factory."""

from __future__ import absolute_import, print_function

import pytest
from celery import Celery
from celery.utils.log import get_task_logger
from flask import Flask, current_app, request

from flask_celeryext import AppContextTask, RequestContextTask, \
    create_celery_app
from flask_celeryext.app import CELERY_4_OR_GREATER


class eager_conf_v4:
    """Configuration for testing Celery tasks for Celery >= 4.0."""

    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_RESULT_BACKEND = "cache"
    CELERY_CACHE_BACKEND = "memory"


class eager_conf_v3:
    """Configuration for testing Celery tasks for Celery < 4.0."""

    CELERY_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    CELERY_RESULT_BACKEND = "cache"
    CELERY_CACHE_BACKEND = "memory"


eager_conf = eager_conf_v4 if CELERY_4_OR_GREATER else eager_conf_v3


@pytest.mark.skipif(CELERY_4_OR_GREATER, reason="requires Celery < 4.0")
def test_config3():
    """Test passing in config."""
    c = Celery('mycurrent')
    c.set_current()

    app = Flask("myapp")
    app.config.from_object(eager_conf)
    celery = create_celery_app(app)
    assert celery
    assert celery.flask_app == app
    assert celery.conf.CELERY_ALWAYS_EAGER
    assert celery.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS
    assert celery.conf.CELERY_RESULT_BACKEND == 'cache'
    assert celery.conf.CELERY_CACHE_BACKEND == 'memory'


@pytest.mark.skipif(not CELERY_4_OR_GREATER, reason="requires Celery >= 4.0")
def test_config4():
    """Test passing in config."""
    c = Celery('mycurrent')
    c.set_current()

    app = Flask("myapp")
    app.config.from_object(eager_conf)
    celery = create_celery_app(app)
    assert celery
    assert celery.flask_app == app
    assert celery.conf.task_always_eager
    assert celery.conf.task_eager_propagates
    assert celery.conf.result_backend == 'cache'
    assert celery.conf.cache_backend == 'memory'


@pytest.mark.skipif(not CELERY_4_OR_GREATER, reason="requires Celery >= 4.0")
def test_config3_on_4():
    """Test passing in config."""
    c = Celery('mycurrent')
    c.set_current()

    app = Flask("myapp")
    app.config.from_object(eager_conf_v3)
    celery = create_celery_app(app)
    assert celery
    assert celery.flask_app == app
    assert celery.conf.task_always_eager
    assert celery.conf.task_eager_propagates
    assert celery.conf.result_backend == 'cache'
    assert celery.conf.cache_backend == 'memory'


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


def test_task_logger_propagation():
    """Test log propagation of Celery task."""
    app = Flask("myapp")
    app.config.from_object(eager_conf)
    celery = create_celery_app(app)
    celery.log.setup_task_loggers()

    @celery.task()
    def logtask():
        logger = get_task_logger(__name__)
        while getattr(logger, 'parent', None):
            assert logger.propagate == 1
            logger = logger.parent

    logtask.delay()


def test_subtask_and_eager_dont_create_new_app_context(mocker):
    app = Flask("myapp")
    app.config.from_object(eager_conf)
    # Set the current Celery application
    c = Celery('mycurrent')
    c.set_current()

    celery = create_celery_app(app)

    spy = mocker.spy(app, 'app_context')

    @celery.task
    def subtask():
        return current_app.name

    @celery.task
    def maintask():
        future = subtask.delay()
        return future.result

    r = maintask.delay()
    assert r.result == "myapp"
    assert spy.call_count == 1
