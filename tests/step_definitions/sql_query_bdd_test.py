import pytest
import pandas as pd

from pytest_bdd import scenarios, given, when, then, parsers
import src.sql_test


scenarios("../features/sql_query.feature")

@pytest.fixture
def file_path():
    return {}

@pytest.fixture
def sql_query():
    return {}


@given(parsers.parse('I require the record provided in ${csv_file_name}'))
def path_to_csv(csv_file_name, file_path):
    csv_file_path = r"..\apha-data-team-testing\use_cases" + "\\" + f"{csv_file_name}"
    file_path["path"] = csv_file_path
    

@when(parsers.parse('I run the query provided in ${sql_file_name}'))
def pass_id(sql_file_name, sql_query):
    sql_file_path = r"..\apha-data-team-testing\use_cases" + "\\" + f"{sql_file_name}"
    fd = open(sql_file_path, 'r') 
    sql_file = fd.read()
    fd.close
    required_query = sql_file
    sql_query["sql_query"] = required_query


@then('the record provided in the csv matches the record provided by the sql query')
def compare_details(file_path, sql_query):
    required_details = pd.read_csv(file_path.get("path"), dtype=object)
    database_details = src.sql_test.main(sql_query.get("sql_query"))
    pd.testing.assert_frame_equal(required_details, database_details, check_dtype=False, check_index_type=False)
