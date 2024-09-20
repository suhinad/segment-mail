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
        select  
            КодПоставщика,
            Название,
            REPLACE(REPLACE(ОбращатьсяК, CHAR(13), ' '), CHAR(10), ' ') as ОбращатьсяК,
            НомерТелефона,
            REPLACE(REPLACE(email, CHAR(13), ' '), CHAR(10), ' ') as email,
            D.nazv,
            REPLACE(REPLACE(S.name, CHAR(13), ' '), CHAR(10), ' ') AS Сегмент
        from
            Клиенты K
        left join
            TBL_segmentation S on S.id = K.segmentation
        left join
            departments D on D.id = K.department
        where
            k.department in (1,2,4,5,8,9,10,12,14,16,19,20,23,29,31,32,33,35,38,40,47.48,57,61,71) and K.КодПоставщика = K.masterID;
        """

        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)

        records = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]

        # Запис результатів у CSV файл
        with open(file_path, mode='w', newline='', encoding='windows-1251', errors='replace') as file:
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

    else:
        connectionString = (f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};'
                            f'DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}')

        conn = pyodbc.connect(connectionString)

        SQL_QUERY = """
                select  
                    КодПоставщика,
                    Название,
                    REPLACE(REPLACE(ОбращатьсяК, CHAR(13), ' '), CHAR(10), ' ') as ОбращатьсяК,
                    НомерТелефона,
                    REPLACE(REPLACE(email, CHAR(13), ' '), CHAR(10), ' ') as email,
                    D.nazv,
                    REPLACE(REPLACE(S.name, CHAR(13), ' '), CHAR(10), ' ') AS Сегмент
                from
                    Клиенты K
                left join
                    TBL_segmentation S on S.id = K.segmentation
                left join
                    departments D on D.id = K.department
                where
                    k.department in (1,2,4,5,8,9,10,12,14,16,19,20,23,29,31,32,33,35,38,40,47.48,57,61,71) 
                    and K.КодПоставщика = K.masterID and  segmentation = ?;
                """

        cursor = conn.cursor()
        cursor.execute(SQL_QUERY, segment)

        records = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]

        # Запис результатів у CSV файл
        with open(file_path, mode='w', newline='', encoding='windows-1251') as file:
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


if __name__ == '__main__':
    segmentemail(0, "Всі")
