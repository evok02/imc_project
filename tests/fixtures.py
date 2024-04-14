
import pytest

from ..src.app import create_app
from ..src.model.agency import Agency
from ..src.model.agency import Newspaper
from .testdata import populate


@pytest.fixture(scope="function")
def app():
    yield create_app()


@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture(scope="function")
def agency(app):
    agency = Agency.get_instance()
    populate(agency)
    yield agency
    agency = Agency.get_instance()



