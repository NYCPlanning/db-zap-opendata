import pytest
from src.runner import Runner

test_dataset_name = "does_not_exist"


@pytest.mark.integration()
def test_runner():
    runner = Runner(name=test_dataset_name)
    runner()