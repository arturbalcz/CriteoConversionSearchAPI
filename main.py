import copy
import csv
import datetime
import json
from statistics import stdev

import mysql.connector as connector

from algorithm.pseudorandom import PseudorandomAlgorithm
from algorithm.ucb import UcbAlgorithm
from model.click_entity import Click
from model.partner_entity import Partner
from model.product_day_entity import ProductDay
from model.product_day_mean_entity import ProductDayMean
from model.product_statistics import ProductStatistics
from model.working_data_entity import WorkingData

filename = 'resource/CriteoSearchData'
results_path = 'results/'

db = connector.connect(host='localhost', port='33069', password='q1w2e3r4', user='root', database='ccs')
cursor = db.cursor()

cost_factor = 0.12
profit_factor = 0.22


def db_cleanup():
    cursor.execute(Click.drop_click_table_script)
    cursor.execute(ProductDay.drop_product_day_table_script)
    cursor.execute(Partner.drop_partner_table_script)
    cursor.execute(WorkingData.drop_table_script)
    cursor.execute(ProductDayMean.drop_product_day_table_script)


def db_setup():
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
            click_date = datetime.datetime.utcfromtimestamp(int(entity[3])).date().isoformat()
            entity.append(click_date)
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


def calculate_product_day_mean(partner_ids):
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
    calculate_product_day(partner_ids)
    calculate_product_day_mean(partner_ids)


def calculate_daily_profit(products):
    daily_profit = 0
    for product in products:
        product_profit = product[ProductStatistics.DAILY_PROFIT]
        daily_profit += product_profit

    return daily_profit


def generate_excluded_products_result(partner_ids, strategy, algorithm, *params):
    for partner_tuple in partner_ids:
        partner_id = partner_tuple[0]

        cursor.execute(ProductDay.select_distinct_day_date_where_partner_id_script, {'partner_id': partner_id})
        days = cursor.fetchall()

        results = []
        products_seen_so_far = []
        excluded_products = []
        total_excluded_products_profit = 0
        for day_tuple in days:
            day = day_tuple[0]
            day_record = {}
            products_to_exclude = excluded_products
            cursor.execute(ProductStatistics.select_products_statistics_where_partner_id_and_day_script,
                           {'date': day, 'partner_id': partner_id})
            products = cursor.fetchall()
            excluded_products = algorithm(products, *params)
            products_actually_excluded = list(set(products).intersection(products_to_exclude))

            profit_before_exclusion = calculate_daily_profit(products)
            excluded_products_profit = calculate_daily_profit(products_actually_excluded)
            profit_after_exclusion = profit_before_exclusion - excluded_products_profit
            total_excluded_products_profit -= excluded_products_profit

            products_in_day_ids = \
                list(map(lambda p: p[ProductStatistics.PRODUCT_ID], products))
            products_to_exclude_next_day_ids = \
                list(map(lambda p: p[ProductStatistics.PRODUCT_ID], excluded_products))
            products_to_exclude_ids = \
                list(map(lambda p: p[ProductStatistics.PRODUCT_ID], products_to_exclude))
            products_actually_excluded_ids = \
                list(map(lambda p: p[ProductStatistics.PRODUCT_ID], products_actually_excluded))

            day_record['day'] = str(day)
            day_record['products_seen_so_far'] = copy.copy(products_seen_so_far)
            day_record['products_in_day'] = products_in_day_ids
            day_record['products_to_exclude'] = products_to_exclude_ids
            day_record['products_to_exclude_next_day'] = products_to_exclude_next_day_ids
            day_record['products_actually_excluded'] = products_actually_excluded_ids
            day_record['profit_before_exclusion'] = profit_before_exclusion
            day_record['profit_after_exclusion'] = profit_after_exclusion
            day_record['excluded_products_profit'] = -excluded_products_profit
            day_record['total_excluded_products_profit'] = total_excluded_products_profit
            results.append(day_record)

            products_seen_so_far = sorted(list(set(products_seen_so_far + products_in_day_ids)))

        result = {'strategy': strategy, 'days': results}
        out_file_name = str(partner_id) + '_' + strategy + '.json'
        generate_results_file(out_file_name, result)


def generate_results_file(out_file_name, result):
    file_path = results_path + out_file_name
    with open(file_path, "w") as outfile:
        json.dump(result, outfile, indent=4)


if __name__ == '__main__':
    partners = [['C0F515F0A2D0A5D9F854008BA76EB537'], ['04A66CE7327C6E21493DA6F3B9AACC75'],
                ['C306F0AD20C9B20C69271CC79B2E0887']]

    # db_cleanup()
    # db_setup()
    # import_data_from_csv()
    # calculate_partner_data(partners)

    # partners = [['C0F515F0A2D0A5D9F854008BA76EB537']]
    generate_excluded_products_result(partners, 'pseudorandom', PseudorandomAlgorithm.exclude_products)
    generate_excluded_products_result(partners, 'ucb_beta_13', UcbAlgorithm.exclude_products, 13)
