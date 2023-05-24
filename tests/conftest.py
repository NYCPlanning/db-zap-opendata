import pytest
from src import CLIENT_ID, SECRET, TENANT_ID, ZAP_DOMAIN
from src.client import Client

TEST_DATA_PATH = "tests/test_data"

@pytest.fixture()
def seed_data_path():
    return "mapzap/seeds"

@pytest.fixture(scope="session")
def test_client():
    return Client(
        zap_domain=ZAP_DOMAIN,
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        secret=SECRET,
    )
