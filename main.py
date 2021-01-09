import csv
from datetime import date
from statistics import stdev

import mysql.connector as connector

from algorithm.pseudorandom import PseudorandomAlgorithm
from model.click_entity import Click
from model.partner_entity import Partner
from model.product_day_entity import ProductDay
from model.product_day_mean_entity import ProductDayMean
from model.working_data_entity import WorkingData

filename = 'resource/CriteoSearchData'

db = connector.connect(host='localhost', port='33069', password='q1w2e3r4', user='root', database='ccs')
cursor = db.cursor()

cost_factor = 0.12
profit_factor = 0.22


def db_setup():
    cursor.execute(Click.drop_click_table_script)
    cursor.execute(ProductDay.drop_product_day_table_script)
    cursor.execute(Partner.drop_partner_table_script)
    cursor.execute(WorkingData.drop_table_script)
    cursor.execute(ProductDayMean.drop_product_day_table_script)

    cursor.execute(Click.create_click_table_script)
    cursor.execute(ProductDay.create_product_day_table_script)
    cursor.execute(Partner.create_partner_table_script)
    cursor.execute(WorkingData.create_table_script)
    cursor.execute(ProductDayMean.create_product_day_table_script)


def import_data_from_csv():
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        i = 0
        for row in reader:
            entity = []
            for e in row:
                entity.append(e)
            entity.append(date.fromtimestamp(int(entity[3])).isoformat())
            cursor.execute(Click.insert_click_entity_script, tuple(entity))
            if i % 10000 == 0:
                print('PROCESSED ' + str(i) + ' RECORDS')
                db.commit()
            i += 1
        print('PROCESSED TOTAL ' + str(i) + ' RECORDS')
        file.close()

    db.commit()


def create_working_table_for_partner(partner_id):
    cursor.execute(Click.select_working_data_where_partner_id_script, {'partner_id': partner_id})
    working_data_for_partner = cursor.fetchall()

    print('CREATING WORKING TABLE FOR PARTNER: ' + str(partner_id))
    for entity in working_data_for_partner:
        cursor.execute(WorkingData.insert_entity_script, entity)
    db.commit()


def calculate_product_day(partner_ids):
    for partner_tuple in partner_ids:
        partner_id = partner_tuple[0]
        print('PROCESSING PARTNER: ' + str(partner_id))
        create_working_table_for_partner(partner_id)

        cursor.execute(WorkingData.select_distinct_product_id)
        products_for_partner = cursor.fetchall()

        print('PROCESSING DATA FOR PARTNER: ' + str(partner_id))
        total_sales_amount = 0
        total_clicks_number = 0
        for product_tuple in products_for_partner:
            product_id = product_tuple[0]
            cursor.execute(WorkingData.select_distinct_click_day_where_product_id_script,
                           {'product_id': product_id})
            days_for_product = cursor.fetchall()

            for day_tuple in days_for_product:
                day = day_tuple[0]
                cursor.execute(WorkingData.select_all_where_click_date_and_product_id_script,
                               {'click_date': day, 'product_id': product_id})
                clicks_for_product = cursor.fetchall()

                daily_clicks_number = 0
                daily_sales_number = 0
                daily_sales_amount = 0
                for click in clicks_for_product:
                    daily_clicks_number += 1
                    sales_amount = click[WorkingData.SALES_AMOUNT]
                    if sales_amount != -1:
                        daily_sales_number += 1
                        daily_sales_amount += sales_amount

                total_sales_amount += daily_sales_amount
                total_clicks_number += daily_clicks_number

                product_day_entity = [product_id, partner_id, daily_sales_amount, daily_clicks_number,
                                      daily_sales_number, day]
                cursor.execute(ProductDay.insert_product_day_entity_script, tuple(product_day_entity))

        single_click_cost = total_sales_amount * cost_factor / total_clicks_number
        partner_entity = [partner_id, total_sales_amount, total_clicks_number, single_click_cost]
        cursor.execute(Partner.insert_partner_entity_script, tuple(partner_entity))
        db.commit()
        cursor.execute(WorkingData.delete_all_script)
        db.commit()
        print('FINISHED PROCESSING PARTNER: ' + str(partner_id))

    cursor.execute(WorkingData.delete_all_script)
    db.commit()


def calculate_product_day_mean():
    cursor.execute(ProductDay.select_distinct_partner_id_script)
    partner_ids = cursor.fetchall()
    for partner_tuple in partner_ids:
        partner_id = partner_tuple[0]
        cursor.execute(Partner.select_all_where_partner_id_script, {'partner_id': partner_id})
        partner_data = cursor.fetchall()
        per_partner_cost = partner_data[0][Partner.SINGLE_CLICK_COST]
        print('CALCULATING MEAN FOR PARTNER: ' + str(partner_id))

        cursor.execute(ProductDay.select_distinct_product_id_where_partner_id_script, {'partner_id': partner_id})
        products_for_partner = cursor.fetchall()

        for product_tuple in products_for_partner:
            product_id = product_tuple[0]

            cursor.execute(ProductDay.select_all_where_partner_id_and_product_id_script,
                           {'partner_id': partner_id, 'product_id': product_id})
            product_days_for_product = cursor.fetchall()

            mean = 0
            days_counter = 0
            for product_day in product_days_for_product:
                days_counter += 1
                income = product_day[ProductDay.DAILY_SALES_AMOUNT] * profit_factor
                cost = product_day[ProductDay.DAILY_CLICKS_NUMBER] * per_partner_cost
                profit = income - cost
                mean = (mean + profit) / days_counter
                std_dev = stdev([mean, profit])

                mean_entity = [product_day[ProductDay.ID], profit, cost, mean, std_dev]

                cursor.execute(ProductDayMean.insert_product_day_entity_script, tuple(mean_entity))

        db.commit()
        print('FINISHED CALCULATING MEAN FOR PARTNER: ' + str(partner_id))

    db.commit()


def calculate_partner_data(partner_ids):
    partner_ids = [['C0F515F0A2D0A5D9F854008BA76EB537'], ['04A66CE7327C6E21493DA6F3B9AACC75'],
                   ['C306F0AD20C9B20C69271CC79B2E0887']]
    calculate_product_day()
    calculate_product_day_mean()


def generate_excluded_products_result(algorithm, *params):

    algorithm(products, *params)


if __name__ == '__main__':
    generate_excluded_products_result(PseudorandomAlgorithm.exclude_products)
