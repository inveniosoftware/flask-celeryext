Changes
=======

Version v0.4.3 (release 2022-06-15)

- housekeeping: misaligned tag vs version fix

Version v0.4.2 (release 2022-06-15)

- add two missing mappings
- global: fix revision id due to rebase
- add .git-blame-ignore-revs
- migrate to use black as opinionated auto formater
- bugfix BROKER_URL not in the mapping


Version 0.4.1 (released 2022-03-17)

- Fixes celery mapping fo the configuration.

Version 0.4.0 (released 2022-03-15)

- Adds support for Python 3.9.
- Adds support for new Celery configuration variable naming.
- Drops support for Python 2.7 and 3.6 due to end of life.
- Drops support for Celery 3 and 4.

Version 0.3.4 (released 2020-02-17)

- Adds support for Python 3.8
- Fixes pin for Celery on Python <3.7.

Version 0.3.3 (released 2020-02-13)

- Fix celery version for Python < 3.7

Version 0.3.2 (released 2019-06-25)

- Uses correct Celery version for Python 3.7.
- Prevents multiple creation and pushing of Flask application contexts.

Version 0.3.1 (released 2018-03-26)

- Accounts for non-strict Celery versions.

Version 0.3.0 (released 2017-03-24)

- Adds support for Celery v4.

Version 0.2.2 (released 2016-11-07)

- Forces celery version to v3.1-4.0 due to problem with 4.x.

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
