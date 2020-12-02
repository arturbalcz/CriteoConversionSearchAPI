import csv
import mysql.connector as connector
from model.click_entity import drop_table_script, create_table_script, insert_entity_script


def import_data_from_csv():
    filename = 'resource/ccs_top_100.csv'

    db = connector.connect(host='localhost', port='33069', password='q1w2e3r4', user='root', database='ccs')
    cursor = db.cursor()
    cursor.execute(drop_table_script)
    cursor.execute(create_table_script)

    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            cursor.execute(insert_entity_script, tuple(row))
    db.commit()


if __name__ == '__main__':
    import_data_from_csv()
