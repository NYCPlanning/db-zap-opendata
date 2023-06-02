import os
import pytest
from collections import namedtuple

from src.runner import Runner

TEST_SCHEMA_SUFFIX = os.environ.get("TEST_SCHEMA_SUFFIX", None)

test_data_expected_schema = "test_data_expected"
test_data_actual_schema = "test_data_actual"
if TEST_SCHEMA_SUFFIX:
    test_data_actual_schema = f"{test_data_actual_schema}_{TEST_SCHEMA_SUFFIX}"

test_data_query = """
    select * from :dataset_name :filter_clause
"""
TestDataset = namedtuple(
    "TestDataset",
    [
        "name",
        "filter_clause",
        "expected_row_count",
    ],
)
# TODO add all output table names to these test datasets
test_datasets = [
    TestDataset(
        name="dcp_projects",
        filter_clause="""
            where dcp_name in (
                'P2016K0159', '2023K0228', 'P2005K0122', '2021M0260'
                )
            """,
        expected_row_count=4,
    ),
    # TestDataset(
    #     name="dcp_projectbbls",
    #     filter_clause="""
    #         where SUBSTRING(dcp_projectbbls.dcp_name, 0,10) in (
    #             'P2016K0159', '2023K0228', 'P2005K0122', '2021M0260'
    #             )
    #         """,
    #     expected_row_count=2210,
    # ),
]


@pytest.mark.integration()
@pytest.mark.parametrize("test_dataset", test_datasets)
def test_validate_expected_test_data(test_dataset):
    runner = Runner(name=test_dataset.name, schema=test_data_expected_schema)
    test_data_query_parameters = {
        "dataset_name": test_dataset.name,
        "filter_clause": test_dataset.filter_clause,
    }
    test_data_expected = runner.pg.execute_select_query(
        base_query=test_data_query,
        parameters=test_data_query_parameters,
    )
    assert len(test_data_expected) == test_dataset.expected_row_count


# @pytest.mark.skip(reason="in-progress")
@pytest.mark.integration()
@pytest.mark.parametrize("test_dataset", test_datasets)
def test_runner_clean(test_dataset):
    runner = Runner(name=test_dataset.name, schema=test_data_actual_schema)
    runner.clean()
    # TODO assert things
    # if os.path.isdir(self.output_dir):
    #   assert directory is empty
    # if os.path.isdir(self.cahce_dir):
    #   assert directory is empty


# @pytest.mark.skip(reason="in-progress")
@pytest.mark.integration()
@pytest.mark.parametrize("test_dataset", test_datasets)
def test_runner(test_dataset):
    # TODO run the entire runner
    runner = Runner(name=test_dataset.name, schema=test_data_actual_schema)
    runner()
    test_data_actual = runner.pg.execute_select_query(
        base_query=test_data_query,
        parameters={
            "dataset_name": test_dataset.name,
            "filter_clause": test_dataset.filter_clause,
        },
    )
    # TODO assert things for all output tables
    assert len(test_data_actual) == test_dataset.expected_row_count

    # TODO compare a subset of the final csv to known data
    runner = Runner(name=test_dataset.name, schema=test_data_expected_schema)
    test_data_expected = runner.pg.execute_select_query(
        base_query=test_data_query,
        parameters={
            "dataset_name": test_dataset.name,
            "filter_clause": test_dataset.filter_clause,
        },
    )
    # TODO assert things
