========================
 Flask-CeleryExt v0.2.0
========================

Flask-CeleryExt v0.2.0 was released on February 2, 2016.

About
-----

Flask-CeleryExt is a simple integration layer between Celery and Flask.

Incompatible changes
--------------------

- Changes celery application creation to use the default current
  celery application instead creating a new celery application. This
  addresses an issue with tasks using the shared_task decorator and
  having Flask-CeleryExt initialized multiple times.

Installation
------------

   $ pip install flask-cli==0.2.0

Documentation
-------------

   http://flask-cli.readthedocs.org/en/v0.2.0

Homepage
--------

   https://github.com/inveniosoftware/flask-celeryext

Happy hacking and thanks for flying Flask-CeleryExt.

| Invenio Development Team
|   Email: info@invenio-software.org
|   Twitter: http://twitter.com/inveniosoftware
|   GitHub: http://github.com/inveniosoftware
|   URL: http://invenio-software.org
