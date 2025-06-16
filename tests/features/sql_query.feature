Feature: SQL Query
    To run a SQL Query and recive and expected result.


    Scenario: Sql Query Provides correct details
        Given I require the record provided in $<folder>\<result_file>
        When I run the query provided in $<folder>\<query_file>
        Then the record provided in the csv matches the record provided by the sql query 
        Examples:
          | Test_line | folder     | result_file                   | query_file                   |
          | 1         | use_case_1 | customer_name_&_address.csv   | customer_name_&_address.sql  |
          | 2         | use_case_2 | customer_name.csv             | customer_name.sql            |
          | 3         | use_case_3 | deliberate_fail.csv           | deliberate_fail.sql          |