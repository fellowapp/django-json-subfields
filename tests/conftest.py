import os
import pytest
import pymysql
from django.conf import settings


def pytest_configure():
    pymysql.install_as_MySQLdb()

    settings.configure(
        INSTALLED_APPS=["tests"],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": "django_json_subfields",
                "PORT": os.environ.get("MYSQL_PORT"),
                "USER": "root",
                "PASSWORD": os.environ.get("MYSQL_ROOT_PASSWORD"),
            }
        },
    )


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
