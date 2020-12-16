import csv
from datetime import date

import mysql.connector as connector

from model.click_entity import Click
from model.partner_entity import Partner
from model.product_day_entity import ProductDay

filename = 'resource/ccs_top_100.csv'

db = connector.connect(host='localhost', port='33069', password='q1w2e3r4', user='root', database='ccs')
cursor = db.cursor()


def import_data_from_csv():
    cursor.execute(Click.drop_click_table_script)
    cursor.execute(Click.create_click_table_script)

    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        i = 0
        for row in reader:
            entity = []
            for e in row:
                entity.append(e)
            entity.append(date.fromtimestamp(int(entity[3])).isoformat())
            cursor.execute(Click.insert_click_entity_script, tuple(entity))
            if ++i % 10000 == 0:
                db.commit()
    db.commit()


def calculate_product_day():
    cursor.execute(ProductDay.drop_product_day_table_script)
    cursor.execute(ProductDay.create_product_day_table_script)

    cursor.execute(Click.select_distinct_partner_id_script)
    partner_ids = cursor.fetchall()
    partner_id = partner_ids[0][0]

    cursor.execute(Click.select_distinct_click_day_where_partner_id_script, {'partner_id': partner_id})
    days_for_partner = cursor.fetchall()
    for day_tuple in days_for_partner:
        day = day_tuple[0]

        cursor.execute(Click.select_distinct_product_id_where_partner_id_and_click_date_script,
                       {'partner_id': partner_id, 'click_date': day})
        products_in_day = cursor.fetchall()
        for product_tuple in products_in_day:

            product_id = product_tuple[0]
            cursor.execute(Click.select_all_where_partner_id_and_click_date_and_product_id_script,
                           {'partner_id': partner_id, 'click_date': day, 'product_id': product_id})
            clicks_for_product = cursor.fetchall()

            daily_clicks_number = 0
            daily_sales_number = 0
            daily_sales_amount = 0
            for click in clicks_for_product:
                daily_clicks_number += 1
                sales_amount = click[Click.SALES_AMOUNT]
                if sales_amount != -1:
                    daily_sales_number += 1
                    daily_sales_amount += sales_amount

            product_day_entity = [product_id, partner_id, daily_sales_amount, daily_clicks_number, daily_sales_number,
                                  day]
            cursor.execute(ProductDay.insert_product_day_entity_script, tuple(product_day_entity))
        db.commit()


def calculate_partner():
    cursor.execute(Partner.drop_partner_table_script)
    cursor.execute(Partner.create_partner_table_script)

    cursor.execute(ProductDay.select_distinct_partner_id_script)
    partner_ids = cursor.fetchall()
    partner_id = partner_ids[0][0]

    cursor.execute(ProductDay.select_all_where_partner_id_script, {'partner_id': partner_id})
    products_for_partner = cursor.fetchall()

    total_sales_amount = 0
    total_clicks_number = 0
    for product in products_for_partner:
        total_sales_amount += product[ProductDay.DAILY_SALES_AMOUNT]
        total_clicks_number += product[ProductDay.DAILY_CLICKS_NUMBER]

    single_click_cost = total_sales_amount * 0.12 / total_clicks_number

    partner_entity = [partner_id, total_sales_amount, total_clicks_number, single_click_cost]
    cursor.execute(Partner.insert_partner_entity_script, tuple(partner_entity))
    db.commit()


if __name__ == '__main__':
    import_data_from_csv()
    calculate_product_day()
    calculate_partner()
