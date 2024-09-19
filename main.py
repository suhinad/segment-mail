import pyodbc
import csv
from db import SERVER, DATABASE, USERNAME, PASSWORD
from nowdatetime import nowdt


def segmentemail(segment, selected_value):
    now = nowdt()
    segment = int(segment)
    file_path = './download/output-' + now + '-' + selected_value + '.csv'
    if segment == 0:
        connectionString = (f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};'
                            f'DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}')

        conn = pyodbc.connect(connectionString)

        SQL_QUERY = """
        SELECT 
            КодПоставщика,   
            Название, 
            REPLACE(REPLACE(ОбращатьсяК, CHAR(13), ' '), CHAR(10), ' ') as ОбращатьсяК, 
            НомерТелефона, 
            REPLACE(REPLACE(email, CHAR(13), ' '), CHAR(10), ' ') as email, 
            REPLACE(REPLACE(S.name, CHAR(13), ' '), CHAR(10), ' ') AS Сегмент
        FROM 
            Клиенты K
        LEFT JOIN 
            TBL_segmentation S ON S.id = K.segmentation
        WHERE 
            K.department <> 34 
            AND K.КодПоставщика = K.masterID;
        """
        # and КодПоставщика = 3303
        # and segmentation  = "указать код сегмента"

        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)

        records = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]

        # Запис результатів у CSV файл
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')

            # Запис імен колонок
            writer.writerow(column_names)

            # Запис рядків
            for row in records:
                writer.writerow(row)

        # Закриття з'єднання
        cursor.close()
        conn.close()

        print(f"Дані успішно експортовані в {file_path}")
        return file_path

        # print(records)
        # for r in records:
        #    print(f"{r.КодПоставщика};{r.Название};{r.ОбращатьсяК};{r.НомерТелефона};{r.email};{r.Сегмент}")
    else:
        connectionString = (f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};'
                            f'DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}')

        conn = pyodbc.connect(connectionString)

        SQL_QUERY = """
                SELECT 
                    КодПоставщика,   
                    Название, 
                    REPLACE(REPLACE(ОбращатьсяК, CHAR(13), ' '), CHAR(10), ' ') as ОбращатьсяК, 
                    НомерТелефона, 
                    REPLACE(REPLACE(email, CHAR(13), ' '), CHAR(10), ' ') as email, 
                    REPLACE(REPLACE(S.name, CHAR(13), ' '), CHAR(10), ' ') AS Сегмент
                FROM 
                    Клиенты K
                LEFT JOIN 
                    TBL_segmentation S ON S.id = K.segmentation
                WHERE 
                    K.department <> 34 
                    AND K.КодПоставщика = K.masterID
                    AND segmentation = ?;
                """
        # and КодПоставщика = 3303
        # and segmentation  = "указать код сегмента"

        cursor = conn.cursor()
        cursor.execute(SQL_QUERY, segment)

        records = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]

        # Запис результатів у CSV файл
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')

            # Запис імен колонок
            writer.writerow(column_names)

            # Запис рядків
            for row in records:
                writer.writerow(row)

        # Закриття з'єднання
        cursor.close()
        conn.close()

        print(f"Дані успішно експортовані в {file_path}")

        # print(records)
        # for r in records:
        #    print(f"{r.КодПоставщика};{r.Название};{r.ОбращатьсяК};{r.НомерТелефона};{r.email};{r.Сегмент}")
        return file_path


if __name__ == '__main__':
    segmentemail(0)
