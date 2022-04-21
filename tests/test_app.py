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

"""Tests for Celery application factory."""

import pytest
from celery import Celery
from celery.utils.log import get_task_logger
from flask import Flask, current_app, request

from flask_celeryext import AppContextTask, RequestContextTask, create_celery_app
from flask_celeryext._mapping import FLASK_TO_CELERY_MAPPING
from flask_celeryext.app import map_invenio_to_celery


class celery_conf:
    """Configuration for testing Celery tasks for Celery >= 5.1.0."""

    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
    CELERY_ACCEPT_CONTENT = ["json", "msgpack", "yaml"]
    CELERY_RESULT_SERIALIZER = "msgpack"
    CELERY_TASK_SERIALIZER = "msgpack"


def test_mapping():
    """Test Invenio Celery configuration variables to Celery configuration
    variables.
    """
    config = {
        "CELERY_BROKER_URL": "redis://localhost:6379/0",
        "CELERY_RESULT_BACKEND": "redis://localhost:6379/1",
        "CELERY_ACCEPT_CONTENT": ["json", "msgpack", "yaml"],
        "CELERY_RESULT_SERIALIZER": "msgpack",
        "CELERY_TASK_SERIALIZER": "msgpack",
    }

    mapped = map_invenio_to_celery(config, FLASK_TO_CELERY_MAPPING)
    assert mapped["broker_url"] == "redis://localhost:6379/0"
    assert mapped["result_backend"] == "redis://localhost:6379/1"
    assert mapped["accept_content"] == ["json", "msgpack", "yaml"]
    assert mapped["result_serializer"] == "msgpack"
    assert mapped["task_serializer"] == "msgpack"


def test_factory():
    """Test of factory method."""
    # Set the current Celery application
    c = Celery("mycurrent")
    c.set_current()

    app = Flask("testapp")
    celery = create_celery_app(app)
    assert celery
    assert celery.flask_app == app


def test_appctx_task():
    """Test execution of Celery task with application context."""
    app = Flask("testapp")
    app.config.from_object(celery_conf)

    # Set the current Celery application
    c = Celery("mycurrent")
    c.set_current()

    celery = create_celery_app(app)

    @celery.task
    def appctx():
        return current_app.name

    r = appctx.delay()
    assert r.result == "testapp"


def test_reqctx_task():
    """Test execution of Celery task with request context."""
    app = Flask("testapp")
    app.config.from_object(celery_conf)
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
    app = Flask("testapp")
    app.config.from_object(celery_conf)
    celery = create_celery_app(app)
    celery.log.setup_task_loggers()

    @celery.task()
    def logtask():
        logger = get_task_logger(__name__)
        while getattr(logger, "parent", None):
            assert logger.propagate == 1
            logger = logger.parent

    logtask.delay()


def test_subtask_and_eager_dont_create_new_app_context(mocker):
    app = Flask("testapp")
    app.config.from_object(celery_conf)
    # Set the current Celery application
    c = Celery("mycurrent")
    c.set_current()

    celery = create_celery_app(app)

    spy = mocker.spy(app, "app_context")

    @celery.task
    def subtask():
        return current_app.name

    @celery.task
    def maintask():
        future = subtask.delay()
        return future.result

    r = maintask.delay()
    assert r.result == "testapp"
    assert spy.call_count == 1
