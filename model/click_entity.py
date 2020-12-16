class Click:
    ID = 0
    SALE = 1
    SALES_AMOUNT = 2
    TIME_DELAY_FOR_CONVERSION = 3
    CLICK_TIMESTAMP = 4
    NB_CLICKS_ONE_WEEK = 5
    PRODUCT_PRICE = 6
    PRODUCT_ID = 20
    PARTNER_ID = 22
    CLICK_DATE = 24

    drop_click_table_script = "DROP TABLE IF EXISTS CLICK;"
    create_click_table_script = "CREATE TABLE CLICK (" \
                            "ID INT AUTO_INCREMENT PRIMARY KEY," \
                            "SALE INT," \
                            "SALES_AMOUNT FLOAT," \
                            "TIME_DELAY_FOR_CONVERSION INT," \
                            "CLICK_TIMESTAMP INT," \
                            "NB_CLICKS_ONE_WEEK INT," \
                            "PRODUCT_PRICE FLOAT," \
                            "PRODUCT_AGE_GROUP VARCHAR(32)," \
                            "DEVICE_TYPE VARCHAR(32)," \
                            "AUDIENCE_ID VARCHAR(32)," \
                            "PRODUCT_GENDER VARCHAR(32)," \
                            "PRODUCT_BRAND VARCHAR(32)," \
                            "PRODUCT_CATEGORY_1 VARCHAR(32)," \
                            "PRODUCT_CATEGORY_2 VARCHAR(32)," \
                            "PRODUCT_CATEGORY_3 VARCHAR(32)," \
                            "PRODUCT_CATEGORY_4 VARCHAR(32)," \
                            "PRODUCT_CATEGORY_5 VARCHAR(32)," \
                            "PRODUCT_CATEGORY_6 VARCHAR(32)," \
                            "PRODUCT_CATEGORY_7 VARCHAR(32)," \
                            "PRODUCT_COUNTRY VARCHAR(32)," \
                            "PRODUCT_ID VARCHAR(32)," \
                            "PRODUCT_TITLE VARCHAR(512)," \
                            "PARTNER_ID VARCHAR(32)," \
                            "USER_ID VARCHAR(32)," \
                            "CLICK_DATE DATE" \
                            ");"
    insert_click_entity_script = "INSERT INTO CLICK (" \
                             "SALE," \
                             "SALES_AMOUNT," \
                             "TIME_DELAY_FOR_CONVERSION," \
                             "CLICK_TIMESTAMP," \
                             "NB_CLICKS_ONE_WEEK," \
                             "PRODUCT_PRICE," \
                             "PRODUCT_AGE_GROUP," \
                             "DEVICE_TYPE," \
                             "AUDIENCE_ID," \
                             "PRODUCT_GENDER," \
                             "PRODUCT_BRAND," \
                             "PRODUCT_CATEGORY_1," \
                             "PRODUCT_CATEGORY_2," \
                             "PRODUCT_CATEGORY_3," \
                             "PRODUCT_CATEGORY_4," \
                             "PRODUCT_CATEGORY_5," \
                             "PRODUCT_CATEGORY_6," \
                             "PRODUCT_CATEGORY_7," \
                             "PRODUCT_COUNTRY," \
                             "PRODUCT_ID," \
                             "PRODUCT_TITLE," \
                             "PARTNER_ID," \
                             "USER_ID," \
                             "CLICK_DATE" \
                             ")" \
                             "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    select_distinct_partner_id_script = "SELECT DISTINCT PARTNER_ID FROM CLICK;"
    select_distinct_click_day_where_partner_id_script = "SELECT DISTINCT CLICK_DATE FROM CLICK WHERE PARTNER_ID = %(partner_id)s;"
    select_distinct_product_id_where_partner_id_and_click_date_script = "SELECT DISTINCT PRODUCT_ID FROM CLICK WHERE PARTNER_ID = %(partner_id)s AND CLICK_DATE = %(click_date)s;"
    select_all_where_partner_id_and_click_date_and_product_id_script = "SELECT * FROM CLICK WHERE PARTNER_ID = %(partner_id)s AND CLICK_DATE = %(click_date)s AND PRODUCT_ID = %(product_id)s;"
