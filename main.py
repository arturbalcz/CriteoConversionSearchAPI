import csv
from datetime import date

import mysql.connector as connector
from model.click_entity import drop_click_table_script, create_click_table_script, insert_click_entity_script


def import_data_from_csv():
    filename = 'resource/ccs_top_100.csv'

    db = connector.connect(host='localhost', port='33069', password='q1w2e3r4', user='root', database='ccs')
    cursor = db.cursor()
    cursor.execute(drop_click_table_script)
    cursor.execute(create_click_table_script)

    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            entity = []
            for e in row:
                entity.append(e)
            entity.append(date.fromtimestamp(int(entity[3])).isoformat())
            cursor.execute(insert_click_entity_script, tuple(entity))
    db.commit()


if __name__ == '__main__':
    import_data_from_csv()
