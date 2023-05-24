import pytest
from src import CLIENT_ID, SECRET, TENANT_ID, ZAP_DOMAIN
from src.client import Client


def test_data_path():
    return "tests/test_data"


@pytest.fixture(scope="session")
def test_client():
    return Client(
        zap_domain=ZAP_DOMAIN,
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        secret=SECRET,
    )
