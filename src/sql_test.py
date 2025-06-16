import os
import pyodbc, struct
import pandas as pd
from azure import identity # type: ignore


CUSOTMER_ID = "DF121623-13D5-4A22-B532-584F0562E4D8"
SQL_QUERY = f"""
                SELECT
                    *
                FROM
                    dbo.Customer
                WHERE 
                    CustomerID = '{CUSOTMER_ID}'
                """

def connect_to_db():
    if os.getenv('GITHUB_ACTION') is None:
        connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]

        credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
        token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
        token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
        SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
        cnxn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    
        return cnxn
    else:
        SERVER = 'devsqldacinfsq1401.database.windows.net'
        DATABASE = 'devsqldacinfdbs1401'
        USERNAME = 'USERNAME'
        PASSWORD = 'PWD'

        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
    
        # conn = pyodbc.connect(connectionString)

        print(connectionString)
    


def query_customer_details(cnxn, query):
    sql_query = query
    df = pd.read_sql_query(sql_query, cnxn)
    return(df)


def close_connection(cnxn):
    cnxn.close()


def main(sql_query):
    cnxn = connect_to_db()
    query = query_customer_details(cnxn, sql_query)
    close_connection(cnxn)
    return(query)

if __name__ == "__main__":
    main(SQL_QUERY)
