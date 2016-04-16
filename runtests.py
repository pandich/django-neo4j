# coding=utf-8
import sys

try:
    # noinspection PyUnresolvedReferences
    from django.conf import settings
    # noinspection PyUnresolvedReferences
    from django.test.utils import get_runner

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            u'default': {
                u'ENGINE': u'django.db.backends.sqlite3',
            }
        },
        ROOT_URLCONF=u'django_neo4j.urls',
        INSTALLED_APPS=[
            u'django.contrib.auth',
            u'django.contrib.contenttypes',
            u'django.contrib.sites',
            u'django_neo4j',
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(),
    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError(u'To fix this error, run: pip install -r requirements-test.txt')


def run_tests(*test_args):
    if not test_args:
        test_args = [u'tests']

    # Run tests
    # noinspection PyPep8Naming
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == u'__main__':
    run_tests(*sys.argv[1:])
