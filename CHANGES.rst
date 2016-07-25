Changes
=======

Version 0.2.1 (released 2016-07-25)

Improved features

- Improves documentation structure and its automatic generation.

Version 0.2.0 (released 2016-02-02)

Incompatible changes

- Changes celery application creation to use the default current
  celery application instead creating a new celery application. This
  addresses an issue with tasks using the shared_task decorator and
  having Flask-CeleryExt initialized multiple times.

Version 0.1.0 (released 2015-08-17)

- Initial public release
