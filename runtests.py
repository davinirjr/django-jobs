# coding: utf-8

# Inspired by model_mommy's (github.com/vandersonmota/model_mommy) test runner.


def configure_settings():
    from django.conf import settings

    params = dict(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        INSTALLED_APPS=(
            'jobs',
        ),
        TEST_RUNNER='django.test.simple.DjangoTestSuiteRunner',
    )

    settings.configure(**params)

    return settings


def get_runner(settings):
    '''
    Asks Django for the TestRunner defined in settings or the default one.
    '''
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    return TestRunner(verbosity=1, interactive=True, failfast=False)

if __name__ == '__main__':
    settings = configure_settings()
    test_runner = get_runner(settings)
    test_runner.run_tests(['jobs'])
