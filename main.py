import mysql.connector as connector
from model.ClickEntity import ClickEntity


def import_data_from_csv():
    db = connector.connect(host='localhost', port='33069', password='q1w2e3r4', user='root', database='ccs')
    cursor = db.cursor()
    click_entity = ClickEntity.create_from_csv_record("1	89.9	442485	1598929598	9	49.95")
    cursor.execute(ClickEntity.drop_table_script)
    cursor.execute(ClickEntity.create_table_script)
    cursor.execute(ClickEntity.insert_entity_script, click_entity)
    db.commit()


if __name__ == '__main__':
    import_data_from_csv()
