class ProductDay:
    ID = 0
    PRODUCT_ID = 1
    PARTNER_ID = 2
    DAILY_SALES_AMOUNT = 3
    DAILY_CLICKS_NUMBER = 4
    DAILY_SALES_NUMBER = 5
    DAY_DATE = 6

    drop_product_day_table_script = "DROP TABLE IF EXISTS PRODUCT_DAY;"
    create_product_day_table_script = "CREATE TABLE IF NOT EXISTS PRODUCT_DAY (" \
                      "ID INT AUTO_INCREMENT PRIMARY KEY," \
                      "PRODUCT_ID VARCHAR(32)," \
                      "PARTNER_ID VARCHAR(32)," \
                      "DAILY_SALES_AMOUNT FLOAT," \
                      "DAILY_CLICKS_NUMBER INT, " \
                      "DAILY_SALES_NUMBER INT," \
                      "DAY_DATE DATE" \
                      ");"
    insert_product_day_entity_script = "INSERT INTO PRODUCT_DAY (" \
                       "PRODUCT_ID," \
                       "PARTNER_ID," \
                       "DAILY_SALES_AMOUNT," \
                       "DAILY_CLICKS_NUMBER," \
                       "DAILY_SALES_NUMBER," \
                       "DAY_DATE" \
                       ")" \
                       "VALUES (%s,%s,%s,%s,%s,%s);"

    select_distinct_partner_id_script = "SELECT DISTINCT PARTNER_ID FROM PRODUCT_DAY;"
    select_all_where_partner_id_script = "SELECT * FROM PRODUCT_DAY WHERE PARTNER_ID = %(partner_id)s;"
    select_distinct_product_id_where_partner_id_script = "SELECT DISTINCT PRODUCT_ID FROM PRODUCT_DAY WHERE PARTNER_ID = %(partner_id)s;"
    select_distinct_day_date_script = "SELECT DISTINCT DAY_DATE FROM PRODUCT_DAY ORDER BY DAY_DATE;"
    select_distinct_day_date_where_partner_id_script = "SELECT DISTINCT DAY_DATE FROM PRODUCT_DAY WHERE PARTNER_ID = %(partner_id)s ORDER BY DAY_DATE;"
    select_all_where_partner_id_and_product_id_script = "SELECT * FROM PRODUCT_DAY WHERE PARTNER_ID = %(partner_id)s AND PRODUCT_ID = %(product_id)s ORDER BY DAY_DATE ASC;"
