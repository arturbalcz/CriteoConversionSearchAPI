class ClickEntity:
    drop_table_script = "DROP TABLE IF EXISTS CLICK;"
    create_table_script = "CREATE TABLE CLICK (" \
                          "ID INT AUTO_INCREMENT PRIMARY KEY," \
                          "SALE INT," \
                          "SALES_AMOUNT FLOAT," \
                          "TIME_DELAY_FOR_CONVERSION INT," \
                          "CLICK_TIMESTAMP VARCHAR(100)," \
                          "NB_CLICKS_ONE_WEEK INT," \
                          "PRODUCT_PRICE FLOAT" \
                          ");"
    insert_entity_script = "INSERT INTO CLICK (SALE, " \
                           "SALES_AMOUNT, " \
                           "TIME_DELAY_FOR_CONVERSION, " \
                           "CLICK_TIMESTAMP, " \
                           "NB_CLICKS_ONE_WEEK, " \
                           "PRODUCT_PRICE) " \
                           "VALUES (%s,%s,%s,%s,%s, %s)"

    def __init__(self, sale,
                 sales_amount_euro,
                 time_delay_for_conversion,
                 click_timestamp,
                 nb_clicks_one_week,
                 product_price,
                 product_age_group,
                 device_type,
                 audience_id,
                 product_gender,
                 product_brand,
                 product_category,
                 product_country,
                 product_id,
                 product_title,
                 partner_id,
                 user_id
                 ):
        self.sale = sale
        self.sales_amount_euro = sales_amount_euro
        self.time_delay_for_conversion = time_delay_for_conversion
        self.click_timestamp = click_timestamp
        self.nb_clicks_one_week = nb_clicks_one_week
        self.product_price = product_price
        # self.product_age_group = product_age_group
        # self.device_type = device_type
        # self.audience_id = audience_id
        # self.product_gender = product_gender
        # self.product_brand = product_brand
        # self.product_category = product_category
        # self.product_country = product_country
        # self.product_id = product_id
        # self.product_title = product_title
        # self.partner_id = partner_id
        # self.user_id = user_id

    @staticmethod
    def create_from_csv_record(line: str, separator='\t'):
        values = line.split(separator)
        return (values[0],
                values[1],
                values[2],
                values[3],
                values[4],
                values[5])
        # values[6],
        # values[7],
        # values[8],
        # values[9],
        # values[10],
        # values[11],
        # values[12],
        # values[13],
        # values[14],
        # values[15],
        # values[16]
        # )
