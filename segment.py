import pyodbc
from db import SERVER, DATABASE, USERNAME, PASSWORD


def dict_segmentation():
    connectionString = (f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER}'
                        f';DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}')
    conn = pyodbc.connect(connectionString)
    SQL_QUERY = """
    select * from TBL_segmentation
    """

    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)

    records = cursor.fetchall()
    dict = {0: 'Всі'}
    for r in records:
        dict[r.id] = r.name
    return dict
